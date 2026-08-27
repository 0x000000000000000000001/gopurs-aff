const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

const oldReplacement = `isClosureNode :: forall r. Ref { globalTypes :: Map.Map String ExprType | r } -> TcoExpr -> Boolean
isClosureNode helpersRef expr = case extractExprFuncType (getExprType expr) of`;

const newReplacement = `stripNestedTyped :: TcoExpr -> TcoExpr
stripNestedTyped expr@(TcoExpr ann syn) = case syn of
  Typed t1 (TcoExpr ann2 (Typed t2 inner)) ->
    case extractExprFuncType t1 of
      Just _ -> stripNestedTyped (TcoExpr ann (Typed t1 inner))
      Nothing -> stripNestedTyped (TcoExpr ann2 (Typed t2 inner))
  _ -> expr

isClosureNode :: forall r. Ref { globalTypes :: Map.Map String ExprType | r } -> TcoExpr -> Boolean
isClosureNode helpersRef exprOriginal = 
  let expr = stripNestedTyped exprOriginal
  in case extractExprFuncType (getExprType expr) of`;

if (content.includes(oldReplacement)) {
  content = content.replace(oldReplacement, newReplacement);
  fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
  console.log("Success");
} else {
  console.log("Failed to find replacement string");
}
