const fs = require('fs');

const data = JSON.parse(fs.readFileSync('output/Test.Main/corefn.json', 'utf8'));
function walk(node, parentType) {
  if (Array.isArray(node)) {
    node.forEach(n => walk(n, parentType));
  } else if (node && typeof node === 'object') {
    let t = parentType;
    if (node.type === 'Typed') {
      t = node.annotation && node.annotation.type ? node.annotation.type : 'UnknownType';
    }
    if (node.type === 'Accessor') {
      console.log('Accessor found, parentType:', JSON.stringify(t));
    }
    for (const key in node) {
      if (key !== 'type') walk(node[key], t);
    }
  }
}

walk(data, 'NoParentType');
