const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

const oldReplacement = `unwrapTcoExpr :: TcoExpr -> BackendSyntax TcoExpr
unwrapTcoExpr (TcoExpr _ (Typed _ (TcoExpr _ (Typed t e)))) = unwrapTcoExpr (TcoExpr nullSourceSpan (Typed t e))
unwrapTcoExpr (TcoExpr _ syn) = syn`;

const newReplacement = `unwrapTcoExpr :: TcoExpr -> BackendSyntax TcoExpr
unwrapTcoExpr (TcoExpr _ (Typed outer (TcoExpr _ (Typed inner e)))) = unwrapTcoExpr (TcoExpr nullSourceSpan (Typed outer e))
unwrapTcoExpr (TcoExpr _ syn) = syn`;

content = content.replace(oldReplacement, newReplacement);

fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
