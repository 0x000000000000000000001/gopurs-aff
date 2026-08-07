with open("src/Effect/Aff.go", "r") as f:
    lines = f.read()

import re
lines = re.sub(r'killedBox: %T.*\\n"', r'killedBox: %T\\n"', lines, flags=re.DOTALL)

# Let me just revert the whole thing!
