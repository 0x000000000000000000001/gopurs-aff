package main
import (
	"context"
	"fmt"
	"sync"
	import_atomic "sync/atomic"
	"time"
	"gopurs/output/gopurs_runtime"
)

type AffFn = func(context.Context) (any, error)

type BindNode struct {
	Aff any
	K   func(any) AffFn
}

func runAffSync(aff AffFn, ctx context.Context) (any, error) {
	var current = aff
	var stack []func(any) AffFn

	for {
		val, err := current(ctx)
		if err != nil {
			return nil, err
		}

		if node, ok := val.(BindNode); ok {
			stack = append(stack, node.K)
			current = node.Aff.(AffFn)
		} else {
			if len(stack) > 0 {
				k := stack[len(stack)-1]
				stack = stack[:len(stack)-1]
				current = k(val)
			} else {
				return val, nil
			}
		}
	}
}

func _Pure(val any) any {
	return func(ctx context.Context) (any, error) {
		select {
		case <-ctx.Done():
			return nil, ctx.Err()
		default:
			return val, nil
		}
	}
}

func _Bind(aff AffFn, k func(any) AffFn) any {
	return func(ctx context.Context) (any, error) {
		return BindNode{Aff: aff, K: k}, nil
	}
}

func _Delay(right any, ms float64) any {
	return func(ctx context.Context) (any, error) {
		duration := time.Duration(ms) * time.Millisecond
		timer := time.NewTimer(duration)
		defer timer.Stop()

		select {
		case <-timer.C:
			return nil, nil
		case <-ctx.Done():
			return nil, ctx.Err()
		}
	}
}

func _LiftEffect(eff func(any) any) any {
	return func(ctx context.Context) (any, error) {
		select {
		case <-ctx.Done():
			return nil, ctx.Err()
		default:
			return eff(nil), nil
		}
	}
}

func _MakeAffImpl(build func(func(error) func(any) any) func(func(any) func(any) any) func(any) func(any) AffFn) any {
	return func(ctx context.Context) (any, error) {
		resultChan := make(chan struct {
			val any
			err error
		}, 1)

		onError := func(err error) func(any) any {
			return func(_ any) any {
				select {
				case resultChan <- struct{val any; err error}{nil, err}:
				default:
				}
				return nil
			}
		}

		onSuccess := func(val any) func(any) any {
			return func(_ any) any {
				select {
				case resultChan <- struct{val any; err error}{val, nil}:
				default:
				}
				return nil
			}
		}

		cancelerEffect := build(onError)(onSuccess)
		canceler := cancelerEffect(nil)

		select {
		case res := <-resultChan:
			return res.val, res.err
		case <-ctx.Done():
			cancelFnAff := canceler(fmt.Errorf("context canceled"))
			go runAffSync(cancelFnAff, context.Background())
			return nil, ctx.Err()
		}
	}
}






type NativeFiber struct {
	Ctx        context.Context
	Done       chan struct{}
	Start      chan struct{}
	Val        any
	Err        error
	Cancel     context.CancelCauseFunc
	Id         int64
	mu         sync.Mutex
	IsComplete int32
}

func _MakeFiberNative(aff AffFn) any {
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
}

func _ForkAffNative(aff AffFn) any {
	return func(ctx context.Context) (any, error) {
		eff := _MakeFiberNative(aff).(func(any) any)
		nf := eff(nil)
		return nf, nil
	}
}


func _RunFiber(nf *NativeFiber) any {
	return func(_ any) any {
		select {
		case <-nf.Start:
		default:
			close(nf.Start)
		}
		return nil
}
}

func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	nf.Cancel(errAny)
	select {
	case <-nf.Start:
	default:
		close(nf.Start)
	}
	go func() {
		<-nf.Done
		
		onSuccess(nil)(nil)
	}()
	return func(_ any) any {
		return nil
	}

}

