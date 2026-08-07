package main
import "fmt"
import "gopurs/output/gopurs_runtime"

func main() {
	fmt.Printf("%#v\n", gopurs_runtime.Box(nil))
}
