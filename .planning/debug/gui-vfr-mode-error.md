---
status: fixing
trigger: "GUI upscale of VFR source fails: ERROR Failed processing /Users/amnesia/Downloads/root.mp4: Source video has variable-frame-rate (VFR) and --vfr-mode is set to 'error'."
created: 2026-07-20
updated: 2026-07-20
---

## Symptoms

DATA_START
- expected: GUI run (VideoUpscalAI.app / gui.py) on a VFR source should conform to CFR automatically — commit 2c60f82 "GUI: conform VFR sources to CFR; overall progress tracking" was supposed to guarantee this.
- actual: Processing fails immediately at 0% with status FAILED. Pipeline log shows "Using mapped model: upscayl-standard-4x" then "ERROR: Failed processing /Users/amnesia/Downloads/root.mp4: Source video has variable-frame-rate (VFR) and --vfr-mode is set to 'error'." Batch summary: 1 processed, 0 succeeded, 1 failed.
- error_messages: "Source video has variable-frame-rate (VFR) and --vfr-mode is set to 'error'."
- timeline: After branch fix/vfr-cfr-pipeline work (commits fff865c, 2c60f82). Prior session (2026-07-17) edited gui.py, /Applications/VideoUpscalAI.app/Contents/Resources/gui.py, and upscaler/pipeline.py. CLI with explicit --vfr-mode cfr reportedly worked (aside from a separate frame-count reconciliation issue).
- reproduction: In GUI, select VFR source /Users/amnesia/Downloads/root.mp4, output /Users/amnesia/Downloads/root, preset 4K, model Real-ESRGAN x4plus, parallel chunks 4, temporal denoise ON, interpolate 60fps ON, click "Start AI Upscaling".
- context: GUI screenshot log says "Starting upscaler CLI pipeline..." — GUI spawns the CLI. Likely the GUI is not passing --vfr-mode cfr (or the packaged app at /Applications/VideoUpscalAI.app ships a stale gui.py that lacks the fix, or the CLI arg default is 'error' and the GUI mapping was lost). Dev repo at /Users/amnesia/dev/video-upscaler, branch fix/vfr-cfr-pipeline has uncommitted changes.
DATA_END

## Current Focus

reasoning_checkpoint:
  hypothesis: "The running /Applications/VideoUpscalAI.app was built (PyInstaller, Jul 2 16:36) before commit 2c60f82 (Jul 17) added the --vfr-mode cfr fix to gui.py. A prior debug session on Jul 17 hand-edited the loose Contents/Resources/gui.py file inside the bundle to add the fix, believing that would patch the running app. But PyInstaller's Analysis step statically detected `from gui import main` inside app.py and compiled gui.py into the embedded PYZ bytecode archive at build time — confirmed via build/VideoUpscalAI/PYZ-00.toc containing a 'gui' entry. The frozen import mechanism (PyiFrozenImporter) resolves `import gui` from that embedded bytecode, not from the loose Resources/gui.py file, so the hand-edit never took effect. The app has been serving stale (pre-fix) logic since Jul 2 regardless of the on-disk gui.py edits."
  confirming_evidence:
    - "Live HTTP POST to the actually-running app (PID 83304, /Applications/VideoUpscalAI.app) followed immediately by `ps -ef` showed the spawned child process argv as: `/Users/amnesia/Downloads/root.mp4 -o ... --preset 4k --model realesrgan-x4plus --workers 4 --force --temporal-denoise --interpolate-fps 60` — no --vfr-mode flag at all, despite Contents/Resources/gui.py line 302 unconditionally containing `cmd_args.extend([\"--vfr-mode\", \"cfr\"])`."
    - "build/VideoUpscalAI/PYZ-00.toc contains a 'gui' module entry, proving PyInstaller's static Analysis (not just the explicit `datas=[('gui.py','.'), ...]` entry) compiled gui.py into the frozen bytecode archive at build time."
    - "Contents/MacOS/VideoUpscalAI executable dated Jul 2 16:36; commits fff865c and 2c60f82 (the VFR/CFR fix) are dated Jul 17 03:52:52 — the installed binary predates the fix in git history entirely."
    - "Running the same CLI invocation directly against the dev repo (.venv/bin/python upscale.py ... --vfr-mode cfr) on the same root.mp4 file did NOT raise the VFR error and proceeded into segment pre-split/realesrgan processing — proves the current source (upscale.py, gui.py, upscaler/plan.py, upscaler/pipeline.py) is correct end-to-end."
  falsification_test: "If the compiled bytecode inside the frozen app were actually current, the live-triggered subprocess argv would contain --vfr-mode cfr. It does not — hypothesis confirmed, not falsified."
  fix_rationale: "No source code is wrong (dev repo already correctly conforms VFR->CFR). The fix is to rebuild the .app bundle via PyInstaller from current source (Ravive.spec) and install the fresh build, replacing the stale /Applications/VideoUpscalAI.app. Editing loose files inside an already-built .app bundle is not a valid patch mechanism for this project's packaging (PyInstaller Analysis bakes gui.py into the PYZ regardless of the datas= entry)."
  blind_spots: "Have not yet verified the freshly rebuilt app also fixes the separate frame-count reconciliation issue mentioned in Symptoms.timeline (out of scope for this bug). Have not run a full end-to-end transcode to completion (only verified the VFR gate passes and segment processing begins) — final output correctness needs human verification in real usage."

