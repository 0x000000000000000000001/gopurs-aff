const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/Effect.Aff/corefn.json', 'utf8'));

let monoidCancelerDecl = data.decls.find(d => d.identifier === 'monoidCanceler');
console.log(JSON.stringify(monoidCancelerDecl, null, 2));
