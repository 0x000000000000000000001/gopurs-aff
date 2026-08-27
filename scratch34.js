const fs = require('fs');
const corefn = JSON.parse(fs.readFileSync('output/Effect.Aff/corefn.json', 'utf8'));
const never = corefn.decls.find(d => d.identifier === 'never' || (d.binds && d.binds.some(b => b.identifier === 'never')));
console.log(JSON.stringify(never, null, 2));
