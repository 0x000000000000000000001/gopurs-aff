const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/Effect/corefn.json', 'utf8'));

let applicativeEffectDecl = data.decls.find(d => d.identifier === 'applicativeEffect');
console.log(JSON.stringify(applicativeEffectDecl, null, 2));
