const fs = require('fs');
const dump = JSON.parse(fs.readFileSync('dump.json'));

function hasEqArray(node) {
  if (Array.isArray(node)) {
    for (const item of node) {
      if (hasEqArray(item)) return true;
    }
  } else if (typeof node === 'object' && node !== null) {
    if (node.value1 === 'eqArray' && node.value0 && node.value0.value0 === 'Test.Main') return true;
    for (const key in node) {
      if (hasEqArray(node[key])) return true;
    }
  }
  return false;
}

function findMapWithEqArray(node) {
  if (Array.isArray(node)) {
    for (const item of node) {
      const res = findMapWithEqArray(item);
      if (res) return res;
    }
  } else if (typeof node === 'object' && node !== null) {
    // Check if this node is an ExprApp of _map
    if (node.value0 && node.value0.value0 && node.value0.value0.value1 === '_map' && node.value1 && Array.isArray(node.value1)) {
       // Check if any argument contains eqArray
       if (hasEqArray(node.value1)) {
         return node;
       }
    }

    for (const key in node) {
      const res = findMapWithEqArray(node[key]);
      if (res) return res;
    }
  }
  return null;
}

const node = findMapWithEqArray(dump);
console.log(JSON.stringify(node, null, 2));
