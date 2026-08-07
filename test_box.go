package main

import (
	"context"
	"fmt"
	"gopurs-aff/output/gopurs_runtime"
)

type AffFn = func(context.Context) (any, error)

func main() {
	var f any = func(ctx context.Context) (any, error) { return nil, nil }
	val := gopurs_runtime.Box(f)
	fmt.Printf("Boxed type: %v\n", val.Type)
	
	defer func() {
		if r := recover(); r != nil {
			fmt.Printf("Recovered in unbox: %v\n", r)
		}
	}()
	
	unboxed := gopurs_runtime.Unbox[AffFn](val)
	fmt.Printf("Unboxed successfully: %T\n", unboxed)
}
