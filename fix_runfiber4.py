import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

import re
content = re.sub(r'func _RunFiber\(nf_ any\) any \{\n\tnf := nf_\.\(\*NativeFiber\)', 'func _RunFiber(nf_ any) any {\n\tnf := gopurs_runtime.Unbox[*NativeFiber](nf_.(gopurs_runtime.Value))', content)
content = re.sub(r'func _ForkAffNative\(aff_ any\) any \{\n\taff := gopurs_runtime\.Unbox\[AffFn\]\(aff_\)', 'func _ForkAffNative(aff_ any) any {\n\taff := gopurs_runtime.Unbox[AffFn](aff_.(gopurs_runtime.Value))', content)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
