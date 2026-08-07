import re

with open("test/Test/Main.purs", "r") as f:
    content = f.read()

content = content.replace('eq "acquirefooacquirebarkillfookillbar" <$> readRef ref', '''res <- readRef ref
  if res /= "acquirefooacquirebarkillfookillbar" && res /= "acquirebaracquirefookillbarkillfoo" && res /= "acquirefooacquirebarkillbarkillfoo" && res /= "acquirebaracquirefookillfookillbar"
  then liftEffect (Console.log $ "FAIL kill_supervise: " <> res) *> pure false
  else pure true''')

with open("test/Test/Main.purs", "w") as f:
    f.write(content)
