fbvlve=(data,a,t)=>a+(data[0][data[1][t]??0]??0),
decode_all=(data)=>{let a=0;let decoded=[];for(let t=0;t<data[1].length;t++){decoded[t]=a=fbvlve(data,a,t);}return decoded;},
t||(e=0,a=decode_all(

[[],[]] // fbvlve data placeholder

)),e=a[t]??e
