# Roadmap: Ravive

## Overview

The journey from a baseline CLI script upscaler to a fully robust, resumable, hardware-accelerated GUI application on macOS, compiled, signed, and notarized for Apple Gatekeeper.

## Phases

- [x] **Phase 1: Pipeline** - Core frame extraction, Real-ESRGAN upscaling, and re-encoding.
- [x] **Phase 2: Resilience** - Per-file resume manifests, frame reconciliation, and error handling.
- [x] **Phase 3: Interface** - Local python web server and native pywebview GUI desktop window.
- [x] **Phase 4: Packaging** - PyInstaller application bundling, developer ID codesigning, and Apple notarization.

## Phase Details

### Phase 1: Pipeline
**Goal**: Core video splitting, frame upscaling, re-encoding, and stream concatenation/remuxing.
**Depends on**: Nothing
**Requirements**: PIPE-01, PIPE-02, PIPE-03, PIPE-04
**Success Criteria**:
  1. User can run upscale pipeline via CLI on a video file.
  2. Audio and metadata are losslessly preserved.
**Plans**: 1 plan

Plans:
- [x] 01-01: Implement CLI split-upscale-encode-concat pipeline.

### Phase 2: Resilience
**Goal**: Segment state caching, frame verification, variable frame rate and HDR protection guards.
**Depends on**: Phase 1
**Requirements**: RESG-01, RESG-02, RESG-03
**Success Criteria**:
  1. Aborted jobs can resume exactly from the interrupted segment.
  2. Frame drops or mismatches are reconciled.
**Plans**: 1 plan

Plans:
- [x] 02-01: Build JSON manifest resume layer and frame verification guards.

### Phase 3: Interface
**Goal**: User-friendly UI with progress indicators, native file dialogs, and subprocess streaming.
**Depends on**: Phase 2
**Requirements**: GUI-01, GUI-02, GUI-03
**Success Criteria**:
  1. User can choose files/folders and click "Start" in a native window.
  2. Real-time stdout progress is parsed and rendered in UI.
**Plans**: 1 plan

Plans:
- [x] 03-01: Implement webview UI container and local HTTP controller.

### Phase 4: Packaging
**Goal**: Standalone DMG package creation, code signature integration, and Apple Gatekeeper validation.
**Depends on**: Phase 3
**Requirements**: PACK-01, PACK-02, PACK-03
**Success Criteria**:
  1. Packaged app works without python environment or dependencies installed.
  2. DMG mounts and launches without Gatekeeper warnings.
**Plans**: 1 plan

Plans:
- [x] 04-01: Implement PyInstaller packaging, signing script, and notarization check.

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Pipeline | 1/1 | Complete | 2026-07-02 |
| 2. Resilience | 1/1 | Complete | 2026-07-02 |
| 3. Interface | 1/1 | Complete | 2026-07-02 |
| 4. Packaging | 1/1 | Complete | 2026-07-02 |
