import sys

with open("test/Test/Main.purs", "r") as f:
    content = f.read()

replacement = """test_kill_bracket_nested = assert "kill/bracket/nested" do
  ref <- newRef []
  let
    action s = do
      delay (Milliseconds 10.0)
      _ <- modifyRef ref (_ <> [ s ])
      pure s
    bracketAction s =
      bracket
        (action (s <> "/bar"))
        (\s' -> void $ action (s' <> "/release"))
        (\s' -> action (s' <> "/run"))
  fiber <-
    forkAff $ bracket
      (bracketAction "foo")
      (\s -> void $ bracketAction (s <> "/release"))
      (\s -> bracketAction (s <> "/run"))
  delay (Milliseconds 5.0)
  killFiber (error "Nope") fiber
  _ <- try (joinFiber fiber)
  res <- readRef ref
  liftEffect $ Console.log ("kill/bracket/nested output: " <> show res)
  pure (res ==
    [ "foo/bar"
    , "foo/bar/run"
    , "foo/bar/release"
    , "foo/bar/run/release/bar"
    , "foo/bar/run/release/bar/run"
    , "foo/bar/run/release/bar/release"
    ])"""

import re
content = re.sub(r'test_kill_bracket_nested = assert "kill/bracket/nested" do\n.*?,\ "foo/bar/run/release/bar/release"\n    \]', replacement, content, flags=re.DOTALL)

with open("test/Test/Main.purs", "w") as f:
    f.write(content)
