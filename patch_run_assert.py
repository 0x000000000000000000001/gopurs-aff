import sys
with open("output/Test.Main/Test_Main.go", "r") as f:
    content = f.read()

content = content.replace('func Call_runAssertEq__gopurs_runtime_Value_3525359739(dictEq_0_loop gopurs_runtime.Value, s_1_loop string, a_2_loop gopurs_runtime.Value) gopurs_runtime.Value {', '''func Call_runAssertEq__gopurs_runtime_Value_3525359739(dictEq_0_loop gopurs_runtime.Value, s_1_loop string, a_2_loop gopurs_runtime.Value) gopurs_runtime.Value {
	fmt.Printf("Call_runAssertEq called\\n")
''')

content = content.replace('return gopurs_runtime.Apply(pkg_Effect_Aff.Get_runAff_(), gopurs_runtime.Func(func(x_4 gopurs_runtime.Value) gopurs_runtime.Value {', '''res := gopurs_runtime.Apply(pkg_Effect_Aff.Get_runAff_(), gopurs_runtime.Func(func(x_4 gopurs_runtime.Value) gopurs_runtime.Value {
return Call_assertEff(s_1, gopurs_runtime.Apply(__local_var_3_0, x_4))
}))
	fmt.Printf("Call_runAssertEq returns: %+v\\n", res)
	return res''')

content = content.replace('"gopurs/output/gopurs_runtime"', '"gopurs/output/gopurs_runtime"\n\t"fmt"')

with open("output/Test.Main/Test_Main.go", "w") as f:
    f.write(content)
