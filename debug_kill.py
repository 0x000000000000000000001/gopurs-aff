import re

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

getKillError_old = """func getKillError(ctx context.Context, defaultErr error) error {
	if ks, ok := ctx.Value(killErrKey).(*KillState); ok && ks.Err != nil {
		return ks.Err
	}
	return defaultErr
}"""

getKillError_new = """func getKillError(ctx context.Context, defaultErr error) error {
	if ks, ok := ctx.Value(killErrKey).(*KillState); ok {
		if ks.Err != nil {
			return ks.Err
		}
		fmt.Println("getKillError: ks.Err is nil!")
	} else {
		fmt.Println("getKillError: no KillState found!")
	}
	return defaultErr
}"""

killFiber_old = """	if ks, ok := nf.Ctx.Value(killErrKey).(*KillState); ok {
		ks.Err = errAny
	}"""

killFiber_new = """	if ks, ok := nf.Ctx.Value(killErrKey).(*KillState); ok {
		ks.Err = errAny
		fmt.Println("_KillFiber: set ks.Err successfully")
	} else {
		fmt.Println("_KillFiber: no KillState found on nf.Ctx!")
	}"""

content = content.replace("import (\\n\\t\"context\"", "import (\\n\\t\"context\"\\n\\t\"fmt\"")
content = content.replace(getKillError_old, getKillError_new)
content = content.replace(killFiber_old, killFiber_new)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
