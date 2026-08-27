const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

content = content.replace(
  'TypeBool -> GoBinOp "!=" (GoSelector expr "IntVal") (GoInt 0)',
  'TypeBool -> let _ = unsafePerformEffect (Console.log ("unboxGoExpr to TypeBool for " <> printGoExpr expr <> "\\n" <> gopursTrace unit)) in GoBinOp "!=" (GoSelector expr "IntVal") (GoInt 0)'
);

fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
