import sys
with open("output/Test.Main/main/main.go", "r") as f:
    content = f.read()

content = content.replace('func main() {', 'func main() {\n\tprintln("MAIN STARTED")')
content = content.replace('gopurs_runtime.EventLoopWait()', 'println("WAITING")\n\tgopurs_runtime.EventLoopWait()\n\tprintln("WAIT DONE")')

with open("output/Test.Main/main/main.go", "w") as f:
    f.write(content)
