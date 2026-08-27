const fs = require('fs');
const ast = JSON.parse(fs.readFileSync('output/Test.Main/corefn.json', 'utf8'));

function findBracket(expr) {
  if (!expr) return null;
  if (expr.binds) {
    for (const b of expr.binds) {
      if (b.identifier === 'test_bracket') return b.expression;
    }
  }
  for (const k in expr) {
    if (typeof expr[k] === 'object') {
      const res = findBracket(expr[k]);
      if (res) return res;
    }
  }
  return null;
}

const bracket = findBracket(ast);
fs.writeFileSync('bracket.json', JSON.stringify(bracket, null, 2));
