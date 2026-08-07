import re

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

# Replace all resourceBox.(gopurs_runtime.Value) with gopurs_runtime.Box(resourceBox)
code = code.replace("resourceBox.(gopurs_runtime.Value)", "gopurs_runtime.Box(resourceBox)")
code = code.replace("killedBox(errBox)(resourceBox)", "killedBox(errBox)(gopurs_runtime.Box(resourceBox))")
code = code.replace("failedBox(errBox)(resourceBox)", "failedBox(errBox)(gopurs_runtime.Box(resourceBox))")
code = code.replace("completedBox(resultVal)(resourceBox)", "completedBox(gopurs_runtime.Box(resultVal))(gopurs_runtime.Box(resourceBox))")

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
