import re

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

def strip_closure(func_name, code):
    pattern = r'(func ' + func_name + r'\b.*?\{)\s*return func\(_ any\) any \{(.*?)\t\}\n\}'
    def repl(m):
        header = m.group(1)
        body = m.group(2)
        body = body.replace("\n\t\t", "\n\t")
        return header + body + "\n}"
    return re.sub(pattern, repl, code, flags=re.DOTALL)

for fn in ["_MakeFiberNative", "_KillFiber", "_JoinFiber", "_OnCompleteFiber", "_RunFiber", "_IsSuspendedFiber"]:
    code = strip_closure(fn, code)
    
with open("src/Effect/Aff.go", "w") as f:
    f.write(code)

