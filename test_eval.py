import sys
with open("output/Effect/Effect_ffi.go", "r") as f:
    content = f.read()

content = content.replace('func BindE(a func(interface{}) any, f func(any) func(interface{}) any, _ interface{}) any {\n\tprintln("BindE OUTSIDE executed!")\n\treturn func(_ interface{}) any {\n\t\tprintln("BindE executed!")', 'func BindE(a func(interface{}) any, f func(any) func(interface{}) any, _ interface{}) any {\n\treturn func(_ interface{}) any {\n\t\tfmt.Printf("BindE executed! a=%v\\n", a)')

with open("output/Effect/Effect_ffi.go", "w") as f:
    f.write(content)
