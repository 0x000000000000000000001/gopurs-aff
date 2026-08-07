import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

import re
content = re.sub(r'"supervisor": sup,\n\t\t\t"fiber":      nf,', '"supervisor": gopurs_runtime.Box(sup),\n\t\t\t"fiber":      gopurs_runtime.Box(nf),', content)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
