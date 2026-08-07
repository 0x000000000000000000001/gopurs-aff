import sys

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

old_block = """func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	return func(_ any) any {
		nf.Cancel(errAny)
	select {
	case <-nf.Start:
	default:
		close(nf.Start)
	}
		go func() {
			<-nf.Done
			
			if nf.Err != nil {
				onError(nf.Err)(nil)
			} else {
				onSuccess(nf.Val)(nil)
			}
		}()"""
new_block = """func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any) any {
	return func(_ any) any {
		nf.Cancel(errAny)
	select {
	case <-nf.Start:
	default:
		close(nf.Start)
	}
		go func() {
			<-nf.Done
			
			onSuccess(nil)(nil)
		}()"""

if old_block in code:
    code = code.replace(old_block, new_block)
    with open("src/Effect/Aff.go", "w") as f:
        f.write(code)
    print("PATCHED")
else:
    print("NOT FOUND")
