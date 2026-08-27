const fs = require('fs');
const ast = JSON.parse(fs.readFileSync('output/Test.Main/corefn.json', 'utf8'));

let idents = [];
for (const decl of ast.decls) {
  if (decl.type === 'NonRec' || decl.type === 'Rec') {
    for (const b of decl.binds) {
      idents.push(b.identifier);
    }
  }
}
console.log(idents);
