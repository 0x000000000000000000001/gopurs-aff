const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

content = content.replace(
  'Let name binding body, _ ->',
  'Let name binding body, _ ->\n            let _ = if String.contains (Pattern "__local_var_3_0") name then unsafePerformEffect (Console.log ("AST FOR __local_var_3_0: " <> printTcoExpr binding)) else unit\n            in'
);

content = content.replace(
  'return unboxGoExpr(boxGoExpr(v)(v1))(TypeValue.value)(v2);',
  'return unboxGoExpr(boxGoExpr(v)(v1))(TypeValue.value)(v2);'
);

fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
