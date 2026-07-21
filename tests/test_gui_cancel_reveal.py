"""Tests for cancel/failed race handling and the reveal-in-Finder endpoint."""
import pytest

import gui


@pytest.fixture(autouse=True)
def reset_task_state():
    gui.task_state["status"] = "idle"
    gui.task_state["progress"] = 0.0
    gui.task_state["current_segment"] = ""
    gui.task_state["logs"] = []
    gui.task_state["output_file"] = ""
    gui.task_state["error_hint"] = ""
    gui.task_state["workers"] = []
    gui.active_process = None
    yield


def test_finalize_after_cancel_stays_cancelled_not_failed():
    """Simulates the exact race: /cancel flips status to "cancelling", then
    the OS reports SIGTERM's non-zero exit code -- that must not overwrite
    "cancelled" with "failed"."""
    gui.task_state["status"] = "running"
    gui._handle_cancel_request()
    assert gui.task_state["status"] == "cancelling"

    with gui.task_lock:
        gui._finalize_run(-15)  # SIGTERM's exit code arrives late

    assert gui.task_state["status"] == "cancelled"
    assert "Process cancelled by user." in gui.task_state["logs"]


def test_finalize_success_path():
    gui.task_state["status"] = "running"
    with gui.task_lock:
        gui._finalize_run(0)
    assert gui.task_state["status"] == "completed"
    assert gui.task_state["progress"] == 100.0


def test_finalize_nonzero_without_cancel_is_failed_with_hint():
    gui.task_state["status"] = "running"
    gui.task_state["logs"] = ["Low disk space on workspace drive, aborting."]
    with gui.task_lock:
        gui._finalize_run(1)
    assert gui.task_state["status"] == "failed"
    assert "disk space" in gui.task_state["error_hint"]


def test_cancel_when_idle_is_a_noop_status():
    """Cancelling when nothing is running must not fabricate a status."""
    gui.task_state["status"] = "idle"
    gui._handle_cancel_request()
    assert gui.task_state["status"] == "idle"


def test_reveal_only_fires_when_completed_and_file_exists(tmp_path):
    real_output = tmp_path / "video_upscaled.mp4"
    real_output.write_text("fake video")

    gui.task_state["status"] = "running"
    gui.task_state["output_file"] = str(real_output)
    assert gui._resolve_reveal_target() is None  # not completed yet

    gui.task_state["status"] = "completed"
    assert gui._resolve_reveal_target() == str(real_output)


def test_reveal_rejects_when_output_file_missing_or_gone(tmp_path):
    gui.task_state["status"] = "completed"
    gui.task_state["output_file"] = ""
    assert gui._resolve_reveal_target() is None

    missing = tmp_path / "gone.mp4"
    gui.task_state["output_file"] = str(missing)
    assert gui._resolve_reveal_target() is None


def test_classify_failure_falls_back_for_unknown_errors():
    assert gui.classify_failure(["some unrelated traceback"]) == "Something went wrong during processing."
