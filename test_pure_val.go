package main

import (
	"fmt"
	"gopurs/output/Test.Main"
)

func main() {
	val := Test_Main.Get_test_pure()
	fmt.Printf("Get_test_pure returned: %+v\n", val)
}
