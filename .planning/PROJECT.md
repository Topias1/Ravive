# Ravive

## What This Is

A robust, resumable desktop app and CLI pipeline for macOS that upscales videos using Real-ESRGAN-ncnn-vulkan (GPU-accelerated inference) for frame upscaling and ffmpeg for demuxing, downscaling, and hardware-accelerated re-encoding.

## Core Value

Providing a 100% self-contained, fully signed and notarized application bundle that delivers fast, high-quality, and robust video upscaling on macOS.

## Requirements

### Validated

- ✓ Local GUI server and browser-based pywebview desktop interface — existing
- ✓ Keyframe-aligned chunking and pipeline (split, upscale, encode, concat, remux) — existing
- ✓ Per-file manifest JSON resumability and frame-count reconciliation — existing
- ✓ Hardware-accelerated Apple VideoToolbox / NVENC / VAAPI re-encoding — existing
- ✓ macOS codesigning and notarization build pipeline — existing

### Active

- [ ] [Feature 1] Define upcoming active features here

### Out of Scope

- [Exclusion 1] — None defined yet

## Context

- Technical ecosystem: macOS Apple Silicon, Python 3.14, PyInstaller bundles.
- Includes pre-compiled universal realesrgan-ncnn-vulkan and static ffmpeg/ffprobe binaries.

## Constraints

- **Tech Stack**: PyInstaller for packaging, pywebview for GUI, subprocess-based CLI invocation.
- **Hardware**: Vulkan-capable GPU required (Apple Silicon / Metal virtualization).

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Codesigning & Notarization | Gatekeeper security bypass for macOS users. | ✓ Good |
| Subprocess realesrgan CLI | Avoid C++ driver deadlock issues under multi-threaded Python. | ✓ Good |

---
*Last updated: 2026-07-02 after project rename & notarization*
