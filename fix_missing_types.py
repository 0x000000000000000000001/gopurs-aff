import sys
with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

types_to_add = """type key int
const killErrKey key = 0
const supervisorKey key = 1
type KillState struct {
	Err error
}

type Supervisor struct {
	Ctx    context.Context
	Cancel context.CancelCauseFunc
	Wg     *sync.WaitGroup
}
"""

if "type key int" not in content:
    content = content.replace("type NativeFiber struct {", types_to_add + "\ntype NativeFiber struct {")

if "context.WithCancel(context.Background())" in content:
    content = content.replace("context.WithCancel(context.Background())", "context.WithCancelCause(context.Background())")

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
