import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace('println("_ForkAffNative executed")\n\t\t//debug.PrintStack()', 'println("_ForkAffNative executed")\n\t\tdebug.PrintStack()')
content = content.replace('import (\n\t"context"', 'import (\n\t"context"\n\t"runtime/debug"')

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
