import re

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

pattern = r'(func _KillFiber.*?)\n\tnf\.Cancel\(\)'

def repl(m):
    return m.group(1) + "\n\tif ks, ok := nf.Ctx.Value(killErrKey).(*KillState); ok {\n\t\tks.Err = errAny\n\t}\n\tnf.Cancel()"

code = re.sub(pattern, repl, code, flags=re.DOTALL)

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
