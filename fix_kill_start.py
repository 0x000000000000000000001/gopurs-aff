import re

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

pattern = r'(func _KillFiber.*?nf\.Cancel\(\)\n)(.*?go func\(\) \{)'

def repl(m):
    return m.group(1) + "\tselect {\n\tcase <-nf.Start:\n\tdefault:\n\t\tclose(nf.Start)\n\t}\n" + m.group(2)

code = re.sub(pattern, repl, code, flags=re.DOTALL)

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
