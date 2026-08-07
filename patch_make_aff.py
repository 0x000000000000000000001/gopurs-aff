import sys

with open("src/Effect/Aff.go", "r") as f:
    content = f.read()

content = content.replace('cancelerEffect := build(onError)(onSuccess)', 'fmt.Printf("CANCELER EFFECT TYPE: %T\\n", build(onError)(onSuccess))\n\t\tcancelerEffect := build(onError)(onSuccess)')

with open("src/Effect/Aff.go", "w") as f:
    f.write(content)
