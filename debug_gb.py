with open("src/Effect/Aff.go", "r") as f:
    lines = f.read()

lines = lines.replace('''				killErr := getKillError(ctx, ctx.Err())
				killedBox := gopurs_runtime.RecordGet(optionsVal, "killed")
				cleanupBox := gopurs_runtime.Apply2(killedBox, gopurs_runtime.Box(killErr), gopurs_runtime.Box(resource))''', '''				killErr := getKillError(ctx, ctx.Err())
				killedBox := gopurs_runtime.RecordGet(optionsVal, "killed")
				fmt.Printf("killedBox: %T\n", killedBox.UnsafePtr)
				cleanupBox := gopurs_runtime.Apply2(killedBox, gopurs_runtime.Box(killErr), gopurs_runtime.Box(resource))''')

with open("src/Effect/Aff.go", "w") as f:
    f.write(lines)
