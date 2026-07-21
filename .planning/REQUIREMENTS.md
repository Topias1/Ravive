# Requirements: Ravive

**Defined:** 2026-07-02
**Core Value:** Providing a 100% self-contained, fully signed and notarized application bundle that delivers fast, high-quality, and robust video upscaling on macOS.

## v1 Requirements (Core & Implemented)

### Core Pipeline (PIPE)

- [x] **PIPE-01**: Video segment splitting & keyframe-aligned chunking.
- [x] **PIPE-02**: Real-ESRGAN Vulkan GPU-accelerated frame upscaling.
- [x] **PIPE-03**: Hardware-accelerated Apple VideoToolbox / NVENC / VAAPI re-encoding.
- [x] **PIPE-04**: Lossless stream preservation, audio remuxing, and metadata copy.

### Resumability & Guards (RESG)

- [x] **RESG-01**: Per-file manifest JSON state tracking for inter-session resume.
- [x] **RESG-02**: Frame-count verification and reconciliation between stages.
- [x] **RESG-03**: VFR to CFR conformance and HDR downscaling guards.

### User Interface (GUI)

- [x] **GUI-01**: Local GUI web server and browser-based pywebview container.
- [x] **GUI-02**: Native file & folder dialog selectors.
- [x] **GUI-03**: Real-time progress bar, ETA, and console log streaming.

### App Packaging (PACK)

- [x] **PACK-01**: Standalone app bundle compilation with PyInstaller.
- [x] **PACK-02**: Apple Developer ID Codesigning.
- [x] **PACK-03**: Automated macOS Apple Gatekeeper Notarization.

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| PIPE-01 | Phase 1: Pipeline | Complete |
| PIPE-02 | Phase 1: Pipeline | Complete |
| PIPE-03 | Phase 1: Pipeline | Complete |
| PIPE-04 | Phase 1: Pipeline | Complete |
| RESG-01 | Phase 2: Resilience | Complete |
| RESG-02 | Phase 2: Resilience | Complete |
| RESG-03 | Phase 2: Resilience | Complete |
| GUI-01 | Phase 3: Interface | Complete |
| GUI-02 | Phase 3: Interface | Complete |
| GUI-03 | Phase 3: Interface | Complete |
| PACK-01 | Phase 4: Packaging | Complete |
| PACK-02 | Phase 4: Packaging | Complete |
| PACK-03 | Phase 4: Packaging | Complete |

**Coverage:**
- v1 requirements: 13 total
- Mapped to phases: 13
- Unmapped: 0 ✓

---
*Requirements defined: 2026-07-02*
*Last updated: 2026-07-02 after codesign and notarization implementation*
