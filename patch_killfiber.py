import sys

with open("output/Effect.Aff/Effect_Aff_ffi.go", "r") as f:
    content = f.read()

old_func = """func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
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

new_func = """func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
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
				// If it died with the kill error (or successfully despite kill), kill succeeds!
				import_unit := gopurs_runtime.Apply(gopurs_runtime.RecordGet(gopurs_runtime.RecordDict0(), "a"), gopurs_runtime.Any(nil)) // dummy
				_ = import_unit
				// Just pass nil to onSuccess, it ignores the value since it's Unit
				onSuccess(nil)(nil)
			}
		}()
		return func(_ any) any {
			return nil
		}
	}
}"""

content = content.replace(old_func, new_func)

with open("output/Effect.Aff/Effect_Aff_ffi.go", "w") as f:
    f.write(content)
