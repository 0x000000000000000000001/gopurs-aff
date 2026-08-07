import sys

with open("output/gopurs_runtime/runtime.go", "r") as f:
    content = f.read()

old_apply = """func Apply(f Value, arg Value) Value {
	switch f.Type {
	case TypeFunc:"""

new_apply = """func Apply(f Value, arg Value) Value {
	if f.Type == TypeString {
		fmt.Printf("PANIC ABOUT TO HAPPEN IN APPLY: f is String: %s\\n", Unbox[string](f))
	}
	switch f.Type {
	case TypeFunc:"""

content = content.replace(old_apply, new_apply)

# Add fmt import if needed
if '"fmt"' not in content:
    content = content.replace('import (', 'import (\n\t"fmt"')

with open("output/gopurs_runtime/runtime.go", "w") as f:
    f.write(content)
