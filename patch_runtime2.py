import sys
with open("output/gopurs_runtime/runtime.go", "r") as f:
    content = f.read()

content = content.replace('''case TypeFunc3:
		fn := *(*func(Value, Value, Value) Value)(unsafe.Pointer(&f.UnsafePtr))
		fmt.Printf("Apply2 TypeFunc3: capturing arg1=%+v, arg2=%+v\\n", arg1, arg2)
		return Func(func(a Value) Value { 
			fmt.Printf("Apply2 TypeFunc3 closure: executing with arg1=%+v, arg2=%+v, a=%+v\\n", arg1, arg2, a)
			return fn(arg1, arg2, a) 
		})''', '''case TypeFunc3:
		fn := *(*func(Value, Value, Value) Value)(unsafe.Pointer(&f.UnsafePtr))
		fnPtr := f.UnsafePtr
		fmt.Printf("Apply2 TypeFunc3: fnPtr=%v capturing arg1=%+v, arg2=%+v\\n", fnPtr, arg1, arg2)
		return Func(func(a Value) Value { 
			fmt.Printf("Apply2 TypeFunc3 closure: fnPtr=%v executing with arg1=%+v, arg2=%+v, a=%+v\\n", fnPtr, arg1, arg2, a)
			return fn(arg1, arg2, a) 
		})''')

with open("output/gopurs_runtime/runtime.go", "w") as f:
    f.write(content)
