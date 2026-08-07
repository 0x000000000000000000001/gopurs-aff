import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

supervise_impl = """type Supervisor struct {
	Cancel context.CancelCauseFunc
	Wg     *sync.WaitGroup
}

type supervisorKeyType struct{}
var supervisorKey = supervisorKeyType{}

func _MakeSupervisedFiber(aff AffFn) any {
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

		sup := &Supervisor{
			Cancel: cancel,
			Wg:     &sync.WaitGroup{},
		}
		
		// The fiber itself is a child of the supervisor
		sup.Wg.Add(1)

		gopurs_runtime.Retain()
		go func() {
			defer gopurs_runtime.Release()
			defer sup.Wg.Done()
			<-nf.Start
			
			// Put the supervisor in the context so child fibers can find it
			ctxWithSup := context.WithValue(ctx, supervisorKey, sup)
			val, err := runAffSync(aff, ctxWithSup)
			
			nf.mu.Lock()
			nf.Val = val
			nf.Err = err
			import_atomic.StoreInt32(&nf.IsComplete, 1)
			nf.mu.Unlock()
			close(nf.Done)
		}()
		
		return map[string]any{
			"supervisor": sup,
			"fiber":      nf,
		}
	}
}

func _KillAll(errAny error, supAny any, cbAny any) any {
	return func(_ any) any {
		sup := supAny.(*Supervisor)
		cb := cbAny.(func(any) any)
		
		sup.Cancel(errAny)
		
		go func() {
			sup.Wg.Wait()
			cb(nil)
		}()
		
		return func(_ any) any {
			return nil
		}
	}
}
"""

content = content.replace('func _MakeSupervisedFiber(aff AffFn) any {\n\tpanic("Not implemented")\n\n}\nfunc _KillAll(_ any, _ any, _ any) any { panic("Not implemented") }', supervise_impl)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)

