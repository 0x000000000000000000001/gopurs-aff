const fs = require('fs');
const corefn = JSON.parse(fs.readFileSync('output/Data.Monoid/corefn.json'));
const mempty = corefn.decls.find(d => d.bindType === 'NonRec' && d.expression.abstraction && d.expression.abstraction.value.identifier === 'mempty' || d.bindType === 'Rec' && d.binds.some(b => b.identifier === 'mempty') || d.identifier === 'mempty');
console.log(JSON.stringify(mempty.annotation.type, null, 2));
