import sys
with open("output/Effect/Effect_ffi.go", "r") as f:
    content = f.read()

content = content.replace('func BindE(a func(interface{}) any, f func(any) func(interface{}) any, _ interface{}) any {\n\treturn func(_ interface{}) any {\n\t\tfmt.Printf("BindE executed! a=%v\\n", a)\n\t\tresA := a(nil)\n\t\treturn f(resA)(nil)\n\t}', 'func BindE(a func(interface{}) any, f func(any) func(interface{}) any, _ interface{}) any {\n\tresA := a(nil)\n\treturn f(resA)(nil)\n}')

with open("output/Effect/Effect_ffi.go", "w") as f:
    f.write(content)
