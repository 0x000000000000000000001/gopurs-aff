with open('test/Test/Main.purs', 'r') as f:
    content = f.read()

with open('scratch.txt', 'r') as f:
    case_stmt = f.read()

target = '  pure (r1 == "foo" || r1 == "bar" || r1 == "baz")'
replacement = case_stmt + '  pure ((r1 == "foo" || r1 == "bar" || r1 == "baz") && is_valid_r2)'

new_content = content.replace(target, replacement)

with open('test/Test/Main.purs', 'w') as f:
    f.write(new_content)
