import sys

with open("test/Test/Main.purs", "r") as f:
    content = f.read()

content = content.replace('  pure (r1 == "done" && r2 == "acquiredonerelease")',
                          '  liftEffect $ Console.log ("r1 was: " <> r1 <> ", r2 was: " <> r2)\n  pure (r1 == "done" && r2 == "acquiredonerelease")')

with open("test/Test/Main.purs", "w") as f:
    f.write(content)
