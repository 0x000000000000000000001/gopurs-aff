const fs = require('fs');
const corefn = JSON.parse(fs.readFileSync('output/purescript/Test_Main.gopurs-cache.json')).d;
let bracket = corefn.bindings.find(b => {
  let inner = b;
  if (inner.value1) inner = inner.value1; // NonRecursive vs Recursive
  if (Array.isArray(inner)) inner = inner[0];
  return inner.value0 === 'test_bracket';
});
if (bracket) {
  if (bracket.value1) bracket = bracket.value1;
  if (Array.isArray(bracket)) bracket = bracket[0];
  console.log(JSON.stringify(bracket, null, 2));
} else {
  console.log("NOT FOUND");
}
