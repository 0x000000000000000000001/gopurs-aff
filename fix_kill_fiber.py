import re

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace("func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any, _ interface{}) any {\\n\\t_RunFiber(nf, nil)", "func _KillFiber(nf *NativeFiber, errAny error, onError func(any) func(any) any, onSuccess func(any) func(any) any, _ interface{}) any {\\n\\tif ks, ok := nf.Ctx.Value(killErrKey).(*KillState); ok {\\n\\t\\tks.Err = errAny\\n\\t}\\n\\t_RunFiber(nf, nil)")

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
