import re

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

# Add getKillError function
helper = """
func getKillError(ctx context.Context, defaultErr error) error {
	if ks, ok := ctx.Value(killErrKey).(*KillState); ok && ks.Err != nil {
		return ks.Err
	}
	return defaultErr
}
"""
content = content.replace("type NativeFiber struct {", helper + "\ntype NativeFiber struct {")

# Replace ctx.Err() with getKillError(ctx, ctx.Err())
content = content.replace("return nil, ctx.Err()", "return nil, getKillError(ctx, ctx.Err())")
content = content.replace('canceler(fmt.Errorf("context canceled"))', 'canceler(getKillError(ctx, fmt.Errorf("context canceled")))')

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
