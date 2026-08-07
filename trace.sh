#!/bin/bash
sed -i 's/gopurs_runtime.Apply(Test_Main.Get_main(), gopurs_runtime.Value{})/fmt.Println("Main called"); gopurs_runtime.Apply(Test_Main.Get_main(), gopurs_runtime.Value{}); fmt.Println("Main finished")/g' output/Test.Main/main/main.go
