const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

const oldReplacement = `    App _ _ ->
      let Tuple flatFn flatArgs = flattenApp expr
          expectedArity = getArityFromType (getExprType flatFn)
          actualArity = Array.length flatArgs
      in actualArity < expectedArity`;

const newReplacement = `    App _ _ ->
      let Tuple flatFn flatArgs = flattenApp expr
          expectedArity = getArityFromType (getExprType flatFn)
          actualArity = Array.length flatArgs
      in case unwrapTcoExpr flatFn of
           Var (Qualified mbMn (Ident i)) ->
             let
               h = unsafePerformEffect (Ref.read helpersRef)
               vType = case mbMn of
                 Just mn -> Map.lookup (unwrap mn <> "." <> i) h.globalTypes
                 Nothing -> Nothing
               
               expectedArity2 = case vType of
                 Just t -> getArityFromType t
                 Nothing -> 0
             in actualArity < expectedArity2
           _ -> actualArity < expectedArity`;

if (content.includes(oldReplacement)) {
  content = content.replace(oldReplacement, newReplacement);
  fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
  console.log("Success");
} else {
  console.log("Failed to find replacement string");
}
