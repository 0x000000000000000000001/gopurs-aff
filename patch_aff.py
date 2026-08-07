import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

# 1. Fix _IsSuspendedFiber
old_sus = """func _IsSuspendedFiber(nf *NativeFiber) bool {
	return false
}"""
new_sus = """func _IsSuspendedFiber(nf *NativeFiber) func(any) any {
	return func(any) any {
		return false
	}
}"""
content = content.replace(old_sus, new_sus)

# 2. Fix _KillFiber
old_kill = """func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	return func(_ any) any {
		nf.Cancel(errAny)
	select {
	case <-nf.Start:
	default:
		close(nf.Start)
	}
		go func() {
			<-nf.Done
			
			if nf.Err != nil {
				onError(nf.Err)(nil)
			} else {
				onSuccess(nf.Val)(nil)
			}
		}()
		return func(_ any) any {
			return nil
		}
	}
}"""
new_kill = """func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	return func(_ any) any {
		nf.Cancel(errAny)
	select {
	case <-nf.Start:
	default:
		close(nf.Start)
	}
		go func() {
			<-nf.Done
			
			if nf.Err != nil && nf.Err != errAny && nf.Err.Error() != errAny.Error() {
				onError(nf.Err)(nil)
			} else {
				onSuccess(nil)(nil)
			}
		}()
		return func(_ any) any {
			return nil
		}
	}
}"""
content = content.replace(old_kill, new_kill)

# 3. Fix GeneralBracket
old_bracket = """		if err != nil {
			failedBox := gopurs_runtime.RecordGet(optionsVal, "failed")
			errBox := gopurs_runtime.Box(err)
			cleanupBox := gopurs_runtime.Apply2(failedBox, errBox, gopurs_runtime.Box(resource))
			cleanupFn := gopurs_runtime.Unbox[AffFn](cleanupBox)
			_, _ = runAffSync(cleanupFn, ctx)
			return nil, err
		} else {"""
new_bracket = """		if err != nil {
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
		} else {"""
content = content.replace(old_bracket, new_bracket)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
