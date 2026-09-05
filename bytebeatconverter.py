import numpy as np
import soundfile as sf
from scipy.signal import resample
from collections import Counter

def encode(data, error = 1):
    encoded = []
    current = 0
    err0r = 0
    for i, sample in enumerate(data):
        print(f"\r{i}/{len(data)}  {i/len(data):.1%}", end="")
        err0r += abs(sample - current)
        if err0r > error:
            encoded.append(sample - current)
            current = sample
            err0r = 0
        else:
            encoded.append(0)
    print(f"\r{len(data)}/{len(data)} 100.0% ")

    print("finalizing...")
    common = Counter(encoded).most_common()
    common_lookup = {value: i for i, (value, _) in enumerate(common)}
    common_fbvlve_lookup = [value for value, _ in common]
    encoded_fbvlve = [common_lookup[value] for value in encoded]
    return [common_fbvlve_lookup, encoded_fbvlve]



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
list_repr = lambda x: ",".join(str(i).removeprefix("0") for i in x)
output = (
    "[[" +
    list_repr(encoded[0]) +
    "],[" +
    list_repr(encoded[1]) +
    "]]"
)

# output the fbvlve data
# change this to whatever you want
print("\n" + output + "\n")
