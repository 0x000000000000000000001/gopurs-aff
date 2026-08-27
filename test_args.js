const fs = require('fs');
const dump = JSON.parse(fs.readFileSync('dump.json'));

function traverse(node) {
  if (Array.isArray(node)) {
    for (const item of node) {
      traverse(item);
    }
  } else if (typeof node === 'object' && node !== null) {
    if (node.type === 'App' && node.value0 && node.value0.value0 && node.value0.value0.value1 === '_map') {
       console.log("FOUND MAP CALL!");
       console.log(JSON.stringify(node.value1, null, 2)); // Print the first argument
       process.exit(0);
    }
    for (const key in node) {
      traverse(node[key]);
    }
  }
}
traverse(dump);
