import sys

with open("output/Effect/Effect_ffi.go", "r") as f:
    code = f.read()

code = code.replace('import "gopurs/output/gopurs_runtime"\n\t"fmt"\n\t"gopurs/output/gopurs_runtime"\n)\n', 'import (\n\t"gopurs/output/gopurs_runtime"\n\t"fmt"\n)\n')

with open("output/Effect/Effect_ffi.go", "w") as f:
    f.write(code)
