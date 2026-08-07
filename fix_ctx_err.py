import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace("return nil, ctx.Err()", "return nil, context.Cause(ctx)")

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
