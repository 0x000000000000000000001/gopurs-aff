import sys

with open("output/Effect.Aff/Effect_Aff_ffi.go", "r") as f:
    code = f.read()

code = code.replace('''		if ctx.Err() != nil {
			killedBox := gopurs_runtime.RecordGet(optionsVal, "killed")''', '''		if ctx.Err() != nil {
			fmt.Printf("GeneralBracket: ctx.Err() != nil. Cause: %v\\n", context.Cause(ctx))
			killedBox := gopurs_runtime.RecordGet(optionsVal, "killed")''')

with open("output/Effect.Aff/Effect_Aff_ffi.go", "w") as f:
    f.write(code)
