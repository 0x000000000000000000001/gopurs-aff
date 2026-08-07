import sys
with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace('import (\n\timport_atomic "sync/atomic"\n', 'import (\n\t"fmt"\n\timport_atomic "sync/atomic"\n')
content = content.replace('const killErrKey key = 0', 'const killErrKey key = 0\nconst supervisorKey key = 1\n')

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
