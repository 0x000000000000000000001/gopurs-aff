import sys

with open("output/Effect/Effect_ffi.go", "r") as f:
    content = f.read()

content = content.replace('''func PureE(a any, _ interface{}) any {
	return func(_ interface{}) any {
		return a
	}
}''', '''func PureE(a any, _ interface{}) any {
	return a
}''')

content = content.replace('''func UntilE(f func(interface{}) any, _ interface{}) any {
	return func(_ interface{}) any {
		for {
			if f(nil).(bool) {
				break
			}
		}
		return nil
	}
}''', '''func UntilE(f func(interface{}) any, _ interface{}) any {
	for {
		if f(nil).(bool) {
			break
		}
	}
	return nil
}''')

content = content.replace('''func WhileE(f func(interface{}) any, a func(interface{}) any, _ interface{}) any {
	return func(_ interface{}) any {
		for {
			if !f(nil).(bool) {
				break
			}
			a(nil)
		}
		return nil
	}
}''', '''func WhileE(f func(interface{}) any, a func(interface{}) any, _ interface{}) any {
	for {
		if !f(nil).(bool) {
			break
		}
		a(nil)
	}
	return nil
}''')

content = content.replace('''func ForE(lo int64, hi int64, f func(any) func(interface{}) any, _ interface{}) any {
	return func(_ interface{}) any {
		for i := lo; i < hi; i++ {
			f(i)(nil)
		}
		return nil
	}
}''', '''func ForE(lo int64, hi int64, f func(any) func(interface{}) any, _ interface{}) any {
	for i := lo; i < hi; i++ {
		f(i)(nil)
	}
	return nil
}''')

content = content.replace('''func ForeachE(as []any, f func(any) func(interface{}) any, _ interface{}) any {
	return func(_ interface{}) any {
		for _, a := range as {
			f(a)(nil)
		}
		return nil
	}
}''', '''func ForeachE(as []any, f func(any) func(interface{}) any, _ interface{}) any {
	for _, a := range as {
		f(a)(nil)
	}
	return nil
}''')

with open("output/Effect/Effect_ffi.go", "w") as f:
    f.write(content)
