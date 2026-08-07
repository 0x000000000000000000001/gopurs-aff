import sys

with open("output/Effect.Aff/Effect_Aff_ffi.go", "r") as f:
    content = f.read()

old_func = """func _IsSuspendedFiber(nf *NativeFiber) bool {
	return false
}"""

new_func = """func _IsSuspendedFiber(nf *NativeFiber) func(any) any {
	return func(any) any {
		return false
	}
}"""

content = content.replace(old_func, new_func)

with open("output/Effect.Aff/Effect_Aff_ffi.go", "w") as f:
    f.write(content)
