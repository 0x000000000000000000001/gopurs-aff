import sys

with open("output/Effect.Aff/Effect_Aff_ffi.go", "r") as f:
    code = f.read()

old_block = """
		go func() {
			<-nf.Done
			
			if nf.Err != nil {
				onError(nf.Err)(nil)
			} else {
				onSuccess(nf.Val)(nil)
			}
		}()
"""
new_block = """
		go func() {
			<-nf.Done
			
			onSuccess(nil)(nil)
		}()
"""

code = code.replace(old_block, new_block)

with open("output/Effect.Aff/Effect_Aff_ffi.go", "w") as f:
    f.write(code)
