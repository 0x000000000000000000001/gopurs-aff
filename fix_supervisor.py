import sys
with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

helper = """
type Supervisor struct {
	Ctx    context.Context
	Cancel context.CancelCauseFunc
	Wg     *sync.WaitGroup
}
"""

if "type Supervisor struct" not in content:
    content = content.replace("type NativeFiber struct", helper + "\ntype NativeFiber struct")

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
