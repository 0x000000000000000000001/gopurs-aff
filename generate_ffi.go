package main

import (
	"fmt"
	"os"
)

func main() {
	f, _ := os.Create("/Users/0x1/Documents/htdocs/gopurs-effect/src/Effect/Uncurried.go")
	fmt.Fprintln(f, "package Effect_Uncurried")
	fmt.Fprintln(f)
	fmt.Fprintln(f, "import \"gopurs/output/gopurs_runtime\"")
	fmt.Fprintln(f)

	for i := 1; i <= 10; i++ {
		args := ""
		apply := "f"
		for j := 1; j <= i; j++ {
			if j > 1 {
				args += ", "
			}
			args += fmt.Sprintf("a%d gopurs_runtime.Value", j)
			apply = fmt.Sprintf("gopurs_runtime.Apply(%s, a%d)", apply, j)
		}
		
		fmt.Fprintf(f, "func MkEffectFn%d(f gopurs_runtime.Value) gopurs_runtime.Value {\n", i)
		if i == 1 {
			fmt.Fprintf(f, "\treturn gopurs_runtime.Func(func(%s) gopurs_runtime.Value {\n", args)
		} else {
			fmt.Fprintf(f, "\treturn gopurs_runtime.Func%d(func(%s) gopurs_runtime.Value {\n", i, args)
		}
		fmt.Fprintf(f, "\t\treturn gopurs_runtime.Apply(%s, gopurs_runtime.Value{})\n", apply)
		fmt.Fprintf(f, "\t})\n")
		fmt.Fprintf(f, "}\n\n")
	}

	for i := 1; i <= 10; i++ {
		args := ""
		argsCall := ""
		for j := 1; j <= i; j++ {
			if j > 1 {
				args += ", "
				argsCall += ", "
			}
			args += fmt.Sprintf("a%d gopurs_runtime.Value", j)
			argsCall += fmt.Sprintf("a%d", j)
		}
		
		fmt.Fprintf(f, "func RunEffectFn%d(f gopurs_runtime.Value, %s) gopurs_runtime.Value {\n", i, args)
		fmt.Fprintf(f, "\treturn gopurs_runtime.Func(func(_ gopurs_runtime.Value) gopurs_runtime.Value {\n")
		if i == 1 {
			fmt.Fprintf(f, "\t\treturn gopurs_runtime.Apply(f, %s)\n", argsCall)
		} else {
			fmt.Fprintf(f, "\t\treturn gopurs_runtime.Apply%d(f, %s)\n", i, argsCall)
		}
		fmt.Fprintf(f, "\t})\n")
		fmt.Fprintf(f, "}\n\n")
	}
}
