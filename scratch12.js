const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

const oldReplacement = `    App _ _ ->
      let Tuple flatFn flatArgs = flattenApp expr
          expectedArity = getArityFromType (getExprType flatFn)
          actualArity = Array.length flatArgs
      in case unwrapTcoExpr flatFn of`;

const newReplacement = `    App _ _ ->
      let Tuple flatFn flatArgs = flattenApp expr
          expectedArity = getArityFromType (getExprType flatFn)
          actualArity = Array.length flatArgs
          _ = unsafePerformEffect $ Debug.trace ("isClosureNode flatFn expectedArity=" <> show expectedArity <> " actualArity=" <> show actualArity <> " flatFnType=" <> printExprType (getExprType flatFn)) \\_ -> pure unit
      in case unwrapTcoExpr flatFn of`;

if (content.includes(oldReplacement)) {
  content = content.replace(oldReplacement, newReplacement);
  fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
  console.log("Success");
} else {
  console.log("Failed to find replacement string");
}
