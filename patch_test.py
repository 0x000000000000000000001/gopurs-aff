import sys

with open("test/Test/Main.purs", "r") as f:
    content = f.read()

content = content.replace('  pure (isLeft r1 && isLeft r2 && isRight r3 && r4 == "foofoo/kill/zbarbar/throw/bbazcbaz/release/c")',
                          '  liftEffect $ Console.log ("r4 was: " <> r4)\n  pure (isLeft r1 && isLeft r2 && isRight r3 && r4 == "foofoo/kill/zbarbar/throw/bbazcbaz/release/c")')

with open("test/Test/Main.purs", "w") as f:
    f.write(content)
