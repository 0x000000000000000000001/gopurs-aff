import sys
with open("output/Test.Main/main/main.go", "r") as f:
    content = f.read()

content = content.replace('''f := gopurs_runtime.Apply(Test_Main.Get_main(), gopurs_runtime.Value{})
	for f.Type == gopurs_runtime.TypeFunc {
		f = gopurs_runtime.Apply(f, gopurs_runtime.Value{})
	}''', 'gopurs_runtime.Apply(Test_Main.Get_main(), gopurs_runtime.Value{})')

with open("output/Test.Main/main/main.go", "w") as f:
    f.write(content)
