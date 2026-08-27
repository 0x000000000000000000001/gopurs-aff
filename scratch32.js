const fs = require('fs');
const path = require('path');
const corefn = JSON.parse(fs.readFileSync('output/Data.Monoid/corefn.json', 'utf8'));
const mempty = corefn.decls.find(d => d.identifier === 'mempty' || (d.binds && d.binds.some(b => b.identifier === 'mempty')));
console.log(JSON.stringify(mempty, null, 2));
