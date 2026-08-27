const fs = require('fs');
const corefn = JSON.parse(fs.readFileSync('output/Effect.Aff/corefn.json'));
const f = corefn.foreign.find(x => x === '_map');
if (f) {
  console.log("foreign import _map exists");
}
