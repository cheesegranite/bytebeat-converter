fbvlve=(data,a,t)=>a+(data[0][data[1][t]??0]??0),
b64decode=(data)=>{
    let chars="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let output="",buffer=0,bits=0;
    for(let c of data){
        if(c==="=") break;
        buffer=(buffer<<6)|chars.indexOf(c);
        bits+=6;
        if(bits>=8){
            bits-=8;
            output+=String.fromCharCode((buffer>>bits)&255);
        }
    }
    return output;
},
decode_huffman=(data,tree,bits)=>{
    data=b64decode(data);
    let decoded="",code="";
    for(let pos=0;pos<bits;pos++){
        code+=((data.charCodeAt(pos>>3)>>(7-(pos%8)))&1);
        if(tree[code]!=undefined){
            decoded+=tree[code];
            code="";
        }
    }
    return decoded;
},
decode_all=(data,tree)=>{
    let a=0;
    let decoded=decode_huffman(data[2],tree,data[1]).split(",").map(x=>x===""?0:+x);
    let output=[];
    for(let t=0;t<decoded.length;t++)
        output[t]=a=fbvlve([data[0],decoded],a,t);
    return output;
},
tree={
    "0":",",
    "1000":"1",
    "1001":"2",
    "1010":"3",
    "1011":"4",
    "1100":"5",
    "1101":"6",
    "11100":"7",
    "11101":"8",
    "11110":"9",
    "11111":"0"
},
data=

[[],0,``] // huffman fbvlve data placeholder

,t||(e=0,a=decode_all(data,tree)),e=a[t]??e
