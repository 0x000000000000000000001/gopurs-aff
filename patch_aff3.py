import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

old_bracket = """		acquireVal := acquireBox.(gopurs_runtime.Value)
		acquireFn := gopurs_runtime.Unbox[AffFn](acquireVal)
		
		resource, err := runAffSync(acquireFn, ctx)
		if err != nil {
			return nil, err
		}
		
		useVal := useBox.(gopurs_runtime.Value)
		useResultBox := gopurs_runtime.Apply(useVal, gopurs_runtime.Box(resource))
		useFn := gopurs_runtime.Unbox[AffFn](useResultBox)
		
		val, err := runAffSync(useFn, ctx)
		
		optionsVal := optionsBox.(gopurs_runtime.Value)
		
		if err != nil {
			// Check if it was canceled
			cause := context.Cause(ctx)
			var cleanupBox any
			if cause != nil && (err == cause || err.Error() == cause.Error()) {
				killedBox := gopurs_runtime.RecordGet(optionsVal, "killed")
				errBox := gopurs_runtime.Box(err)
				cleanupBox = gopurs_runtime.Apply2(killedBox, errBox, gopurs_runtime.Box(resource))
			} else {
				failedBox := gopurs_runtime.RecordGet(optionsVal, "failed")
				errBox := gopurs_runtime.Box(err)
				cleanupBox = gopurs_runtime.Apply2(failedBox, errBox, gopurs_runtime.Box(resource))
			}
			cleanupFn := gopurs_runtime.Unbox[AffFn](cleanupBox)
			_, _ = runAffSync(cleanupFn, ctx)
			return nil, err
		} else {
			completedBox := gopurs_runtime.RecordGet(optionsVal, "completed")
			cleanupBox := gopurs_runtime.Apply2(completedBox, gopurs_runtime.Box(val), gopurs_runtime.Box(resource))
			cleanupFn := gopurs_runtime.Unbox[AffFn](cleanupBox)
			_, _ = runAffSync(cleanupFn, ctx)
			return val, nil
		}"""

new_bracket = """		acquireVal := acquireBox.(gopurs_runtime.Value)
		acquireFn := gopurs_runtime.Unbox[AffFn](acquireVal)
		
		acquireCtx := context.WithoutCancel(ctx)
		resource, err := runAffSync(acquireFn, acquireCtx)
		if err != nil {
			return nil, err
		}
		
		useVal := useBox.(gopurs_runtime.Value)
		useResultBox := gopurs_runtime.Apply(useVal, gopurs_runtime.Box(resource))
		useFn := gopurs_runtime.Unbox[AffFn](useResultBox)
		
		val, err := runAffSync(useFn, ctx)
		
		optionsVal := optionsBox.(gopurs_runtime.Value)
		
		if err != nil {
			// Check if it was canceled
			cause := context.Cause(ctx)
			var cleanupBox any
			if cause != nil && (err == cause || err.Error() == cause.Error()) {
				killedBox := gopurs_runtime.RecordGet(optionsVal, "killed")
				errBox := gopurs_runtime.Box(err)
				cleanupBox = gopurs_runtime.Apply2(killedBox, errBox, gopurs_runtime.Box(resource))
			} else {
				failedBox := gopurs_runtime.RecordGet(optionsVal, "failed")
				errBox := gopurs_runtime.Box(err)
				cleanupBox = gopurs_runtime.Apply2(failedBox, errBox, gopurs_runtime.Box(resource))
			}
			cleanupFn := gopurs_runtime.Unbox[AffFn](cleanupBox)
			cleanupCtx := context.WithoutCancel(ctx)
			_, _ = runAffSync(cleanupFn, cleanupCtx)
			return nil, err
		} else {
			completedBox := gopurs_runtime.RecordGet(optionsVal, "completed")
			cleanupBox := gopurs_runtime.Apply2(completedBox, gopurs_runtime.Box(val), gopurs_runtime.Box(resource))
			cleanupFn := gopurs_runtime.Unbox[AffFn](cleanupBox)
			cleanupCtx := context.WithoutCancel(ctx)
			_, _ = runAffSync(cleanupFn, cleanupCtx)
			return val, nil
		}"""

content = content.replace(old_bracket, new_bracket)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
