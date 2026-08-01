import (
	"context"
	"fmt"
	"time"
	"gopurs/output/gopurs_runtime"
)

type AffFn = func(context.Context) (any, error)

type BindNode struct {
	Aff any
	K   func(any) any
}

func runAffSync(aff AffFn, ctx context.Context) (any, error) {
	var current = aff
	var stack []func(any) any

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
				retVal := k(val)
				if valWrapper, isVal := retVal.(gopurs_runtime.Value); isVal {
					current = (*(*any)(valWrapper.UnsafePtr)).(AffFn)
				} else {
					current = retVal.(AffFn)
				}
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

func _Bind(aff AffFn, k func(any) any) any {
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

func MakeAff(build func(func(any) any) func(any) any) any {
	return func(ctx context.Context) (any, error) {
		resultChan := make(chan struct {
			val any
			err error
		}, 1)

		callback := func(either any) any {
			return func(_ any) any {
				if val, ok := either.(gopurs_runtime.Value); ok {
					if val.IntVal == 3711209382 { // Left
						errVal := (*struct{Rc uint32; Value0 gopurs_runtime.Value})(val.UnsafePtr).Value0
						resultChan <- struct{val any; err error}{nil, fmt.Errorf("Aff Error: %+v", errVal)}
					} else { // Right
						rval := (*struct{Rc uint32; Value0 gopurs_runtime.Value})(val.UnsafePtr).Value0
						resultChan <- struct{val any; err error}{rval, nil}
					}
				}
				return nil
			}
		}

		cancelerEffect := build(callback)
		canceler := cancelerEffect(nil)

		select {
		case res := <-resultChan:
			return res.val, res.err
		case <-ctx.Done():
			if cancelFn, ok := canceler.(func(any) any); ok {
				cancelFnEffect := cancelFn(fmt.Errorf("context canceled"))
				if effectFn, ok := cancelFnEffect.(func(any) any); ok {
					effectFn(nil)
				}
			}
			return nil, ctx.Err()
		}
	}
}

func _MakeFiber(ffiUtil any, aff AffFn, _ any) any {
	ctx, cancel := context.WithCancel(context.Background())
	resultChan := make(chan struct {
		val any
		err error
	}, 1)

	go func() {
		val, err := runAffSync(aff, ctx)
		resultChan <- struct {
			val any
			err error
		}{val, err}
	}()

	fiber := map[string]any{
		"run": func(_ any) any { return nil },
		"kill": func(err any) any {
			return func(k any) any {
				return func(_ any) any {
					cancel()
					return func(_ any) any {
						res := <-resultChan
						return k.(func(any) any)(res.val).(func(any) any)(nil)
					}
				}
			}
		},
		"join": func(k any) any {
			return func(_ any) any {
				return func(_ any) any {
					res := <-resultChan
					return k.(func(any) any)(res.val).(func(any) any)(nil)
				}
			}
		},
		"onComplete": func(onComplete any) any {
			return func(_ any) any {
				return func(_ any) any {
					return nil
				}
			}
		},
		"isSuspended": func(_ any) any { return false },
	}
	return fiber
}

func _Fork(isSuspended any, aff AffFn) any {
    return func(ctx context.Context) (any, error) {
        fiber := _MakeFiber(nil, aff, nil)
        return fiber, nil
    }
}

func _ThrowError(err any) any {
	return func(ctx context.Context) (any, error) {
		if val, ok := err.(gopurs_runtime.Value); ok {
			if val.Type == 13 {
				if e, ok := (*(*any)(val.UnsafePtr)).(error); ok {
					return nil, e
				}
			}
		}
		if e, ok := err.(error); ok {
			return nil, e
		}
		return nil, fmt.Errorf("%v", err)
	}
}

func _CatchError(aff AffFn, handler func(any) any) any {
	return func(ctx context.Context) (any, error) {
		val, err := runAffSync(aff, ctx)
		if err != nil {
			retVal := handler(err)
			var nextAff AffFn
			if valWrapper, isVal := retVal.(gopurs_runtime.Value); isVal {
				nextAff = (*(*any)(valWrapper.UnsafePtr)).(AffFn)
			} else {
				nextAff = retVal.(AffFn)
			}
			return runAffSync(nextAff, ctx)
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
func _MakeSupervisedFiber(_ any, _ any) any { panic("Not implemented") }
func _KillAll(_ any, _ any, _ any) any { panic("Not implemented") }
func _Sequential(aff AffFn) any { return aff }
func GeneralBracket(_ any, _ any, _ any) any { panic("Not implemented") }
