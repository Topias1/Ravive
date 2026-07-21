"""A frozen bundle re-launches itself; those re-launches are not user input.

In a PyInstaller bundle sys.executable is the app. Anything asking Python for
a helper process therefore restarts the app: multiprocessing's resource
tracker runs "<app> -c 'from multiprocessing.resource_tracker import
main;main(5)'". The CLI branch used to read that code string as a file to
upscale and abort the whole run with FileNotFoundError.

upscale.py already dropped a bare "-c" from argv, which removed the flag but
kept its payload — the half-fix that let this survive.
"""
import subprocess
import sys
from pathlib import Path

import pytest

APP = Path(__file__).resolve().parent.parent / "app.py"


def run_app(args, env_extra=None):
    import os
    env = os.environ.copy()
    env["VIDEO_UPSCALER_CLI"] = "1"
    if env_extra:
        env.update(env_extra)
    return subprocess.run([sys.executable, str(APP)] + args,
                          capture_output=True, text=True, env=env, timeout=60)


def test_resource_tracker_bootstrap_is_not_treated_as_input():
    """The exact re-entry that broke a real run."""
    code = "from multiprocessing.resource_tracker import main;main(5)"
    res = run_app(["-c", code])
    assert "Input path does not exist" not in res.stdout + res.stderr
    assert "FileNotFoundError" not in res.stderr


def test_spawn_bootstrap_is_not_treated_as_input():
    code = "from multiprocessing.spawn import spawn_main; spawn_main(pipe_handle=7)"
    res = run_app(["-c", code])
    assert "Input path does not exist" not in res.stdout + res.stderr


def test_a_real_missing_file_still_reports_clearly():
    """The guard must not swallow genuine bad input."""
    res = run_app(["/nonexistent/clip.mp4"])
    assert "Input path does not exist" in res.stdout + res.stderr


def test_unrelated_dash_c_payload_is_not_executed():
    """Only multiprocessing's own bootstrap is honoured, not any -c payload."""
    res = run_app(["-c", "open('/tmp/ravive_should_not_exist','w')"])
    assert not Path("/tmp/ravive_should_not_exist").exists()
