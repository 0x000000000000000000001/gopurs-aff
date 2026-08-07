import re

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

# 1. Replace NativeFiber.Cancel type
code = code.replace("Cancel     context.CancelFunc", "Cancel     context.CancelCauseFunc")

# 2. Update _MakeFiberNative
# We need to replace ctx, cancel := context.WithCancel(context.Background())
# And remove the KillState stuff!
pattern_make = r'ctx, cancel := context\.WithCancel\(context\.Background\(\)\)\n\t\tctx = context\.WithValue\(ctx, killErrKey, &KillState\{\}\)'
code = re.sub(pattern_make, 'ctx, cancel := context.WithCancelCause(context.Background())', code)

# 3. Update _KillFiber
# nf.Cancel() -> nf.Cancel(errAny)
code = code.replace("nf.Cancel()\n\tselect {", "nf.Cancel(errAny)\n\tselect {")

# 4. Remove getKillError and KillState
pattern_killstate = r'type key int.*?func getKillError.*?return defaultErr\n\}'
code = re.sub(pattern_killstate, '', code, flags=re.DOTALL)

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
