const fs = require('fs');
const cache = JSON.parse(fs.readFileSync('output/purescript/Effect_Aff.gopurs-cache.json'));
console.log("MAP ARITY", JSON.stringify(cache['_map'], null, 2));
