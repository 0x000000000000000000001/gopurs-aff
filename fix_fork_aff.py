import sys
with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

fork_impl = """func _ForkAffNative(aff AffFn) any {
	return func(ctx context.Context) (any, error) {
		childCtx, cancel := context.WithCancelCause(ctx)
		done := make(chan struct{})
		start := make(chan struct{})
		
		fiberId := time.Now().UnixNano()
		nf := &NativeFiber{
			Ctx:        childCtx,
			Done:       done,
			Start:      start,
			Cancel:     cancel,
			Id:         fiberId,
			IsComplete: 0,
		}

		if sup, ok := ctx.Value(supervisorKey).(*Supervisor); ok {
			sup.Wg.Add(1)
			go func() {
				defer sup.Wg.Done()
				<-nf.Done
			}()
		}

		gopurs_runtime.Retain()
		go func() {
			defer gopurs_runtime.Release()
			<-nf.Start
			val, err := runAffSync(aff, childCtx)
			nf.mu.Lock()
			nf.Val = val
			nf.Err = err
			import_atomic.StoreInt32(&nf.IsComplete, 1)
			nf.mu.Unlock()
			close(nf.Done)
		}()

		return nf, nil
	}
}
"""

content = content.replace("func _RunFiber", fork_impl + "\nfunc _RunFiber")

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