func _JoinFiber(nf *NativeFiber, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	go func() {
		select {
		case <-nf.Start:
		default:
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


func _OnCompleteFiber(nf *NativeFiber, onCompleteAny any) any {
	return func(_ any) any {
		return func(_ any) any {
			return nil
		}
}
}

func _IsSuspendedFiber(nf *NativeFiber) any {
	return func(_ any) any {
		return false
	}
}

func _ThrowError(err error) any {
	return func(ctx context.Context) (any, error) {
		return nil, err
	}
}

func _CatchError(aff AffFn, handler func(any) AffFn) any {
	return func(ctx context.Context) (any, error) {
		val, err := runAffSync(aff, ctx)
		if err != nil {
			if ctx.Err() != nil && context.Cause(ctx) == err {
				return nil, err
			}
			return runAffSync(handler(err), ctx)
		}
		return val, nil
	}
}

func _Map(f func(any) any, aff AffFn) any {
	return func(ctx context.Context) (any, error) {
		val, err := runAffSync(aff, ctx)
		if err != nil {
			return nil, err
		}
		return f(val), nil
	}
}

func _ParAffMap(f func(any) any, aff AffFn) any {
	return _Map(f, aff)
}

func _ParAffApply(aff1 AffFn, aff2 AffFn) any {
	return func(ctx context.Context) (any, error) {
		ctx, cancel := context.WithCancel(ctx)
		defer cancel()

		var wg sync.WaitGroup
		wg.Add(2)

		var res1 any
		var err1 error
		var res2 any
		var err2 error

		go func() {
			defer wg.Done()
			res1, err1 = runAffSync(aff1, ctx)
			if err1 != nil {
				cancel()
			}
		}()

		go func() {
			defer wg.Done()
			res2, err2 = runAffSync(aff2, ctx)
			if err2 != nil {
				cancel()
			}
		}()

		wg.Wait()

		if err1 != nil {
			return nil, err1
		}
		if err2 != nil {
			return nil, err2
		}

		if val, ok := res1.(gopurs_runtime.Value); ok {
			return gopurs_runtime.Apply(val, gopurs_runtime.Box(res2)), nil
		}
		if res1 == nil {
			return nil, nil
		}
		f := res1.(func(any) any)
		return f(res2), nil
	}
}
func _ParAffAlt(aff1 AffFn, aff2 AffFn) any {
	return func(ctx context.Context) (any, error) {
		fn1 := aff1
		fn2 := aff2

		ctx, cancel := context.WithCancel(ctx)
		defer cancel()

		type Result struct {
			val any
			err error
		}
		resCh := make(chan Result, 2)

		go func() {
			val, err := runAffSync(fn1, ctx)
			resCh <- Result{val, err}
		}()
		go func() {
			val, err := runAffSync(fn2, ctx)
			resCh <- Result{val, err}
		}()

		var firstErr error
		for i := 0; i < 2; i++ {
			select {
			case res := <-resCh:
				if res.err == nil {
					return res.val, nil
				}
				if firstErr == nil {
					firstErr = res.err
				} else {
					return nil, firstErr
				}
			case <-ctx.Done():
				return nil, ctx.Err()
			}
		}
		return nil, firstErr
	}
}
func _MakeSupervisedFiber(aff AffFn) any {
	panic("Not implemented")

}
func _KillAll(_ any, _ any, _ any) any { panic("Not implemented") }
func _Sequential(aff AffFn) any { return aff }
func GeneralBracket(acquireBox any, optionsBox any, useBox any) any {
	return func(ctx context.Context) (any, error) {
		acquireVal := acquireBox.(gopurs_runtime.Value)
		acquireFn := gopurs_runtime.Unbox[AffFn](acquireVal)
		
		acquireCtx := context.WithoutCancel(ctx)
		resourceBox, err := runAffSync(acquireFn, acquireCtx)
		if err != nil {
			return nil, err
		}
		
		optionsVal := optionsBox.(gopurs_runtime.Value)
		killedVal := gopurs_runtime.RecordGet(optionsVal, "killed")
		failedVal := gopurs_runtime.RecordGet(optionsVal, "failed")
		completedVal := gopurs_runtime.RecordGet(optionsVal, "completed")
		
		useVal := useBox.(gopurs_runtime.Value)
		useFnAff := gopurs_runtime.Unbox[AffFn](gopurs_runtime.Apply(useVal, gopurs_runtime.Box(resourceBox)))
		
		resultVal, useErr := runAffSync(useFnAff, ctx)
		
		if useErr != nil {
			var cleanupVal gopurs_runtime.Value
			if ctx.Err() != nil && context.Cause(ctx) == useErr {
				errBox := gopurs_runtime.Box(useErr)
				cleanupVal = gopurs_runtime.Apply2(killedVal, errBox, gopurs_runtime.Box(resourceBox))
			} else {
				errBox := gopurs_runtime.Box(useErr)
				cleanupVal = gopurs_runtime.Apply2(failedVal, errBox, gopurs_runtime.Box(resourceBox))
			}
			cleanupFn := gopurs_runtime.Unbox[AffFn](cleanupVal)
			cleanupCtx := context.WithoutCancel(ctx)
			_, _ = runAffSync(cleanupFn, cleanupCtx)
			return nil, useErr
		} else {
			cleanupVal := gopurs_runtime.Apply2(completedVal, gopurs_runtime.Box(resultVal), gopurs_runtime.Box(resourceBox))
			cleanupFn := gopurs_runtime.Unbox[AffFn](cleanupVal)
			cleanupCtx := context.WithoutCancel(ctx)
			_, cleanupErr := runAffSync(cleanupFn, cleanupCtx)
			if cleanupErr != nil {
				return nil, cleanupErr
			}
			return resultVal, nil
		}
	}
}
