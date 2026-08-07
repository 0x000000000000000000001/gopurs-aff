import sys

with open("test/Test/Main.purs", "r") as f:
    content = f.read()

replacement = """test_kill_canceler = assert "kill/canceler" do
  ref <- newRef ""
  fiber <- forkAff do
    _ <- makeAff \_ -> pure $ Canceler \_ -> do
      delay (Milliseconds 20.0)
      liftEffect (writeRef ref "cancel")
      liftEffect $ Console.log "Canceler finished writing cancel!"
    writeRef ref "done"
  delay (Milliseconds 10.0)
  liftEffect $ Console.log "Calling killFiber"
  killFiber (error "Nope") fiber
  liftEffect $ Console.log "killFiber resolved"
  res <- try (joinFiber fiber)
  n <- readRef ref
  liftEffect $ Console.log ("kill/canceler res: " <> n <> " err: " <> show res)
  pure (n == "cancel" && (lmap message res) == Left "Nope")"""

import re
content = re.sub(r'test_kill_canceler = assert "kill/canceler" do\n.*?pure \(n == "cancel" && \(lmap message res\) == Left "Nope"\)', replacement, content, flags=re.DOTALL)

with open("test/Test/Main.purs", "w") as f:
    f.write(content)
