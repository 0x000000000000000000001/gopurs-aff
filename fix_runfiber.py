import sys
with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

if "func _RunFiber" not in code:
    runfiber = """
func _RunFiber(nf *NativeFiber, _ interface{}) any {
	select {
	case <-nf.Start:
	default:
		close(nf.Start)
	}
	return nil
}
"""
    code = code.replace("func _KillFiber", runfiber + "func _KillFiber")
    with open("src/Effect/Aff.go", "w") as f:
        f.write(code)
