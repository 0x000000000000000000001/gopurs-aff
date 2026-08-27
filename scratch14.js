const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/Test.Main/corefn.json', 'utf8'));
console.log(Object.keys(data));
console.log(Object.keys(data.decls[0]));
