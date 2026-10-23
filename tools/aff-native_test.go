package affprobe

import (
	"context"
	"errors"
	"testing"

	rt "gopurs/output/gopurs_runtime"
)

func runWithoutPanic(t *testing.T, aff AffFn, ctx context.Context) (value any, err error) {
	t.Helper()
	defer func() {
		if failure := recover(); failure != nil {
			t.Errorf("Effect panic escaped Aff: %v", failure)
		}
	}()
	return runAffSync(aff, ctx)
}

func TestLiftEffectSuccess(t *testing.T) {
	calls := 0
	aff := _LiftEffect(func(any) any { calls++; return "result" }).(AffFn)
	value, err := runWithoutPanic(t, aff, context.Background())
	if value != "result" || err != nil || calls != 1 {
		t.Fatalf("value=%v, err=%v, calls=%d", value, err, calls)
	}
}

func TestLiftEffectErrorIdentityAndCatch(t *testing.T) {
	expected := errors.New("incremental cache: read-parts failed")
	lifted := _LiftEffect(func(any) any { panic(expected) }).(AffFn)
	value, err := runWithoutPanic(t, lifted, context.Background())
	if value != nil || err != expected {
		t.Errorf("direct value=%v, err=%v; expected identical error", value, err)
	}
	handled := false
	caught := _CatchError(lifted, func(failure any) AffFn {
		handled = true
		if failure != expected {
			t.Errorf("handler received %v instead of identical error", failure)
		}
		return _Pure("recovered").(AffFn)
	}).(AffFn)
	value, err = runWithoutPanic(t, caught, context.Background())
	if !handled || value != "recovered" || err != nil {
		t.Fatalf("handled=%v, value=%v, err=%v", handled, value, err)
	}
}

func TestLiftEffectStringPanic(t *testing.T) {
	lifted := _LiftEffect(func(any) any { panic("string failure") }).(AffFn)
	value, err := runWithoutPanic(t, lifted, context.Background())
	if value != nil || err == nil || err.Error() != "string failure" {
		t.Fatalf("value=%v, err=%v", value, err)
	}
}

func TestLiftEffectBracketReleasesBeforeCatch(t *testing.T) {
	for _, mode := range []string{"AffThrowControl", "EffectThrow", "BindThrow", "UseThrow"} {
		t.Run(mode, func(t *testing.T) {
			expected := errors.New("use failed")
			events := []string{}
			cleanup := func(kind string) rt.Value {
				return rt.Func(func(value rt.Value) rt.Value {
					return rt.Func(func(resource rt.Value) rt.Value {
						return rt.Box(AffFn(func(context.Context) (any, error) {
							if kind != "failed" || rt.Unbox[error](value) != expected || rt.Unbox[string](resource) != "resource" {
								t.Errorf("cleanup kind=%s, wrong error or resource", kind)
							}
							events = append(events, kind)
							return nil, nil
						}))
					})
				})
			}
			use := rt.Func(func(rt.Value) rt.Value {
				if mode == "UseThrow" {
					panic(expected)
				}
				if mode == "EffectThrow" {
					return rt.Box(_LiftEffect(func(any) any { panic(expected) }))
				}
				if mode == "BindThrow" {
					return rt.Box(_Bind(_Pure(nil).(AffFn), func(any) AffFn { panic(expected) }))
				}
				return rt.Box(_ThrowError(expected))
			})
			bracket := GeneralBracket(rt.Box(_Pure("resource")),
				rt.RecordDict3("killed", "failed", "completed", cleanup("killed"), cleanup("failed"), cleanup("completed")), use).(AffFn)
			caught := _CatchError(bracket, func(failure any) AffFn {
				if failure != expected {
					t.Errorf("catch error identity changed")
				}
				events = append(events, "catch")
				return _Pure("recovered").(AffFn)
			}).(AffFn)
			value, err := runWithoutPanic(t, caught, context.Background())
			if value != "recovered" || err != nil || len(events) != 2 || events[0] != "failed" || events[1] != "catch" {
				t.Fatalf("value=%v, err=%v, events=%v", value, err, events)
			}
		})
	}
}

func TestBindContinuationExceptionCaught(t *testing.T) {
	expected := errors.New("incremental cache: lazy implementation failed")
	aff := _Bind(_Pure(nil).(AffFn), func(any) AffFn { panic(expected) }).(AffFn)
	handled := false
	caught := _CatchError(aff, func(failure any) AffFn {
		handled = true
		if failure != expected {
			t.Errorf("bind error identity changed: %v", failure)
		}
		return _Pure("recovered").(AffFn)
	}).(AffFn)
	value, err := runWithoutPanic(t, caught, context.Background())
	if !handled || value != "recovered" || err != nil {
		t.Fatalf("handled=%v, value=%v, err=%v", handled, value, err)
	}
}

func TestLiftEffectCanceledDoesNotCallEffect(t *testing.T) {
	expected := errors.New("cancelled")
	ctx, cancel := context.WithCancelCause(context.Background())
	cancel(expected)
	calls := 0
	aff := _LiftEffect(func(any) any { calls++; return "unreachable" }).(AffFn)
	value, err := runWithoutPanic(t, aff, ctx)
	if value != nil || err != expected || calls != 0 {
		t.Fatalf("value=%v, err=%v, calls=%d", value, err, calls)
	}
}
