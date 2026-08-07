import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

# Add KillState and getKillError
helper = """
type key int
const killErrKey key = 0
type KillState struct {
	Err error
}

func getKillError(ctx context.Context, defaultErr error) error {
	if ks, ok := ctx.Value(killErrKey).(*KillState); ok && ks.Err != nil {
		return ks.Err
	}
	return defaultErr
}
"""
content = content.replace("type NativeFiber struct {", helper + "\ntype NativeFiber struct {")

# Replace NativeFiber struct
content = content.replace("""type NativeFiber struct {
	Done   chan struct{}
	Val    any
	Err    error
	Cancel context.CancelFunc
	Id     int64
}""", """import_atomic "sync/atomic"

type NativeFiber struct {
	Ctx        context.Context
	Done       chan struct{}
	Start      chan struct{}
	Val        any
	Err        error
	Cancel     context.CancelFunc
	Id         int64
	mu         sync.Mutex
	IsComplete int32
}""")

# Replace _MakeFiberNative
content = content.replace("""func _MakeFiberNative(aff AffFn) any {
	return func(_ any) any {
		ctx, cancel := context.WithCancel(context.Background())
		done := make(chan struct{})
		
		fiberId := time.Now().UnixNano()
		nf := &NativeFiber{
			Done:   done,
			Cancel: cancel,
			Id:     fiberId,
		}

		gopurs_runtime.Retain()
		go func() {
			defer gopurs_runtime.Release()
			val, err := runAffSync(aff, ctx)
			if err != nil {
				fmt.Println("[FATAL] Unhandled Fiber Error:", err)
			}
			nf.Val = val
			nf.Err = err
			close(nf.Done)
		}()

		return nf
	}
}""", """func _MakeFiberNative(aff AffFn) any {
	return func(_ any) any {
		ctx, cancel := context.WithCancel(context.Background())
		ctx = context.WithValue(ctx, killErrKey, &KillState{})
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
}""")

# Add _RunFiber
runfiber = """
func _RunFiber(nf *NativeFiber, _ interface{}) any {
	select {
	case <-nf.Start:
	default:
		close(nf.Start)
	}
	return nil
}
"""
content = content.replace("func _KillFiber", runfiber + "\nfunc _KillFiber")

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
