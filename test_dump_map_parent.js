const fs = require('fs');
const dump = JSON.parse(fs.readFileSync('dump.json'));

function findParent(node, targetVar) {
  if (Array.isArray(node)) {
    for (const item of node) {
      const res = findParent(item, targetVar);
      if (res) return res;
    }
  } else if (typeof node === 'object' && node !== null) {
    let hasTarget = false;
    for (const key in node) {
      const child = node[key];
      if (child && typeof child === 'object' && child.value0 && child.value0.value1 === targetVar) {
          hasTarget = true;
          break;
      }
      const res = findParent(child, targetVar);
      if (res) return res;
    }
    if (hasTarget) return node;
  }
  return null;
}

const node = findParent(dump, '_map');
console.log(JSON.stringify(node, null, 2));
