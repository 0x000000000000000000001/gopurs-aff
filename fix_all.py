import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

import re

# Fix cancelFnAff
content = re.sub(r'cancelFnAff := canceler\(fmt\.Errorf\("context canceled"\)\)\n\t\t\tgo runAffSync\(cancelFnAff, context\.Background\(\)\)', 'cancelFnAff := canceler(context.Cause(ctx))\n\t\t\t_, _ = runAffSync(cancelFnAff, context.Background())', content)

# Fix GeneralBracket ctx.Err()
content = re.sub(r'acquireFn := gopurs_runtime\.Unbox\[AffFn\]\(acquireVal\)\n\t\t\n\t\tacquireCtx := context\.WithoutCancel\(ctx\)', 'acquireFn := gopurs_runtime.Unbox[AffFn](acquireVal)\n\t\t\n\t\tif ctx.Err() != nil {\n\t\t\treturn nil, context.Cause(ctx)\n\t\t}\n\t\t\n\t\tacquireCtx := context.WithoutCancel(ctx)', content)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
