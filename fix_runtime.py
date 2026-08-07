import sys

with open("output/gopurs_runtime/runtime.go", "r") as f:
    content = f.read()

import re
content = re.sub(r'panic\("Attempted to apply a non-function"\)', 'panic(fmt.Sprintf("Attempted to apply a non-function: type=%d", f.Type))', content)
if 'import "fmt"' not in content:
    content = 'import "fmt"\n' + content

with open("output/gopurs_runtime/runtime.go", "w") as f:
    f.write(content)
