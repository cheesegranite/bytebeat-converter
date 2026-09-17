import base64
import numpy as np
import soundfile as sf
from scipy.signal import resample
from collections import Counter

list_repr = lambda x: ",".join(str(i).removeprefix("0") for i in x)
huffman_tree = {
    "," : [0],
    "1" : [1,0,0,0],
    "2" : [1,0,0,1],
    "3" : [1,0,1,0],
    "4" : [1,0,1,1],
    "5" : [1,1,0,0],
    "6" : [1,1,0,1],
    "7" : [1,1,1,0,0],
    "8" : [1,1,1,0,1],
    "9" : [1,1,1,1,0],
    "0" : [1,1,1,1,1]
}

def convert_to_decimal(number):
    decimal = 0
    for bit in number:
        decimal *= 2
        decimal += int(bit)
    return decimal

def encode(data, error=1):
    encoded = []
    current = 0
    err0r = 0
    for i, sample in enumerate(data):
        if i % 1000 == 0:
            print(f"\rencoding... {i}/{len(data)}  {i/len(data):.1%} ", end="")
        err0r += abs(sample - current)
        if err0r > error:
            encoded.append(sample - current)
            current = sample
            err0r = 0
        else:
            encoded.append(0)
    print(f"\rencoding... {len(data)}/{len(data)} 100.0% ")

    print("finalizing...", end="")
    common = Counter(encoded).most_common()
    common_lookup = {value: i for i, (value, _) in enumerate(common)}
    common_fbvlve_lookup = [value for value, _ in common]
    encoded_fbvlve = [common_lookup[value] for value in encoded]

    huffman_ready = list_repr(encoded_fbvlve)
    encoded_bits = []
    for i, char in enumerate(huffman_ready):
        if i % 1000 == 0:
            print(f"\rfinalizing... {i}/{len(huffman_ready)}  {i/len(huffman_ready):.1%} ", end="")
        encoded_bits.extend(huffman_tree[char])
    bit_length = len(encoded_bits)
    while len(encoded_bits) % 8:
        encoded_bits.append(0)

    chunks = [encoded_bits[i:i + 8] for i in range(0, len(encoded_bits), 8)]
    chunks_new = []
    for chunk in chunks:
        chunk = "".join(str(bit) for bit in chunk)
        chunks_new.append(convert_to_decimal(chunk))
    chunks = bytes(chunks_new)
    print(f"\rfinalizing... {len(huffman_ready)}/{len(huffman_ready)} 100.0% ")
    return [common_fbvlve_lookup, base64.b64encode(chunks).decode("ascii"), bit_length]

input_file = input("please enter file path:\n>")
target_sample_rate = input("please enter target sample rate:\n>")
compression = input("please enter compression level (0-255):\n>")

compression = np.clip(int(compression), 0, 255)
audio, sample_rate = sf.read(input_file)
if target_sample_rate.endswith("x"):
    target_sample_rate = float(target_sample_rate[:-1])
    target_sample_rate = int(sample_rate * target_sample_rate)
    if target_sample_rate != sample_rate:
        print(f"relative sample rate: {sample_rate}hz -> {target_sample_rate}hz")
    else:
        print(f"using input file sample rate ({sample_rate}hz)")
else:
    target_sample_rate = int(target_sample_rate.removesuffix("hz"))

if len(audio.shape) > 1:
    audio = np.mean(audio, axis=1)

new_length = int(len(audio) * target_sample_rate / sample_rate)
audio = resample(audio, new_length)

audio = np.clip(audio, -1.0, 1.0)
audio_8bit = ((audio + 1.0) * 127.5).astype(np.uint8)
audio_8bit = [*map(int, audio_8bit)]
encoded = encode(audio_8bit, error=compression)
output = (
    "[[" +
    list_repr(encoded[0]) +
    "]," +
    str(encoded[2]) +
    ",`" +
    encoded[1].replace("\\","\\\\").replace("`","\\`") +
    "`]"
)

# output the fbvlve data
# change this to whatever you want
print("\n" + output + "\n")
