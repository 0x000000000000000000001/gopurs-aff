import re

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

pattern = r'func GeneralBracket\(acquireBox any, optionsBox any, useBox any\) any \{.*?return resultVal, nil\n\t\}\n\}'

replacement = """func GeneralBracket(acquireBox any, optionsBox any, useBox any) any {
	return func(ctx context.Context) (any, error) {
		acquireVal := acquireBox.(gopurs_runtime.Value)
		acquireFn := gopurs_runtime.Unbox[AffFn](acquireVal)
		
		resourceBox, err := runAffSync(acquireFn, ctx)
		if err != nil {
			return nil, err
		}
		
		optionsVal := optionsBox.(gopurs_runtime.Value)
		killedBox := gopurs_runtime.Unbox[func(any) func(any) any](gopurs_runtime.Apply(optionsVal, gopurs_runtime.Box("killed")))
		failedBox := gopurs_runtime.Unbox[func(any) func(any) any](gopurs_runtime.Apply(optionsVal, gopurs_runtime.Box("failed")))
		completedBox := gopurs_runtime.Unbox[func(any) func(any) any](gopurs_runtime.Apply(optionsVal, gopurs_runtime.Box("completed")))
		
		useVal := useBox.(gopurs_runtime.Value)
		useFnAff := gopurs_runtime.Unbox[AffFn](gopurs_runtime.Apply(useVal, resourceBox))
		
		resultVal, useErr := runAffSync(useFnAff, ctx)
		
		if useErr != nil {
			var cleanupBox any
			if ctx.Err() != nil && context.Cause(ctx) == useErr {
				errBox := gopurs_runtime.Box(useErr)
				cleanupBox = killedBox(errBox)(resourceBox)
			} else {
				errBox := gopurs_runtime.Box(useErr)
				cleanupBox = failedBox(errBox)(resourceBox)
			}
			cleanupFn := gopurs_runtime.Unbox[AffFn](cleanupBox)
			cleanupCtx := context.Background()
			_, _ = runAffSync(cleanupFn, cleanupCtx)
			return nil, useErr
		} else {
			cleanupBox := completedBox(resultVal)(resourceBox)
			cleanupFn := gopurs_runtime.Unbox[AffFn](cleanupBox)
			_, cleanupErr := runAffSync(cleanupFn, ctx)
			if cleanupErr != nil {
				return nil, cleanupErr
			}
			return resultVal, nil
		}
	}
}"""

code = re.sub(pattern, replacement, code, flags=re.DOTALL)

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