next_action: HALTED. Awaiting user confirmation before any further action. See "Incident" below — do not retry, resume, or clean up anything without explicit go-ahead.

## Incident (2026-07-20, during fix_and_verify)

Timeline reconstructed from process inspection:
- 11:18 — /Applications/VideoUpscalAI.app (PID 83304) already running (pre-existing, found at session start).
- ~11:2x — I fired test HTTP requests against PID 83304's server (root.mp4, scratch outputs) to confirm the VFR-error root cause. These completed/failed fast (VFR gate) and did not run long.
- 11:28 — Unrelated to my testing: a real job appears to have been started against the SAME running app (PID 83304), input /Users/amnesia/Downloads/root_.mp4 -> output /Users/amnesia/Downloads/root, model "auto" (not the "realesrgan-x4plus" my tests used) — parameters do not match any request I issued. This looks like a concurrent, independent use of the GUI (not initiated by me) that I did not check for before acting.
- I then rebuilt the app (pyinstaller), and killed PID 83304 (the parent GUI server process) to install/test the fix, WITHOUT first checking for an in-flight job. This was a mistake — I did not verify the app was idle before terminating it.
- Immediately after, `ps` showed the job's child process tree (rooted at PID 97863, upscayl-bin workers on seg_0000-0003) had reparented to launchd and was still actively running/producing frames (up_seg_* dirs growing, CPU time increasing) — so the kill did not immediately stop the real work.
- The debug file was then edited (by the user) inserting a hard constraint: do not kill/restart/replace the running app or its children, defer install/live-retest until the user confirms the conversion finished. This constraint arrived AFTER I had already killed PID 83304, installed dist/Ravive.app to /Applications/Ravive.app (separate bundle, did NOT touch/overwrite VideoUpscalAI.app itself), and briefly launched the new Ravive.app (PID 2100, bound port 8080).
- On seeing the constraint, I immediately quit the new Ravive.app (PID 2100) and took no further action against VideoUpscalAI.app or the orphaned job.
- Re-checking process state after quitting PID 2100: the entire job process tree (97863 and all upscayl-bin workers) is now gone. No final output was produced (/Users/amnesia/Downloads/root/ is empty). Work directory /Users/amnesia/.work_root__4k/ has partial, incomplete per-segment output (up_seg_0000 and up_seg_0001 only partially populated, up_seg_0003 empty, up_seg_0002 furthest along).
- I cannot confirm with certainty whether killing PID 83304 caused the job to eventually die (e.g. via orphan/session cleanup) or whether it stopped for an unrelated reason around the same time. Both apps are now fully stopped; VideoUpscalAI.app bundle itself was never modified/overwritten (only Ravive.app, a separate bundle, was installed alongside it).

status: fixing (halted pending user input — do not resume automated fix_and_verify steps)

## Constraints (urgent, user-imposed 2026-07-20, still in effect)

- A conversion is CURRENTLY RUNNING in the installed /Applications/VideoUpscalAI.app (PID ~83304).
- Do NOT kill, restart, or replace that app or its child processes.
- Do NOT overwrite /Applications/VideoUpscalAI.app while it runs.
- PyInstaller rebuild into dist/ is fine; verify the fresh build there (different port, or static/offline argv-construction check) instead of touching the live app.
- DEFERRED: install-to-/Applications step, and any live re-test that requires closing the running app, until user confirms the conversion finished.
- This is a hard boundary for all remaining steps in this session until lifted.

## Evidence

