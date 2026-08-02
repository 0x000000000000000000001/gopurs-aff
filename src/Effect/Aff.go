import (
	"context"
	"fmt"
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
	ResultChan chan struct {
		val any
		err error
	}
	Cancel context.CancelFunc
	Id     int64
}

func _MakeFiberNative(aff AffFn) any {
	return func(_ any) any {
		ctx, cancel := context.WithCancel(context.Background())
		resultChan := make(chan struct {
			val any
			err error
		}, 1)
		
		fiberId := time.Now().UnixNano()

		gopurs_runtime.Retain()
		go func() {
			defer gopurs_runtime.Release()
			val, err := runAffSync(aff, ctx)
			if err != nil {
				resultChan <- struct {
					val any
					err error
				}{nil, err}
			} else {
				resultChan <- struct {
					val any
					err error
				}{val, nil}
			}
		}()

		return &NativeFiber{
			ResultChan: resultChan,
			Cancel:     cancel,
			Id:         fiberId,
		}
	}
}

func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	return func(_ any) any {
		nf.Cancel()
		go func() {
			res := <-nf.ResultChan
			nf.ResultChan <- res
			
			if res.err != nil {
				onError(res.err)(nil)
			} else {
				onSuccess(res.val)(nil)
			}
		}()
		return func(_ any) any {
			return nil
		}
	}
}

func _JoinFiber(nf *NativeFiber, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	return func(_ any) any {
		go func() {
			res := <-nf.ResultChan
			nf.ResultChan <- res
			
			if res.err != nil {
				onError(res.err)(nil)
			} else {
				onSuccess(res.val)(nil)
			}
		}()
		return func(_ any) any {
			return nil
		}
	}
}


func _OnCompleteFiber(nf *NativeFiber, onCompleteAny any) any {
	return func(_ any) any {
		return func(_ any) any {
			return nil
		}
	}
}

func _IsSuspendedFiber(nf *NativeFiber) bool {
	return false
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

func _ParAffMap(_ any, _ any) any { panic("Not implemented") }
func _ParAffApply(_ any, _ any) any { panic("Not implemented") }
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
	return func(_ any) any {
		panic("Not implemented")
	}
}
func _KillAll(_ any, _ any, _ any) any { panic("Not implemented") }
func _Sequential(aff AffFn) any { return aff }
func GeneralBracket(_ any, _ any, _ any) any { panic("Not implemented") }
