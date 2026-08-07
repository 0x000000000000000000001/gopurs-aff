import sys

with open("output/Test.Main/Test_Main.go", "r") as f:
    content = f.read()

content = content.replace("func Get_test_pure() gopurs_runtime.Value {", "func Get_test_pure() gopurs_runtime.Value {\n\tprintln(\"Get_test_pure CALLED\")")

with open("output/Test.Main/Test_Main.go", "w") as f:
    f.write(content)
