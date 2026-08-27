const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

const oldReplacement = `translateExprImpl_ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock nextId tcoExpr =
  translateExprImpl__ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock Nothing nextId tcoExpr`;

const newReplacement = `translateExprImpl_ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock nextId tcoExpr =
  let
    stripNested (TcoExpr pos (Typed outer (TcoExpr _ (Typed _ inner)))) = stripNested (TcoExpr pos (Typed outer inner))
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
