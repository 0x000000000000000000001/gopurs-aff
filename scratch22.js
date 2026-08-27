const fs = require('fs');
let content = fs.readFileSync('../purescript-backend-optimizer/src/PureScript/Backend/Optimizer/Convert.purs', 'utf8');

// Insert a log in toBackendBinding to print the BackendExpr for 'never'
let replacement = `toBackendBinding :: Binding Ann -> ConvertM (Tuple Ident BackendExpr)
toBackendBinding (Binding _ ident expr) = Tuple ident <$> toBackendExpr expr`;

let newReplacement = `toBackendBinding :: Binding Ann -> ConvertM (Tuple Ident BackendExpr)
toBackendBinding (Binding _ ident expr) = do
  res <- toBackendExpr expr
  when (ident == Ident "never") $ do
    unsafePerformEffect (Effect.Class.Console.log ("NEVER BACKEND AST: " <> show res))
  pure $ Tuple ident res`;

if (content.includes(replacement)) {
  content = content.replace(replacement, newReplacement);
  // Also add imports for Effect and Console
  content = "import Effect.Unsafe (unsafePerformEffect)\nimport Effect.Class.Console as Effect.Class.Console\n" + content;
  fs.writeFileSync('../purescript-backend-optimizer/src/PureScript/Backend/Optimizer/Convert.purs', content);
  console.log("Success");
} else {
  console.log("Failed");
}
