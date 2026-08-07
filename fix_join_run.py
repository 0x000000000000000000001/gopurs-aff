import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

join_old = """func _JoinFiber(nf *NativeFiber, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	return func(_ any) any {
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

join_new = """func _JoinFiber(nf *NativeFiber, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	return func(_ any) any {
		go func() {
			select {
			case <-nf.Start:
			default:
				gopurs_runtime.Retain()
				go func() {
					defer gopurs_runtime.Release()
					val, err := runAffSync(nf.Aff, nf.Ctx)
					nf.mu.Lock()
					nf.Val = val
					nf.Err = err
					import_atomic.StoreInt32(&nf.IsComplete, 1)
					nf.mu.Unlock()
					close(nf.Done)
				}()
				close(nf.Start)
			}
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
content = content.replace(join_old, join_new)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
