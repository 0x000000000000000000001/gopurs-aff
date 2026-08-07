import sys

with open("output/Effect.Aff/Effect_Aff_ffi.go", "r") as f:
    content = f.read()

old_func = """func _LiftEffect(effect func(any) any) AffFn {"""

new_func = """func _LiftEffect(effect func(any) any) AffFn {
	return func(_ context.Context) (any, error) {
		return effect(nil), nil
	}
}"""

# Wait, _LiftEffect is:
# func _LiftEffect(effect func(any) any) AffFn {
# 	return func(_ context.Context) (any, error) {
# 		return effect(nil), nil
# 	}
# }
# So we want to patch _Gopurs__LiftEffect!

old_gopurs = """var _Gopurs__LiftEffect = // TAST: (Func [(ADT ["Effect","Effect"] [(TypeVar a)])] (ADT ["Effect","Aff","Aff"] [(TypeVar a)]))
gopurs_runtime.Func(func(arg0 gopurs_runtime.Value) gopurs_runtime.Value {
	go_arg0 := func(p0_0 any) any {
			return gopurs_runtime.Apply(arg0, gopurs_runtime.Box(p0_0))
		}
	go_res := _LiftEffect(go_arg0)
	return gopurs_runtime.Box(go_res)
})"""

new_gopurs = """var _Gopurs__LiftEffect = // TAST: (Func [(ADT ["Effect","Effect"] [(TypeVar a)])] (ADT ["Effect","Aff","Aff"] [(TypeVar a)]))
gopurs_runtime.Func(func(arg0 gopurs_runtime.Value) gopurs_runtime.Value {
	if arg0.Type != gopurs_runtime.TypeFunc && arg0.Type != gopurs_runtime.TypeFunc2 && arg0.Type != gopurs_runtime.TypeFunc3 {
		panic("LIFTEFFECT RECEIVED NON-FUNC TYPE!")
	}
	go_arg0 := func(p0_0 any) any {
			return gopurs_runtime.Apply(arg0, gopurs_runtime.Box(p0_0))
		}
	go_res := _LiftEffect(go_arg0)
	return gopurs_runtime.Box(go_res)
})"""

content = content.replace(old_gopurs, new_gopurs)

with open("output/Effect.Aff/Effect_Aff_ffi.go", "w") as f:
    f.write(content)
