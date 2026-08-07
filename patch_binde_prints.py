import sys

with open("output/Effect/Effect_ffi.go", "r") as f:
    code = f.read()

code = code.replace('''func BindE(a func(interface{}) any, f func(any) func(interface{}) any, _ interface{}) any {
	resA := a(nil)
	return f(resA)(nil)
}''', '''func BindE(a func(interface{}) any, f func(any) func(interface{}) any, _ interface{}) any {
	fmt.Println("BindE executed!")
	resA := a(nil)
	return f(resA)(nil)
}''')
code = code.replace('"gopurs/output/gopurs_runtime"', '"gopurs/output/gopurs_runtime"\n\t"fmt"')

with open("output/Effect/Effect_ffi.go", "w") as f:
    f.write(code)
