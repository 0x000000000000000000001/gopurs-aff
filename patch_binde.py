import sys
with open("output/Effect/Effect_ffi.go", "r") as f:
    content = f.read()

content = content.replace('gopurs_runtime.Func3(func(arg0 gopurs_runtime.Value, arg1 gopurs_runtime.Value, arg2 gopurs_runtime.Value) gopurs_runtime.Value {', '''gopurs_runtime.Func3(func(arg0 gopurs_runtime.Value, arg1 gopurs_runtime.Value, arg2 gopurs_runtime.Value) gopurs_runtime.Value {
	fmt.Printf("_Gopurs_BindE called with arg0=%+v\\n", arg0)
''')

content = content.replace('"gopurs/output/gopurs_runtime"', '"gopurs/output/gopurs_runtime"\n\t"fmt"')

with open("output/Effect/Effect_ffi.go", "w") as f:
    f.write(content)
