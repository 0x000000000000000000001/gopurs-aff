import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace('fmt redeclared in this block', '') # just a placeholder, I'll fix it properly
content = content.replace('import (\n\t"fmt"\n\n\t"fmt"', 'import (\n\t"fmt"')

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
