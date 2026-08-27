const fs = require('fs');
const data = JSON.parse(fs.readFileSync('output/Test.Main/corefn.json', 'utf8'));

let untypedApps = 0;
let typedApps = 0;

function walk(node) {
  if (Array.isArray(node)) {
    node.forEach(walk);
  } else if (node && typeof node === 'object') {
    if (node.type === 'App') {
      const f = node.abstraction;
      if (f.annotation && f.annotation.type) {
        typedApps++;
      } else {
        untypedApps++;
        if (untypedApps < 3) console.log("Untyped App fn:", f.type, f.identifier);
      }
    }
    for (const key in node) {
      if (key !== 'type') walk(node[key]);
    }
  }
}

walk(data);
console.log("typedApps:", typedApps);
console.log("untypedApps:", untypedApps);
