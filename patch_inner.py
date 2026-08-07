import re

path = 'output/Effect.Aff/Effect_Aff_ffi.go'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('"context"', '"context"\n\t"os"')

target = """\t\t\tinner_res3 := gopurs_runtime.Apply(inner_res2, gopurs_runtime.Box(p3_0))
\t\t\treturn gopurs_runtime.Unbox[AffFn](inner_res3)"""
replacement = """\t\t\tinner_res3 := gopurs_runtime.Apply(inner_res2, gopurs_runtime.Box(p3_0))
\t\t\tfmt.Printf("DEBUG inner_res3: Type=%v, UnsafePtr=%v\\n", inner_res3.Type, inner_res3.UnsafePtr)
\t\t\tos.Stdout.Sync()
\t\t\treturn gopurs_runtime.Unbox[AffFn](inner_res3)"""

content = content.replace(target, replacement)
with open(path, 'w') as f:
    f.write(content)
