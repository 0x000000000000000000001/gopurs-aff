import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

fork_impl = """func _ForkAffNative(aff_ any) any {
	aff := gopurs_runtime.Unbox[AffFn](aff_.(gopurs_runtime.Value))
	return func(ctx context.Context) (any, error) {
		childCtx, cancel := context.WithCancelCause(context.Background())
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

		supAny := ctx.Value(supervisorKey)
		if supAny != nil {
			sup := supAny.(*Supervisor)
			sup.Wg.Add(1)
			
			gopurs_runtime.Retain()
			go func() {
				defer gopurs_runtime.Release()
				defer sup.Wg.Done()
				<-nf.Start
				
				// Keep the supervisor in the child's context
				ctxWithSup := context.WithValue(childCtx, supervisorKey, sup)
				val, err := runAffSync(aff, ctxWithSup)
				
				nf.mu.Lock()
				nf.Val = val
				nf.Err = err
				import_atomic.StoreInt32(&nf.IsComplete, 1)
				nf.mu.Unlock()
				close(nf.Done)
			}()
		} else {
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
		}

		return nf, nil
	}
}
"""

import re
content = re.sub(r'func _ForkAffNative\(aff_ any\) any \{[\s\S]*?\n\}\n', fork_impl, content)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
