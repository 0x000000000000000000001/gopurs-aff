import sys
with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace('import (\n\t"fmt"\n\timport_atomic "sync/atomic"', 'import (\n\timport_atomic "sync/atomic"')
content = content.replace('type NativeFiber struct {', """type key int
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

type NativeFiber struct {""")
content = content.replace('ctx, cancel := context.WithCancel(context.Background())', 'ctx, cancel := context.WithCancelCause(context.Background())')

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
