const [_, __, pth, dat, hdr] = process.argv
let res = await fetch("https://www.bitget.com/v1/p2p/"+pth, {
  "method": "POST",
  "headers": JSON.parse(hdr),
  "body": dat,
});
res = await res.json()
console.log(JSON.stringify(res.data));