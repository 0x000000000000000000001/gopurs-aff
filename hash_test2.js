function hs(str) {
  let hash = 5381;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) + hash) + str.charCodeAt(i);
  }
  return (hash >>> 0).toString();
}
const fs = require('fs');
const corefn = JSON.parse(fs.readFileSync('output/Data.Monoid/corefn.json'));
let types = [];
// extract all FQN
for (let key in corefn) {
    if (typeof corefn[key] === 'object' && corefn[key] !== null) {
        if (corefn[key].fqn) {
            types.push(corefn[key].fqn.join('.'));
        }
    }
}
types = [...new Set(types)];
for (let t of types) {
    console.log(t, hs(t));
}
