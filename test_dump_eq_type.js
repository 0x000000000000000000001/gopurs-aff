const fs = require('fs');
const dump = JSON.parse(fs.readFileSync('dump.json'));

function findTypedAccessor(node) {
  if (Array.isArray(node)) {
    for (const item of node) {
      const res = findTypedAccessor(item);
      if (res) return res;
    }
  } else if (typeof node === 'object' && node !== null) {
    if (node.value1 && node.value1.value1 === 'eq' && node.value1.value0 && node.value1.value0.value0 && node.value1.value0.value0.value1 === 'eqArray') {
         return node;
    }

    for (const key in node) {
      const res = findTypedAccessor(node[key]);
      if (res) return res;
    }
  }
  return null;
}

const node = findTypedAccessor(dump);
console.log(JSON.stringify(node.value0, null, 2));
