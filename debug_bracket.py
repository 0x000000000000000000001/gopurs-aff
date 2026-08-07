import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

import re
content = re.sub(r'handler = gopurs_runtime\.Unbox\[func\(any\) any\]\(gopurs_runtime\.Apply2\(killedVal, gopurs_runtime\.Box\(err\), resourceBox\)\)', 'fmt.Printf("killedVal Type: %v\\n", killedVal.Type)\n\t\t\t\t\n\t\t\t\thandler = gopurs_runtime.Unbox[func(any) any](gopurs_runtime.Apply2(killedVal, gopurs_runtime.Box(err), resourceBox))', content)

content = 'import "fmt"\n' + content

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)

