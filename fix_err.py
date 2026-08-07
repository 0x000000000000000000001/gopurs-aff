import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace("return nil, ctx.Err()", "return nil, context.Cause(ctx)")
content = content.replace("if ctx.Err() != nil && context.Cause(ctx) == err", "if context.Cause(ctx) != nil && context.Cause(ctx) == err")
content = content.replace("if ctx.Err() != nil && context.Cause(ctx) == useErr", "if context.Cause(ctx) != nil && context.Cause(ctx) == useErr")

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)

