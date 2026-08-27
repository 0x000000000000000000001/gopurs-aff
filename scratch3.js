const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

const replacement = `unwrapTcoExpr :: TcoExpr -> BackendSyntax TcoExpr
unwrapTcoExpr (TcoExpr _ (Typed _ (TcoExpr _ (Typed t e)))) = unwrapTcoExpr (TcoExpr nullSourceSpan (Typed t e))
unwrapTcoExpr (TcoExpr _ syn) = syn`;

content = content.replace(
  `unwrapTcoExpr :: TcoExpr -> BackendSyntax TcoExpr\nunwrapTcoExpr (TcoExpr _ syn) = syn`,
  replacement
);

fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
