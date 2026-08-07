sed -i '' -e 's/acquireCtx := context\.WithoutCancel(ctx)/if ctx\.Err() != nil { return nil, context\.Cause(ctx) }\n\n\t\tacquireCtx := context\.WithoutCancel(ctx)/' src/Effect/Aff.go
