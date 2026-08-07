import re

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

old_block = """	go func() {
		<-nf.Done
		if nf.Err != nil {
			onError(nf.Err)(nil)
		} else {
			onSuccess(nf.Val)(nil)
		}
	}()"""

new_block = """	go func() {
		<-nf.Done
		if nf.Err != nil && nf.Err != errAny {
			onError(nf.Err)(nil)
		} else {
			onSuccess(nil)(nil)
		}
	}()"""

content = content.replace(old_block, new_block)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
