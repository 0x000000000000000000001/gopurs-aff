const fs = require('fs');
const cache = JSON.parse(fs.readFileSync('output/purescript/Test_Main.gopurs-cache.json', 'utf8')).d;
const bindsGrp = cache.bindings;
for (const grp of bindsGrp) {
  const binds = grp.bindings;
  for (const b of binds) {
    if (b.value0 === 'test_kill_bracket_nested') {
      fs.writeFileSync('dump.json', JSON.stringify(b.value1, null, 2));
      break;
    }
  }
}
