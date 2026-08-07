import sys

with open("output/Effect/Effect_ffi.go", "r") as f:
    content = f.read()

content = content.replace('''func BindE(a func(interface{}) any, f func(any) func(interface{}) any, _ interface{}) any {
	return func(_ interface{}) any {
		resA := a(nil)
		return f(resA)(nil)
	}
}''', '''func BindE(a func(interface{}) any, f func(any) func(interface{}) any, _ interface{}) any {
	resA := a(nil)
	return f(resA)(nil)
}''')

with open("output/Effect/Effect_ffi.go", "w") as f:
    f.write(content)
