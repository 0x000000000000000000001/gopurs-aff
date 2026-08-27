const fs = require('fs');
let content = fs.readFileSync('../gopurs/src/Gopurs/CodeGen.purs', 'utf8');

const oldReplacement = `translateExprImpl_ :: Ref { decls :: Array GoDecl, rawDecls :: Array String, elidedCtors :: Set.Set String, ctorTypes :: Map String { vars :: Array String, fields :: Array ExprType }, pointerAdtPaths :: Map String { ctorName :: String, arity :: Int }, pointerAdtNodes :: Set String, pointerAdtLeaves :: Map String { nodeBaseStruct :: String, nodeCtor :: String }, enumAdts :: Set.Set String, enumCtors :: Set.Set String, globalTypes :: Map.Map String ExprType, classDeclsFields :: Map String { vars :: Array String, fields :: Array { name :: String, "type" :: ExprType } }, globalId :: Int } -> Int -> String -> Array String -> Map String { fullName :: String, fArgs :: Array GoType, fRet :: GoType, arity :: Int } -> Map String { name :: String, goType :: GoType } -> Maybe String -> Array { ident :: String, params :: Array String, loopParams :: Array String, goTypes :: Array GoType } -> Boolean -> Boolean -> Int -> TcoExpr -> { stmts :: StmtTree, expr :: GoExpr, exprType :: GoType, nextId :: Int }
translateExprImpl_ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock nextId tcoExpr =
  translateExprImpl__ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock Nothing nextId tcoExpr`;

const newReplacement = `translateExprImpl_ :: Ref { decls :: Array GoDecl, rawDecls :: Array String, elidedCtors :: Set.Set String, ctorTypes :: Map String { vars :: Array String, fields :: Array ExprType }, pointerAdtPaths :: Map String { ctorName :: String, arity :: Int }, pointerAdtNodes :: Set String, pointerAdtLeaves :: Map String { nodeBaseStruct :: String, nodeCtor :: String }, enumAdts :: Set.Set String, enumCtors :: Set.Set String, globalTypes :: Map.Map String ExprType, classDeclsFields :: Map String { vars :: Array String, fields :: Array { name :: String, "type" :: ExprType } }, globalId :: Int } -> Int -> String -> Array String -> Map String { fullName :: String, fArgs :: Array GoType, fRet :: GoType, arity :: Int } -> Map String { name :: String, goType :: GoType } -> Maybe String -> Array { ident :: String, params :: Array String, loopParams :: Array String, goTypes :: Array GoType } -> Boolean -> Boolean -> Int -> TcoExpr -> { stmts :: StmtTree, expr :: GoExpr, exprType :: GoType, nextId :: Int }
translateExprImpl_ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock nextId tcoExprOriginal =
  let tcoExpr = stripNestedTyped tcoExprOriginal
  in translateExprImpl__ helpersRef depth modNameStr recVars moduleArities bound tcoIdent loopCtx isTail inEffectBlock Nothing nextId tcoExpr`;

if (content.includes(oldReplacement)) {
  content = content.replace(oldReplacement, newReplacement);
  fs.writeFileSync('../gopurs/src/Gopurs/CodeGen.purs', content);
  console.log("Success");
} else {
  console.log("Failed to find replacement string");
}
