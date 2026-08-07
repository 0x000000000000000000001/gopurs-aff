import os

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

# 1. Fix NativeFiber struct and _MakeFiberNative
content = content.replace("""type NativeFiber struct {
	Done   chan struct{}
	Val    any
	Err    error
	Cancel context.CancelFunc
	Id     int64
}

func _MakeFiberNative(aff AffFn) any {
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
}""", """type NativeFiber struct {
	Ctx        context.Context
	Done       chan struct{}
	Start      chan struct{}
	Val        any
	Err        error
	Cancel     context.CancelFunc
	Id         int64
	mu         sync.Mutex
	IsComplete int32
}

func _MakeFiberNative(aff AffFn) any {
	ctx, cancel := context.WithCancel(context.Background())
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
		atomic.StoreInt32(&nf.IsComplete, 1)
		nf.mu.Unlock()
		close(nf.Done)
	}()

	return nf
}""")

# 2. Fix _ForkAffNative (wait, the file has it, let's just do it manually)

# Wait, let's just output the entire fixed file instead of replacing.
