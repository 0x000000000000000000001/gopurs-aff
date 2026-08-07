import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

import re
content = re.sub(r'sup := supAny\.\(\*Supervisor\)', 'sup := gopurs_runtime.Unbox[*Supervisor](supAny.(gopurs_runtime.Value))', content)
content = re.sub(r'cb := cbAny\.\(func\(any\) any\)', 'cb := gopurs_runtime.Unbox[func(any) any](cbAny.(gopurs_runtime.Value))', content)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
