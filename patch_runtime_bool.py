import sys

with open("output/gopurs_runtime/runtime.go", "r") as f:
    content = f.read()

content = content.replace("panic(fmt.Sprintf(\"Attempted to apply a non-function", """if f.Type == TypeBool {
		fmt.Printf("[DEBUG] Applied TypeBool. Stack:\\n")
		import_debug "runtime/debug"
		fmt.Printf("%s\\n", import_debug.Stack())
	}
	panic(fmt.Sprintf(\"Attempted to apply a non-function""")

content = content.replace("import (", "import (\\n\\timport_debug \"runtime/debug\"")

with open("output/gopurs_runtime/runtime.go", "w") as f:
    f.write(content)
