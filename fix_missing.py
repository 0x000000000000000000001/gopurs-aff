import sys
with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

helper = """
type key int
const killErrKey key = 0
const supervisorKey key = 1
type KillState struct {
	Err error
}

func getKillError(ctx context.Context, defaultErr error) error {
	if ks, ok := ctx.Value(killErrKey).(*KillState); ok && ks.Err != nil {
		return ks.Err
	}
	return defaultErr
}
"""

if "KillState" not in content:
    content = content.replace("type NativeFiber struct {", helper + "\ntype NativeFiber struct {")
else:
    content = content.replace("const killErrKey key = 0", "const killErrKey key = 0\nconst supervisorKey key = 1")

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
