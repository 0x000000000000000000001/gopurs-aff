import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

import re
content = re.sub(r'supAny := ctx\.Value\(supervisorKey\)\n\t\tif supAny != nil \{\n\t\t\tsup := supAny\.\(\*Supervisor\)\n\t\t\tsup\.Wg\.Add\(1\)', 'if supAny != nil {\n\t\t\tsup := supAny.(*Supervisor)\n\t\t\tsup.Wg.Add(1)', content)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
