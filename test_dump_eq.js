const fs = require('fs');
const dump = JSON.parse(fs.readFileSync('dump.json'));

function findEqNode(node) {
  if (Array.isArray(node)) {
    for (const item of node) {
      const res = findEqNode(item);
      if (res) return res;
    }
  } else if (typeof node === 'object' && node !== null) {
    if (node.value1 && node.value1.value0 === 'eq' && node.value0 && node.value0.value0 && node.value0.value0.value1 === 'eqArray') {
         return node;
    }

    for (const key in node) {
      const res = findEqNode(node[key]);
      if (res) return res;
    }
  }
  return null;
}

const node = findEqNode(dump);
// BUT we need the Typed wrapper around eq!
// wait, ExprAccessor is wrapped in Typed? No, ExprAccessor is NOT wrapped in Typed directly if it's the function!
// Wait! `node` IS the ExprAccessor!
// Does ExprAccessor have a type?
// In CoreFn.purs, ExprAccessor a (Expr a) String.
// So node.value0 is the `a` (which is the type)!
console.log(JSON.stringify(node.value0, null, 2));