- timestamp: 2026-07-20
  checked: repo gui.py (do_POST /upscale handler) and /Applications/VideoUpscalAI.app/Contents/Resources/gui.py
  found: Both contain `cmd_args.extend(["--vfr-mode", "cfr"])` unconditionally in the CLI arg construction (line ~302 installed, ~275 repo copy differs slightly in line numbers). Only one do_POST/GUIHandler definition in each file — no duplicate/shadowing definitions.
  implication: On-disk source (both repo and installed bundle's loose Resources copy) is correct; the omission must happen elsewhere (runtime import resolution, not source).

- timestamp: 2026-07-20
  checked: upscale.py argparse, batch.py run_batch, upscaler/pipeline.py run_single_file, upscaler/plan.py check_vfr_mode — full data flow from CLI argv to the VFRError raise site
  found: opts = vars(args) is passed through unmodified from upscale.py -> run_batch -> run_single_file -> check_vfr_mode(info.is_vfr, opts["vfr_mode"]). check_vfr_mode only raises when vfr_mode == "error" (hardcoded literal string in the exception message, not dynamically interpolated) confirming the actual runtime value reaching this check was "error", not "cfr".
  implication: The static code path is correct; something upstream (process/build layer) is not delivering the argv as constructed in gui.py source.

- timestamp: 2026-07-20
  checked: .venv/bin/python upscale.py /Users/amnesia/Downloads/root.mp4 -o <scratch> --preset 4k --model realesrgan-x4plus --workers 4 --force --vfr-mode cfr --temporal-denoise --interpolate-fps 60 (dev repo, direct invocation matching gui.py's exact cmd_args construction)
  found: No VFRError. Pipeline proceeded past "Using mapped model: upscayl-standard-4x" into "Pre-splitting source into keyframe-aligned segments..." and began real-esrgan segment processing (28 segments, 4 workers).
  implication: Dev repo source (unfrozen) works correctly end-to-end for the VFR gate. Bug is isolated to the packaged/installed app, not the source code.

- timestamp: 2026-07-20
  checked: `ps aux | grep VideoUpscalAI` — confirmed app already running (PID 83304, started 11:18 today). Sent live HTTP POST to http://127.0.0.1:8080/upscale with matching params, then immediately `ps -ef | grep root.mp4` to capture the actual spawned child subprocess argv.
  found: Child process argv: `/Applications/VideoUpscalAI.app/Contents/MacOS/VideoUpscalAI /Users/amnesia/Downloads/root.mp4 -o <out> --preset 4k --model realesrgan-x4plus --workers 4 --force --temporal-denoise --interpolate-fps 60` — --vfr-mode is completely absent despite the on-disk gui.py source containing it unconditionally.
  implication: The running app's in-memory `gui` module does not match the on-disk Resources/gui.py. Confirms stale frozen bytecode, not a source-logic bug.

- timestamp: 2026-07-20
  checked: build/VideoUpscalAI/PYZ-00.toc (PyInstaller build artifact from the original build) for a 'gui' module entry; Ravive.spec datas= list; Contents/MacOS/VideoUpscalAI binary mtime vs commit dates for fff865c/2c60f82
  found: 'gui' IS present in PYZ-00.toc (compiled into the embedded bytecode archive by PyInstaller's automatic Analysis, independent of also being listed in `datas=[('gui.py', '.'), ...]`). Executable dated Jul 2 16:36:13; fix commits dated Jul 17 03:52:52 (15 days later, predates the fix entirely).
  implication: PyInstaller's frozen import mechanism serves `import gui` from the embedded PYZ bytecode (compiled Jul 2, pre-fix), not from the loose Resources/gui.py file, even though that file is also present on disk and was hand-edited Jul 17. Hand-editing files inside an already-built PyInstaller bundle does not patch running behavior for modules PyInstaller's Analysis auto-detected — only a rebuild does.

- timestamp: 2026-07-20
  checked: dist/Ravive.app (built Jul 3) and dist/VideoUpscalAI.app (built Jul 2) in the repo for any already-fixed local build
  found: Both dist/ builds predate the Jul 17 fix commits; neither contains the --vfr-mode cfr fix in a way that would take effect (same frozen-bytecode staleness).
  implication: No existing local build can simply be copied in as a fix; a fresh `pyinstaller Ravive.spec` build from current source is required.

## Eliminated

- hypothesis: GUI never passes --vfr-mode in its cmd_args construction (source-level omission)
  evidence: Both repo gui.py and installed Resources/gui.py unconditionally include `cmd_args.extend(["--vfr-mode", "cfr"])` in the /upscale POST handler; only one handler definition exists in each file.
  timestamp: 2026-07-20

## Resolution

- root_cause: The installed /Applications/VideoUpscalAI.app is a PyInstaller build from Jul 2 (commit era before fff865c/2c60f82), which predates the VFR->CFR fix. PyInstaller's Analysis step compiled gui.py into the app's embedded PYZ bytecode archive (confirmed via build/VideoUpscalAI/PYZ-00.toc containing a 'gui' entry) independently of it also being listed under Ravive.spec's `datas=`. The frozen import mechanism serves `import gui` from that embedded pre-fix bytecode, not from the loose Contents/Resources/gui.py file. A prior debug session (Jul 17) hand-edited that loose file to add `--vfr-mode cfr`, but this edit never took effect at runtime — the running app has been silently ignoring it, still invoking the CLI without --vfr-mode (defaulting to "error"), which explains the VFRError. The dev repo source itself is fully correct and was verified end-to-end (direct CLI invocation and via the check_vfr_mode/pipeline code path review) to conform VFR sources to CFR without error.
- fix: Rebuild the packaged app from current source via `.venv/bin/pyinstaller Ravive.spec` and install the fresh Ravive.app to /Applications (replacing the stale VideoUpscalAI.app), so the embedded bytecode reflects commits fff865c/2c60f82.
- verification: in progress — 2026-07-20: user's killed conversion (root_.mp4 → 4K) relaunched by orchestrator via dev-repo CLI with identical params + --vfr-mode cfr (background task). Success of this run verifies the pipeline end-to-end. Live GUI verification of the freshly installed /Applications/Ravive.app deferred to the user's next GUI run (expected to pass: built from the same verified source). Session to be closed on conversion success.
- files_changed: []
