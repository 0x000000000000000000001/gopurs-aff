import sys

with open("output/Test.Main/main/main.go", "r") as f:
    code = f.read()

code = code.replace("gopurs_runtime.Apply(Test_Main.Get_main(), gopurs_runtime.Value{})", """fmt.Println("Main started!")
	gopurs_runtime.Apply(Test_Main.Get_main(), gopurs_runtime.Value{})
	fmt.Println("Main finished applying, waiting for event loop...")""")
code = code.replace('"gopurs/output/gopurs_runtime"', '"gopurs/output/gopurs_runtime"\n\t"fmt"')

with open("output/Test.Main/main/main.go", "w") as f:
    f.write(code)
