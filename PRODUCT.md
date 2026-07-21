# Product

## Register

product

## Users

Four audiences share one screen, in rough order of how forgiving they are:

- **People restoring old footage** — family archives, VHS rips, decade-old phone video. Non-technical, one file at a time, do not know what Real-ESRGAN is and should not need to. They judge the app by whether it finished and whether the result looks better.
- **Anime / animation upscalers** — know the models by name, choose deliberately between `realesr-animevideov3` and `x4plus`, batch whole folders recursively.
- **Prosumer / semi-pro video** — comfortable with codecs, presets, encoders; want the pipeline's control surface reachable without dropping to the CLI.
- **The author and friends** — this is also a personal tool. Its own workflow is a legitimate design input.

Shared context: a local macOS window (900×750, min 800×650), on a laptop, running a
job that takes **20-60 minutes** unattended. The user starts it and walks away. They
come back to a screen that must immediately answer four questions.

## Product Purpose

Ravive upscales video to 4K locally with Real-ESRGAN + ffmpeg — no cloud upload, no
per-minute pricing, resumable at file and chunk granularity. The GUI is a thin,
honest window onto a CLI pipeline that already works.

Success: a stranger downloads the DMG, drops in a file, presses one button, and an
hour later has a better video — having, at every moment in between, been able to tell
that the machine was alive and how far along it was.

## Brand Personality

**Warm, approachable, native.** A good Mac utility. Plain language over jargon,
generous spacing, system control vocabulary. It should feel like it shipped with the
OS, not like a web app in a window.

Voice: direct and human. "Cancelled" not "FAILED". "Reduce flickering" before
"temporal denoise". Never cute, never celebratory, never apologetic.

References, and the specific thing taken from each:

- **Native macOS (Preview, Shortcuts, Transmit)** — system font, system controls,
  no invented affordances, correct dark-mode form rendering.
- **Raycast / Linear** — restrained neutrals, one accent reserved for state, a tight
  type scale, obsessive alignment.
- **Pro video tools (Resolve, Compressor)** — dense job readouts, tabular numerals,
  per-item progress that tells the truth about the queue.

## Anti-references

- **Ravive's own current look** — indigo→cyan gradient text, glow shadows,
  backdrop-filter glass, radial background blobs, Outfit @ 800, emoji icons. All eight
  tells from the 2026-07-21 audit are explicitly retired, not softened.
- **Generic AI SaaS dashboard** — purple gradients, hero metrics, identical rounded
  cards, decorative accent everywhere.
- **Topaz Video AI** — the direct competitor: every panel visible at once, nothing
  prioritized, the user left to rank the controls themselves.
- **Cutesy consumer apps** — bouncy springs, playful copy, confetti on completion.
  A one-hour job ending is a fact, not a party.

## Design Principles

1. **Always answerable.** At any instant the window answers: is it alive, how far in,
   how much longer, did anything break. No state may leave one of those unanswered —
   that is the single job of the running screen.
2. **Native before invented.** Use the platform's vocabulary for anything standard
   (file pickers, controls, focus, dark mode). Invention is reserved for what the
   platform has no answer to — per-segment progress across a chunked pipeline.
3. **Defaults carry the novice; depth never blocks them.** The family-archive user
   should succeed touching only two controls. The prosumer's controls exist but never
   stand between the novice and the button.
4. **Honest about the machine.** Real segment, stage, and ETA data or nothing. No
   synthetic progress, no spinner standing in for information, and cancelled is not
   failed.
5. **Quiet under load.** This window is open for an hour. Nothing pulses, glows,
   drifts, or asks for attention. Motion exists only to explain a state change.

## Accessibility & Inclusion

Target: **WCAG 2.2 AA, plus full keyboard operation and VoiceOver support.**

- All text ≥4.5:1 (≥3:1 for large), placeholders included.
- Visible focus indicator on every interactive element; no keyboard traps; the file
  browser fallback must be escapable and focus-managed.
- Progress, stage changes, completion, and failure announced via live regions — a
  screen-reader user must not have to poll a silent screen for 40 minutes.
- `prefers-reduced-motion` honored on every transition.
- `color-scheme: dark` declared so native controls render correctly.
- Status never encoded by color alone (badge text carries the state).
