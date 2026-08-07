import sys

with open("src/Effect/Aff.go", "r") as f:
    code = f.read()

code = code.replace("<-nf.DoneonSuccess(nil)(nil)", "<-nf.Done\n\t\t\tonSuccess(nil)(nil)")

with open("src/Effect/Aff.go", "w") as f:
    f.write(code)
