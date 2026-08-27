const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/Effect.Aff/corefn.json', 'utf8'));

let neverDecl = data.decls.find(d => d.identifier === 'never');
console.log(JSON.stringify(neverDecl.expression.argument.abstraction.body.argument, null, 2));
