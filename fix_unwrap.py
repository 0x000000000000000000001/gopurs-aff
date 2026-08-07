import sys
import re

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

def unwrap_closure(func_name, code):
    pattern = r'(func ' + func_name + r'\b\s*\([^\)]*\)\s*any\s*\{\n)\treturn func\(_ any\) any \{\n(.*?\t)\}\n\}'
    def repl(m):
        header = m.group(1)
        body = m.group(2)
        # Dedent body
        dedented_body = "\n".join(line[1:] if line.startswith("\t") else line for line in body.split("\n"))
        return header + dedented_body + "}"
    return re.sub(pattern, repl, code, flags=re.DOTALL)

for fn in ["_MakeFiberNative", "_KillFiber", "_JoinFiber", "_OnCompleteFiber", "_RunFiber", "_IsSuspendedFiber"]:
    code = unwrap_closure(fn, code)

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
