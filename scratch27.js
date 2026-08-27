const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/Effect/corefn.json', 'utf8'));

let decl = data.decls.find(d => d.identifier.toLowerCase().includes('applicative'));
console.log(JSON.stringify(decl.identifier, null, 2));
