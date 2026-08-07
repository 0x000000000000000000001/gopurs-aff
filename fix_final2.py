import sys
with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace('import (\n\t"fmt"\n', 'import (\n')
import re
content = re.sub(r'type Supervisor struct \{\n\tCtx    context\.Context\n\tCancel context\.CancelCauseFunc\n\tWg     \*sync\.WaitGroup\n\}\n', '', content, count=1)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
