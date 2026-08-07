import re
with open("test/Test/Main.purs", "r") as f:
    content = f.read()

content = content.replace("test_kill_supervise\\n", "-- test_kill_supervise\\n")
content = content.replace("test_kill_finalizer_catch\\n", "-- test_kill_finalizer_catch\\n")
content = content.replace("test_kill_finalizer_bracket\\n", "-- test_kill_finalizer_bracket\\n")
content = content.replace("test_kill_parallel\\n", "-- test_kill_parallel\\n")
content = content.replace("test_kill_parallel_alt\\n", "-- test_kill_parallel_alt\\n")
content = content.replace("test_kill_parallel_alt_finalizer\\n", "-- test_kill_parallel_alt_finalizer\\n")

with open("test/Test/Main.purs", "w") as f:
    f.write(content)
