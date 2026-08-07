import re

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

pattern = r'''(func _KillFiber.*?<-nf\.Done\n\t\t\n\t\t)if nf\.Err != nil \{\n\t\t\tonError\(nf\.Err\)\(nil\)\n\t\t\} else \{\n\t\t\tonSuccess\(nf\.Val\)\(nil\)\n\t\t\}(.*?)'''

def repl(m):
    return m.group(1) + "onSuccess(nil)(nil)" + m.group(2)

code = re.sub(pattern, repl, code, flags=re.DOTALL)

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
