const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

const oldReplacement = `isClosureNode :: forall r. Ref { globalTypes :: Map.Map String ExprType | r } -> TcoExpr -> Boolean
isClosureNode helpersRef expr = case unwrapTcoExpr expr of`;

const newReplacement = `isClosureNode :: forall r. Ref { globalTypes :: Map.Map String ExprType | r } -> TcoExpr -> Boolean
isClosureNode helpersRef expr = case extractExprFuncType (getExprType expr) of
  Just _ -> true
  Nothing -> case unwrapTcoExpr expr of`;

if (content.includes(oldReplacement)) {
  content = content.replace(oldReplacement, newReplacement);
  fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
  console.log("Success");
} else {
  console.log("Failed to find replacement string");
}
