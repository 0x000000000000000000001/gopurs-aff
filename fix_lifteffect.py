import sys

with open("output/Effect.Aff/Effect_Aff_ffi.go", "r") as f:
    content = f.read()

# Remove all declarations of _Gopurs__LiftEffect
start_str = 'var _Gopurs__LiftEffect = '
while start_str in content:
    start_idx = content.find(start_str)
    end_idx = content.find('})\n', start_idx) + 3
    content = content[:start_idx] + content[end_idx:]

# Insert the correct one before _Gopurs__ThrowError
new_decl = """var _Gopurs__LiftEffect = // TAST: (Func [(ADT ["Effect","Effect"] [(TypeVar a)])] (ADT ["Effect","Aff","Aff"] [(TypeVar a)]))
gopurs_runtime.Func(func(arg0 gopurs_runtime.Value) gopurs_runtime.Value {
	if arg0.Type == 11 { panic("BOOLEAN PASSED TO _LiftEffect!!") }
	go_arg0 := func(p0_0 any) any {
			return gopurs_runtime.Apply(arg0, gopurs_runtime.Box(p0_0))
		}
	go_res := _LiftEffect(go_arg0)
	return gopurs_runtime.Box(go_res)
})
var _Gopurs__ThrowError = """
content = content.replace("var _Gopurs__ThrowError = ", new_decl)

with open("output/Effect.Aff/Effect_Aff_ffi.go", "w") as f:
    f.write(content)
