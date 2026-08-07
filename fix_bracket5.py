import re

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

# Fix killErrKey
pattern_kill = r'\n\tif ks, ok := nf\.Ctx\.Value\(killErrKey\)\.\(\*KillState\); ok \{\n\t\tks\.Err = errAny\n\t\}'
code = re.sub(pattern_kill, '', code)

# Fix resourceBox
pattern_box = r'useFnAff := gopurs_runtime\.Unbox\[AffFn\]\(gopurs_runtime\.Apply\(useVal, resourceBox\)\)'
replacement_box = 'useFnAff := gopurs_runtime.Unbox[AffFn](gopurs_runtime.Apply(useVal, resourceBox.(gopurs_runtime.Value)))'
code = code.replace(pattern_box, replacement_box)

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
