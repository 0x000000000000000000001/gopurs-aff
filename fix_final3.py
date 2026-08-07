import sys
with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace('import_atomic "sync/atomic"\\n\\n', '')
content = content.replace('import_atomic "sync/atomic"\n\n', '')
content = content.replace('import (\n\t"context"', 'import (\n\timport_atomic "sync/atomic"\n\t"context"')
content = content.replace('\t"fmt"\n', '')

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
