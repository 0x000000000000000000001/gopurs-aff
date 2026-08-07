import sys
with open("output/Effect.Aff/Effect_Aff_ffi.go", "r") as f:
    content = f.read()

content = content.replace('''func _IsSuspendedFiber(nf *NativeFiber) any {
	return false
}''', '''func _IsSuspendedFiber(nf *NativeFiber) any {
	return func(_ any) any {
		return false
	}
}''')

with open("output/Effect.Aff/Effect_Aff_ffi.go", "w") as f:
    f.write(content)
