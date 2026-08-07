import re

def add_closure(func_name, code):
    # Find the function signature and the entire body until the final closing brace
    # Be careful with nested braces!
    pattern = r'(func ' + func_name + r'\b\s*\([^\)]*\)\s*any\s*\{)(.*?)^\}'
    def repl(m):
        header = m.group(1)
        body = m.group(2)
        # Indent body
        indented_body = "\n".join("\t" + line if line else line for line in body.split("\n"))
        return header + "\n\treturn func(_ any) any {" + indented_body + "}\n}"
    return re.sub(pattern, repl, code, flags=re.MULTILINE|re.DOTALL)

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

for fn in ["_MakeFiberNative", "_KillFiber", "_JoinFiber", "_OnCompleteFiber", "_RunFiber", "_IsSuspendedFiber"]:
    code = add_closure(fn, code)

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
