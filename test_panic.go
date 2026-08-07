package main
import "unsafe"
type Value struct {
	Type      int
	IntVal    int64
	UnsafePtr unsafe.Pointer
}
func Apply(v Value) {
	panic("hello")
}
func main() {
	Apply(Value{Type: 16, IntVal: 0, UnsafePtr: nil})
}
