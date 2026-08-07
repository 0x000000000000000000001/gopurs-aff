import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

kill_all_impl = """func _KillAll(errAny error, supAny any, cbAny any) any {
	return func(_ any) any {
		supVal := supAny.(gopurs_runtime.Value)
		sup := gopurs_runtime.Unbox[*Supervisor](supVal)
		
		cbVal := cbAny.(gopurs_runtime.Value)
		cb := gopurs_runtime.Unbox[func(any) any](cbVal)
		
		sup.Cancel(errAny)
		
		go func() {
			sup.Wg.Wait()
			cb(nil)
		}()
		
		return func(_ any) any {
			return nil
		}
	}
}"""

import re
content = re.sub(r'func _KillAll\(errAny error, supAny any, cbAny any\) any \{.*?return nil\n\t\t\}\n\t\}\n\}', kill_all_impl, content, flags=re.DOTALL)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)

