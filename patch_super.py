import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

old_super = """func _MakeSupervisedFiber(aff_ any) any {
	aff := gopurs_runtime.Unbox[AffFn](aff_.(gopurs_runtime.Value))
	return func(ctx context.Context) (any, error) {
		supCtx, cancel := context.WithCancelCause(context.Background())
		sup := &Supervisor{
			Ctx:    supCtx,
			Cancel: cancel,
			Wg:     &sync.WaitGroup{},
		}
		
		fiberId := time.Now().UnixNano()
		nf := &NativeFiber{
			Aff:        aff,
			Ctx:        supCtx, // supervised
			Done:       make(chan struct{}),
			Start:      make(chan struct{}),
			Cancel:     cancel,
			Id:         fiberId,
		}
		
		rec := gopurs_runtime.RecordDict0()
		rec = gopurs_runtime.RecordInsert(rec, "fiber", gopurs_runtime.Box(nf))
		rec = gopurs_runtime.RecordInsert(rec, "supervisor", gopurs_runtime.Box(sup))
		
		return rec, nil
	}
}"""
new_super = """func _MakeSupervisedFiber(aff_ any) any {
	aff := gopurs_runtime.Unbox[AffFn](aff_.(gopurs_runtime.Value))
	return func(ctx context.Context) (any, error) {
		supCtx, cancel := context.WithCancelCause(context.Background())
		sup := &Supervisor{
			Ctx:    supCtx,
			Cancel: cancel,
			Wg:     &sync.WaitGroup{},
		}
		
		fiberId := time.Now().UnixNano()
		nf := &NativeFiber{
			Aff:        aff,
			Ctx:        supCtx, // supervised
			Done:       make(chan struct{}),
			Start:      make(chan struct{}),
			Cancel:     cancel,
			Id:         fiberId,
		}
		
		rec := gopurs_runtime.RecordDict2("fiber", "supervisor", gopurs_runtime.Box(nf), gopurs_runtime.Box(sup))
		
		return rec, nil
	}
}"""

content = content.replace(old_super, new_super)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
