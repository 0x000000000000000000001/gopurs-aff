package main
import "fmt"
func main() {
	f := func(any) func(any) func(any) any {
		return func(any) func(any) any {
			return func(any) any {
				return func(any) any { return nil }
			}
		}
	}
	res := f(nil)(nil)
	res2 := res(nil)
	fmt.Printf("%T\n", res2)
}
