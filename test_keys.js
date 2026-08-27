const fs = require('fs');
const cache = JSON.parse(fs.readFileSync('output/purescript/Effect_Aff.gopurs-cache.json'));
let mapArity = undefined;
function findMap(node) {
  if (typeof node === 'object' && node !== null) {
    if (node.value2 === '_map') return node;
    for (let k in node) {
       let res = findMap(node[k]);
       if (res) return res;
    }
  }
  return null;
}
console.log(JSON.stringify(findMap(cache.d.foreign), null, 2));
