const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

const oldReplacement = `translateExprImpl_ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock nextId tcoExpr =
  let
    stripNested (TcoExpr pos (Typed outer (TcoExpr innerPos (Typed inner e)))) =
      case extractExprFuncType outer, extractExprFuncType inner of
        Just _, Nothing -> stripNested (TcoExpr pos (Typed outer e))
        Nothing, Just _ -> stripNested (TcoExpr pos (Typed inner e))
        _, _ -> TcoExpr pos (Typed outer (stripNested (TcoExpr innerPos (Typed inner e))))
    stripNested (TcoExpr pos (Typed ty e)) = TcoExpr pos (Typed ty (stripNested e))
    stripNested e = e
  in
    translateExprImpl__ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock Nothing nextId (stripNested tcoExpr)`;

const newReplacement = `translateExprImpl_ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock nextId tcoExpr =
  let
    stripNested (TcoExpr pos (Typed outer (TcoExpr innerPos (Typed inner e)))) =
      case unwrapTcoExpr e of
        App _ _ -> stripNested (TcoExpr pos (Typed outer e))
        _ -> TcoExpr pos (Typed outer (stripNested (TcoExpr innerPos (Typed inner e))))
    stripNested (TcoExpr pos (Typed ty e)) = TcoExpr pos (Typed ty (stripNested e))
    stripNested e = e
  in
    translateExprImpl__ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock Nothing nextId (stripNested tcoExpr)`;

if (content.includes(oldReplacement)) {
  content = content.replace(oldReplacement, newReplacement);
  fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
  console.log("Success");
} else {
  console.log("Failed to find replacement string");
}
