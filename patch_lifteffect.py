import sys
with open("output/Effect.Aff/Effect_Aff_ffi.go", "r") as f:
    content = f.read()

content = content.replace('func _LiftEffect(effect func(any) any) any {\n\treturn func(_ any) any {\n\t\tgo func() {', 'func _LiftEffect(effect func(any) any) any {\n\tprintln("_LiftEffect called")\n\treturn func(_ any) any {\n\t\tprintln("_LiftEffect inner called")\n\t\tgo func() {')

with open("output/Effect.Aff/Effect_Aff_ffi.go", "w") as f:
    f.write(content)
