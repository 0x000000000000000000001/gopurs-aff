const fs = require('fs');

const data = JSON.parse(fs.readFileSync('output/Effect.Aff/corefn.json'));
console.log(JSON.stringify(data.decls.find(d => d.value0 === '_map' || (d.value1 && d.value1.value0 === '_map')) || data.foreign.find(x => x === '_map'), null, 2));

const cache = JSON.parse(fs.readFileSync('.gopurs-cache.json'));
const aff = cache['Effect.Aff'];
if (aff) {
   console.log("From cache:", JSON.stringify(aff.moduleArities['_map'], null, 2));
}

