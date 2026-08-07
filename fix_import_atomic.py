import sys
with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace('import_atomic "sync/atomic"', '')
content = content.replace('import (', 'import (\n\timport_atomic "sync/atomic"\n')

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
