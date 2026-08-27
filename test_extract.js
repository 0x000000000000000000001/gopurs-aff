const fs = require('fs');
const dump = JSON.parse(fs.readFileSync('dump.json'));

function findMapParentType(node) {
  if (Array.isArray(node)) {
    for (const item of node) {
      const res = findMapParentType(item);
      if (res) return res;
    }
  } else if (typeof node === 'object' && node !== null) {
    if (node.value1 && node.value1.value0 && node.value1.value1 === '_map' && node.value1.value0.value0 === 'Effect.Aff') {
         return node;
    }
    for (const key in node) {
      const res = findMapParentType(node[key]);
      if (res) return res;
    }
  }
  return null;
}

const node = findMapParentType(dump);
console.log(JSON.stringify(node.value0, null, 2));
