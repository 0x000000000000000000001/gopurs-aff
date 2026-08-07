import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

import re
content = re.sub(r'cancelFnAff := canceler\(fmt\.Errorf\("context canceled"\)\)\n\t\t\tgo runAffSync\(cancelFnAff, context\.Background\(\)\)', 'cancelFnAff := canceler(context.Cause(ctx))\n\t\t\t_, _ = runAffSync(cancelFnAff, context.Background())', content)

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)

