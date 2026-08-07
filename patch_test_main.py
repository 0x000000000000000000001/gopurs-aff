import sys

with open("test/Test/Main.purs", "r") as f:
    content = f.read()

old_code = """      res <- readRef ref
      pure (res ==
        [ "foo/bar"
        , "foo/run"
        , "foo/release/foo/run"
        , "foo/bar"
        , "foo/kill/z"
        ])"""

new_code = """      res <- readRef ref
      liftEffect $ Console.log ("res=" <> show res)
      pure (res ==
        [ "foo/bar"
        , "foo/run"
        , "foo/release/foo/run"
        , "foo/bar"
        , "foo/kill/z"
        ])"""

content = content.replace(old_code, new_code)

with open("test/Test/Main.purs", "w") as f:
    f.write(content)
