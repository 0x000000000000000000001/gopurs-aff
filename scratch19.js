const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/Data.Monoid/corefn.json', 'utf8'));

let memptyDecl = data.decls.find(d => d.identifier === 'mempty');
console.log(JSON.stringify(memptyDecl, null, 2));
