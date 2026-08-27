const fs = require('fs');
const dump = JSON.parse(fs.readFileSync('dump.json'));

function findEqArrayTyped(node) {
  if (Array.isArray(node)) {
    for (const item of node) {
      const res = findEqArrayTyped(item);
      if (res) return res;
    }
  } else if (typeof node === 'object' && node !== null) {
    if (node.value1 && node.value1.value0 && node.value1.value1 && node.value1.value1.value0) {
       const inner = node.value1.value1.value0;
       if (inner.value0 && inner.value0.value0 && inner.value0.value0.value0 && inner.value0.value0.value0.value0 === 'Test.Main' && inner.value0.value0.value1 === 'eqArray') {
         return node.value0;
       }
    }
    for (const key in node) {
      const res = findEqArrayTyped(node[key]);
      if (res) return res;
    }
  }
  return null;
}

const tp = findEqArrayTyped(dump);
console.log(JSON.stringify(tp, null, 2));
