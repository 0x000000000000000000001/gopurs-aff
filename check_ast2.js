const fs = require('fs');
const corefn = JSON.parse(fs.readFileSync('output/Test.Main/corefn.json'));
let decl = corefn.decls.find(d => d.identifier === 'test_makeAff');
fs.writeFileSync('test_makeAff.json', JSON.stringify(decl, null, 2));
