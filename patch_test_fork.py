import sys

with open("test/Test/Main.purs", "r") as f:
    content = f.read()

old_test_fork = """test_fork :: Aff Unit
test_fork = assert "fork" do
  ref <- newRef ""
  _ <- forkAff do
    delay (Milliseconds 10.0)
    modifyRef ref (_ <> "child")
  _ <- modifyRef ref (_ <> "go")
  delay (Milliseconds 20.0)
  _ <- modifyRef ref (_ <> "parent")
  eq "gochildparent" <$> readRef ref"""

new_test_fork = """test_fork :: Aff Unit
test_fork = assert "fork" do
  ref <- newRef ""
  _ <- forkAff do
    delay (Milliseconds 10.0)
    modifyRef ref (_ <> "child")
  _ <- modifyRef ref (_ <> "go")
  delay (Milliseconds 20.0)
  _ <- modifyRef ref (_ <> "parent")
  val <- readRef ref
  liftEffect $ Console.log ("fork value: " <> val)
  pure (val == "gochildparent")"""

content = content.replace(old_test_fork, new_test_fork)

with open("test/Test/Main.purs", "w") as f:
    f.write(content)
