package main

import (
	"context"
	"fmt"
)

type AffFn = func(context.Context) (any, error)

func main() {
	var go_res any = func(ctx context.Context) (any, error) { return nil, nil }
	var ptr = &go_res
	
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("Recovered: %v\n", r)
		}
	}()
	
	val := (*(*any)(ptr)).(AffFn)
	fmt.Printf("Success: %T\n", val)
}
