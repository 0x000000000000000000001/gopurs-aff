package main

import (
	"context"
	"fmt"
)

func main() {
	var ctx context.Context = context.Background()
	ctx2 := context.WithoutCancel(ctx)
	fmt.Printf("%T\n", ctx2)
}
