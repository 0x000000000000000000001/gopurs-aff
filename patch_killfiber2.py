import sys

with open("output/Effect.Aff/Effect_Aff_ffi.go", "r") as f:
    content = f.read()

old_func = """				// If it died with the kill error (or successfully despite kill), kill succeeds!
				import_unit := gopurs_runtime.Apply(gopurs_runtime.RecordGet(gopurs_runtime.RecordDict0(), "a"), gopurs_runtime.Any(nil)) // dummy
				_ = import_unit
				// Just pass nil to onSuccess, it ignores the value since it's Unit
				onSuccess(nil)(nil)"""

new_func = """				// If it died with the kill error (or successfully despite kill), kill succeeds!
				onSuccess(nil)(nil)"""

content = content.replace(old_func, new_func)

with open("output/Effect.Aff/Effect_Aff_ffi.go", "w") as f:
    f.write(content)
