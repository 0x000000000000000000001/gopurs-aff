import subprocess
import sys

scripts = [
"restore.py",
"fix_kill_success2.py",
"fix_kill_start.py",
"fix_kill_err2.py",
"fix_cancel_cause.py",
"fix_catch_bracket2.py",
"fix_bracket3.py",
"fix_bracket4.py",
"fix_bracket5.py",
"fix_bracket6.py",
"fix_err.py",
"fix_supervise.py",
"fix_fork_aff.py",
"fix_kill_all.py",
"fix_kill_test.py",
"fix_make_aff.py",
"fix_bracket.py",
"fix_all.py",
"fix_runfiber2.py",
"fix_runfiber3.py",
"fix_runfiber4.py",
"fix_ctx_err.py",
"fix_fork_sup.py",
"fix_killall.py",
"fix_box.py",
"fix_fork_sup2.py",
"patch_supervise.py",
"fix_sup_ctx.py",
"fix_sup_ctx2.py",
"fix_final3.py",
"fix_missing_types.py",
"fix_make_run_join.py",
]

for s in scripts:
    print(f"Running {s}")
    subprocess.run(["python3", s], check=True)
