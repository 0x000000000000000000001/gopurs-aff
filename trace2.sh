#!/bin/bash
sed -i '' 's/return Func(func(a Value) Value { return fn(arg1, arg2, a) })/return Func(func(a Value) Value { fmt.Println("Calling Func3 from Apply2"); return fn(arg1, arg2, a) })/g' output/gopurs_runtime/runtime.go
