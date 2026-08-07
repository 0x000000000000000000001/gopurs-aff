import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

# Add Aff to NativeFiber
content = content.replace("type NativeFiber struct {", "type NativeFiber struct {\n\tAff AffFn")

# Fix _MakeFiberNative
make_fiber_old = """func _MakeFiberNative(aff AffFn) any {
	return func(_ any) any {
		ctx, cancel := context.WithCancelCause(context.Background())
		done := make(chan struct{})
		start := make(chan struct{})
		
		fiberId := time.Now().UnixNano()
		nf := &NativeFiber{
			Ctx:        ctx,
			Done:       done,
			Start:      start,
			Cancel:     cancel,
			Id:         fiberId,
			IsComplete: 0,
		}

		gopurs_runtime.Retain()
		go func() {
			defer gopurs_runtime.Release()
			<-nf.Start
			val, err := runAffSync(aff, ctx)
			nf.mu.Lock()
			nf.Val = val
			nf.Err = err
			import_atomic.StoreInt32(&nf.IsComplete, 1)
			nf.mu.Unlock()
			close(nf.Done)
		}()

		return nf
	}
}"""

make_fiber_new = """func _MakeFiberNative(aff AffFn) any {
	return func(_ any) any {
		ctx, cancel := context.WithCancelCause(context.Background())
		done := make(chan struct{})
		start := make(chan struct{})
		
		fiberId := time.Now().UnixNano()
		nf := &NativeFiber{
			Aff:        aff,
			Ctx:        ctx,
			Done:       done,
			Start:      start,
			Cancel:     cancel,
			Id:         fiberId,
			IsComplete: 0,
		}
		return nf
	}
}"""
content = content.replace(make_fiber_old, make_fiber_new)

# Fix _ForkAffNative to set Aff and close start
fork_aff_old = """		nf := &NativeFiber{
			Ctx:        childCtx,
			Done:       done,
			Start:      start,
			Cancel:     cancel,
			Id:         fiberId,
			IsComplete: 0,
		}

		if supAny != nil {"""

fork_aff_new = """		nf := &NativeFiber{
			Aff:        aff,
			Ctx:        childCtx,
			Done:       done,
			Start:      start,
			Cancel:     cancel,
			Id:         fiberId,
			IsComplete: 0,
		}
		close(start)

		if supAny != nil {"""
content = content.replace(fork_aff_old, fork_aff_new)

# Fix _ForkAffNative to remove goroutines
content = content.replace("\t\t\t\t\t<-nf.Start\n\t\t\t\t\t\n\t\t\t\t\t// Keep the supervisor", "\t\t\t\t\t// Keep the supervisor")
content = content.replace("\t\t\t\t\t<-nf.Start\n\t\t\t\t\t\n\t\t\t\t\tval, err :=", "\t\t\t\t\tval, err :=")

# Fix _RunFiber
run_fiber_old = """func _RunFiber(nf *NativeFiber, _ interface{}) any {
	select {
	case <-nf.Start:
	default:
		close(nf.Start)
	}
	return nil
}"""

run_fiber_new = """func _RunFiber(nf *NativeFiber, _ interface{}) any {
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
	return nil
}"""
content = content.replace(run_fiber_old, run_fiber_new)

# Fix _JoinFiber
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
			_RunFiber(nf, nil)
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
