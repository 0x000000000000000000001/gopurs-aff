const fs = require('fs');
const corefn = JSON.parse(fs.readFileSync('output/Effect.Aff/corefn.json', 'utf8'));
const monoidCanceler = corefn.decls.find(d => d.identifier === 'monoidCanceler' || (d.binds && d.binds.some(b => b.identifier === 'monoidCanceler')));
console.log(JSON.stringify(monoidCanceler, null, 2));
