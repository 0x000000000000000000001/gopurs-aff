import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

import re
content = re.sub(r'supAny := ctx\.Value\(supervisorKey\)\n\t\tif supAny != nil \{\n\t\t\tsup := gopurs_runtime\.Unbox\[\*Supervisor\]\(supAny\.\(gopurs_runtime\.Value\)\)', 'supAny := ctx.Value(supervisorKey)\n\t\tif supAny != nil {\n\t\t\tsup := supAny.(*Supervisor)', content)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
