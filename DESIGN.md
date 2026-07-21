---
version: "1.0.0"
name: "Ravive GUI"
description: >
  Visual system for the single-page pywebview UI served from HTML_CONTENT in
  gui.py. Dark-only. No build step, no framework — this file documents the
  CSS custom properties and markup exactly as written in that string.
colors:
  bg:              "oklch(0.155 0.006 250)"
  surface-1:       "oklch(0.205 0.006 250)"
  surface-2:       "oklch(0.235 0.008 250)"
  surface-3:       "oklch(0.125 0.004 250)"
  border:          "oklch(0.520 0.008 250)"
  border-subtle:   "oklch(0.260 0.006 250)"
  text-primary:    "oklch(0.930 0.006 250)"
  text-secondary:  "oklch(0.780 0.008 250)"
  text-muted:      "oklch(0.685 0.010 250)"
  text-disabled:   "oklch(0.400 0.006 250)"
  accent:          "oklch(0.780 0.150 72)"
  accent-hover:    "oklch(0.830 0.140 72)"
  accent-active:   "oklch(0.720 0.160 72)"
  on-accent:       "oklch(0.160 0.010 72)"
  danger:          "oklch(0.720 0.160 25)"
  danger-hover:    "oklch(0.770 0.150 25)"
  idle-surface:       "oklch(0.235 0.006 250)"
  idle-text:          "oklch(0.700 0.008 250)"
  running-surface:    "oklch(0.270 0.055 72)"
  running-text:       "oklch(0.820 0.150 72)"
  completed-surface:  "oklch(0.270 0.050 155)"
  completed-text:     "oklch(0.800 0.150 155)"
  failed-surface:     "oklch(0.270 0.065 25)"
  failed-text:        "oklch(0.780 0.170 25)"
  cancelled-surface:  "oklch(0.235 0.008 250)"
  cancelled-text:     "oklch(0.780 0.012 250)"
  terminal-bg:     "{colors.surface-3}"
  terminal-text:   "oklch(0.800 0.130 150)"
typography:
  font-family: "-apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif"
  font-family-mono: "ui-monospace, SFMono-Regular, Menlo, monospace"
  text-2xs: { size: "0.75rem" }
  text-xs:  { size: "0.8125rem" }
  text-sm:  { size: "0.875rem" }
  text-base: { size: "1rem" }
  text-md:  { size: "1.125rem" }   # declared, unused anywhere in the stylesheet
  text-lg:  { size: "1.5rem" }
  text-xl:  { size: "2rem" }
  weight-regular: 400
  weight-medium: 500
  weight-semibold: 600
rounded:
  sm: "0.625rem"
  md: "0.75rem"
  lg: "1rem"
  xl: "1.25rem"
spacing:
  1: "0.25rem"
  2: "0.5rem"
  3: "0.75rem"
  4: "1rem"
  5: "1.25rem"
  6: "1.5rem"
  7: "2rem"
  8: "2.5rem"
components:
  button-primary:
    background: "{colors.accent}"
    color: "{colors.on-accent}"
    radius: "{rounded.sm}"
  button-cancel:
    color: "{colors.danger}"
    border: "1px solid {colors.danger}"
    background: "transparent"
  button-secondary:
    background: "{colors.surface-2}"
    color: "{colors.text-primary}"
    border: "1px solid {colors.border}"
  input:
    background: "{colors.surface-1}"
    border: "1px solid {colors.border}"
    color: "{colors.text-primary}"
    height: "2.5rem"
  status-badge:
    radius: "{rounded.xl}"
---

## Overview

Ravive's GUI is one Python triple-quoted string (`HTML_CONTENT`, gui.py ~356-1919)
rendered inside a pywebview window (900×750 default, min 800×650, resizable). No
build step, no CSS/JS files, no framework, no external network requests — every
style and script is inline in that literal.

Dark-only: `:root { color-scheme: dark; }` is declared and there is no light
palette. All tokens below are CSS custom properties on `:root` (gui.py:477-550).

Register: native-macOS-utility, not web-app-in-a-window. See PRODUCT.md for the
personality brief this system implements (warm, restrained, quiet under a
20-60 minute unattended job).

## Colors

Neutral scale (page → nested surfaces, tinted 0.004-0.008 chroma at hue 250,
a cool near-neutral grey):

| Token | OKLCH | Role | Contrast (as text, on the surface it sits on) |
|---|---|---|---|
| `--bg` | `oklch(0.155 0.006 250)` | Page canvas, `.container` background | — |
| `--surface-1` | `oklch(0.205 0.006 250)` | Inputs/selects, disabled-input bg, form scrollbar track | — |
| `--surface-2` | `oklch(0.235 0.008 250)` | Progress card, dialog body, idle/cancelled badge bg, `.btn-secondary` bg | — |
| `--surface-3` | `oklch(0.125 0.004 250)` | Log terminal bg (deepest layer). Aliased as `--terminal-bg` | — |
| `--border` | `oklch(0.520 0.008 250)` | Component boundary: input/select, `.btn-browse`, `.btn-secondary`, file-list | 3.55:1 on `--bg`, 3.25:1 on `--surface-1` (≥3:1, meets 1.4.11 non-text contrast) |
| `--border-subtle` | `oklch(0.260 0.006 250)` | Decorative-only divider: progress-card border, form-hint, dialog, log-terminal, file-item row separators | 1.07:1 on `--surface-2` — never relied on for a required contrast |

Text (all four roles paired against every surface they're actually painted on):

| Token | OKLCH | Role | Contrast |
|---|---|---|---|
| `--text-primary` | `oklch(0.930 0.006 250)` | Headings, labels, field values, badge/log-empty primary text | 15.91:1 on `--bg`, 14.58:1 on `--surface-1`, 13.57:1 on `--surface-2` |
| `--text-secondary` | `oklch(0.780 0.008 250)` | Declared, **never referenced** anywhere else in the stylesheet | 9.77:1 on `--bg` (dead token, computed for completeness) |
| `--text-muted` | `oklch(0.685 0.010 250)` | Subtitle, field hints, placeholders, worker rows, timestamps, log-empty copy | 6.92:1 on `--bg`, 6.34:1 on `--surface-1`, 5.90:1 on `--surface-2`, 7.16:1 on `--surface-3` |
| `--text-disabled` | `oklch(0.400 0.006 250)` | Disabled input/select text only | 2.12:1 on `--bg`, 1.95:1 on `--surface-1` — below AA; WCAG exempts disabled-control text from the contrast requirement, and the code comment says so explicitly |

Accent — one solid warm amber/gold, reserved for primary action, focus ring,
progress fill, and links (never decorative):

| Token | OKLCH | Role | Contrast |
|---|---|---|---|
| `--accent` | `oklch(0.780 0.150 72)` | `.btn-primary` bg, progress/worker fill, focus ring, `.breadcrumb-segment` text | 9.53:1 on `--bg`, 8.73:1 on `--surface-1`, 8.12:1 on `--surface-2` (as text/icon) |
| `--accent-hover` | `oklch(0.830 0.140 72)` | `.btn-primary:hover` bg | — |
| `--accent-active` | `oklch(0.720 0.160 72)` | `.btn-primary:active` bg | — |
| `--on-accent` | `oklch(0.160 0.010 72)` | Text on accent fills | 9.47:1 on `--accent`, 11.26:1 on `--accent-hover`, 7.62:1 on `--accent-active` |

Destructive — Cancel button only, never used for the Cancelled *status* (that's
neutral, see below):

| Token | OKLCH | Role | Contrast |
|---|---|---|---|
| `--danger` | `oklch(0.720 0.160 25)` | `.btn-cancel` text + border | 7.35:1 on `--bg`, 6.27:1 on `--surface-2` |
| `--danger-hover` | `oklch(0.770 0.150 25)` | `.btn-cancel:hover` background tint (via `color-mix`) | 8.62:1 on `--bg` |

Status vocabulary — six surface+text pairs, each verified as a pair, never
color alone (badge text always carries the state via `STATUS_LABELS`):

| State | Surface | Text | Contrast |
|---|---|---|---|
| idle | `oklch(0.235 0.006 250)` | `oklch(0.700 0.008 250)` | 6.24:1 |
| running | `oklch(0.270 0.055 72)` | `oklch(0.820 0.150 72)` | 8.49:1 |
| completed | `oklch(0.270 0.050 155)` | `oklch(0.800 0.150 155)` | 8.40:1 |
| failed | `oklch(0.270 0.065 25)` | `oklch(0.780 0.170 25)` | 6.61:1 |
| cancelling | reuses idle-surface | reuses idle-text | 6.24:1 |
| cancelled | `oklch(0.235 0.008 250)` == `--surface-2`, **deliberately** | `oklch(0.780 0.012 250)` | 8.33:1 |

`cancelled` is pinned to the same neutral as `--surface-2`/idle by comment,
not by accident — it is the token-level encoding of PRODUCT.md's "cancelled
is not failed." `cancelling` borrows idle's tokens outright (only the label
text changes, "Cancelling…").

Terminal — same neutral system, one genre-conventional exception:

| Token | OKLCH | Role | Contrast |
|---|---|---|---|
| `--terminal-bg` | = `--surface-3` | `.log-terminal` background | — |
| `--terminal-text` | `oklch(0.800 0.130 150)` | Log text (green) | 11.36:1 on `--terminal-bg` |

## Typography

Family stack, exactly as written (gui.py:580, body selector):

```
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', system-ui, sans-serif;
```

No web font, no `@font-face`, no network request for type — one requirement
of running fully offline. Monospace stack, log terminal only (gui.py:1047):

```
font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
```

Scale (`--text-*`, gui.py:524-530). Comment at gui.py:521 states "400/500/600
only" as the weight ceiling:

| Token | rem | px (16px root) | Used by |
|---|---|---|---|
| `--text-2xs` | 0.75rem | 12px | field hints, form-hint |
| `--text-xs` | 0.8125rem | 13px | worker rows, log terminal, status badge, status message, result panel, `.btn-secondary`, time estimate |
| `--text-sm` | 0.875rem | 14px | subtitle, field labels, inputs/selects, legend, breadcrumbs, file names |
| `--text-base` | 1rem | 16px | button base size (`button { font-size }`) |
| `--text-md` | 1.125rem | 18px | **declared, never referenced anywhere else in the file** |
| `--text-lg` | 1.5rem | 24px | h1 wordmark, dialog close-button glyph |
| `--text-xl` | 2rem | 32px | `#progressText` — the one hero numeral, "scanned from across the room" per the code's own comment |

Weights actually applied: 600 (h1, labels, legend, buttons, badges,
`progressText`), 500 (`form-hint strong`, `#progressSegment`), 400 (subtitle,
checkbox labels — the generic label rule is 600 but each checkbox `<label>`
carries an inline `font-weight: normal` override).

`font-variant-numeric: tabular-nums` on `#progressText`, worker `.worker-pct`,
and the elapsed/ETA readout — numerals don't reflow the layout as digits
change during a live job.

## Layout

Window chrome: `body` is `100vw`×`100vh`, flex, `overflow: hidden`.
`.container` fills it edge to edge with `border-radius: 0` — no rounded outer
frame, no border, no shadow; it *is* the window, not a card floating in one.
Padding `var(--space-6)` (24px) on all sides.

Two-column grid, `.main-layout { grid-template-columns: 1fr 1.2fr; gap:
var(--space-6); }` — form-side left, status-side right. The code comment at
gui.py:626-628 puts the idle columns at roughly 330-400px each.

**Observed at the shipped default window size**: a `@media (max-width:
62.5rem)` rule (1000px at the default 16px root) collapses the grid to a
single stacked column whenever the *viewport* is narrower than 1000px
logical px. The default launch window is 900×750 — narrower than the
breakpoint — so the idle two-column split does not actually appear until the
user manually widens the window past ~1000px; at first launch the form and
status panels are always stacked, one above the other.

Running state overrides the grid independently of width:
`.main-layout.processing { grid-template-columns: 1fr; }` plus
`.form-side { display: none; }` — the status panel takes the full row while
a job runs, regardless of window size.

Below the 1000px breakpoint, `.container`/`body` switch `overflow` to `auto`
(scroll) and the grid rows switch to `auto auto` with `height: auto` — a
long code comment (gui.py:634-639) explains this is to stop content from
being clipped under a viewport-height clamp once the grid is single-column.

Shared control height: `--control-height: 2.5rem` (40px) — every text input,
select, and `.btn-browse` icon button.

## Elevation & Depth

No drop shadows for surface separation. Depth is expressed as **tonal
layering**: each nested surface in the neutral scale (`--bg` →
`--surface-1` → `--surface-2` → `--surface-3`) is a fixed step darker/lighter
than its parent, and that's the entire depth system for cards, panels, and
the terminal.

The only two `box-shadow` declarations that aren't a focus ring:

- `dialog#explorerModal { box-shadow: 0 10px 30px oklch(0 0 0 / 0.5); }` —
  the file-explorer modal, which uses the native top layer and only exists
  transiently (browser-fallback path, never opens in the shipped `.app`).
- The 50px wordmark logo `<img>` carries an inline
  `box-shadow: 0 5px 15px oklch(0 0 0 / 0.35)` — a literal value, not a
  token, and the one hardcoded style in the header markup.

No glow shadows, no `translateY` lift, no hover elevation on any button —
all interactive-state feedback on buttons/inputs is background-color and
border-color only.

## Shapes

`--radius-sm` (0.625rem/10px): inputs, selects, `.btn-browse`, all buttons.
`--radius-md` (0.75rem/12px): `.form-hint`, `.log-terminal`, breadcrumbs bar,
file-list container. `--radius-lg` (1rem/16px): `.progress-card` — the one
component at this radius. `--radius-xl` (1.25rem/20px): status badge (pill),
`.jump-to-latest` (pill), the file-explorer `<dialog>`.

The logo's `border-radius: 12px` is hardcoded inline, not `var(--radius-md)`
— same visual value, but not wired to the token.

## Motion

Three durations, two easings, all on `background-color`/`border-color`/
`box-shadow`/`width` — never `transform`, never `all`:

| Duration | Easing | Applies to |
|---|---|---|
| 180ms | `ease-out` | inputs/selects (border+shadow), `.btn-browse`, `.btn-primary`, `.btn-cancel`, `.btn-secondary`, `.jump-to-latest`, file-item rows |
| 200ms | `ease-out` | `.status-badge` background-color/color — the one outlier duration |
| 450ms | `linear` | `.progress-bar-fill` and `.worker-bar-fill` width. Chosen (per code comment, gui.py:980-982) to land *just under* the 500ms poll interval so a fill finishes before the next poll updates it, instead of visibly stepping |

`.close-btn` declares no transition at all — its hover/active color change is
an instant swap, the one interactive element without an eased state change.

No `@keyframes`, no `animation` outside the reduced-motion override, no
pulsing/glowing/drifting anything — consistent with PRODUCT.md's "quiet
under load." Log auto-scroll and "jump to latest" are hard `scrollTop`
jumps, not smooth-scrolled.

Reduced motion (gui.py:1310-1322):

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
  }
  dialog#explorerModal,
  dialog#explorerModal::backdrop { animation: none !important; }
}
```

The dialog gets an explicit second rule because `<dialog>`'s native
open/close animation isn't reliably caught by the generic
`transition-duration` override.

## Components

**Button — primary** (`.btn-primary`, `#submitBtn`)
Default: bg `--accent`, text `--on-accent`, `--radius-sm`, `flex: 1`.
Hover: bg `--accent-hover`. Active: bg `--accent-active`.
Disabled: generic `button:disabled { opacity: 0.5; cursor: not-allowed; }`.
Focus-visible: global 3px `--accent` outline, offset 2px.
State-machine (JS): disabled immediately on submit (`startUpscale`);
`display: none` while a job runs (`submitBtn.style.display`); restored
`display: block` + re-enabled once status settles to
completed/failed/cancelled (`pollStatus`).

**Button — secondary** (`.btn-secondary`, e.g. `revealBtn`)
Default: bg `--surface-2`, text `--text-primary`, border `--border`,
`--radius-sm`, `--text-xs`/600. Hover: bg tinted with
`color-mix(in oklch, var(--accent) 12%, var(--surface-2))`. No component-
specific active or disabled rule — falls through to the generic
`button:disabled` opacity rule.

A third, destructive variant exists alongside these two: `.btn-cancel`
(`#cancelBtn`) — transparent bg, `--danger` text + 1px `--danger` border,
`flex: none` (fixed width, right-pinned via `margin-left: auto`, unlike
`.btn-primary`'s `flex: 1`, "so a full-width danger-red button doesn't
outweigh the progress readout," per the code comment). Hover/active tint
`--danger` at 15%/30% via `color-mix`. Hidden by default
(`display: none` inline), shown for the run's duration, self-disables on
click (`cancelUpscale`) so it can't double-fire.

**Text input** (`input[type="text"]`, `input[type="number"]`)
Default: height `--control-height` (2.5rem), bg `--surface-1`, border
`--border`, `--radius-sm`, text `--text-primary`, `--text-sm`.
Placeholder: explicit `color: var(--text-muted); opacity: 1;` (overrides the
UA default dimming — this is the fix for placeholders that would otherwise
render at browser-default grey).
Focus-visible: **local override** — `border-color: var(--accent)`,
`box-shadow: 0 0 0 3px color-mix(in oklch, var(--accent) 25%, transparent)`,
`outline: none`. This replaces the page's generic 3px outline ring with a
colored border + glow ring for text inputs and selects specifically; both
are visible focus indicators, just styled differently per control type.
Disabled: bg unchanged (`--surface-1`), text `--text-disabled`, `opacity: 1`,
`cursor: not-allowed`.
Transition: `border-color 180ms ease-out, box-shadow 180ms ease-out`.

**Select** (`<select>`)
Shares the exact selector list and rule block with text inputs — same
states, same focus treatment. `.grid` uses
`grid-template-columns: repeat(auto-fit, minmax(17rem, 1fr))`; the code
comment (gui.py:796-798) states 17rem is deliberately sized to the longest
option label's rendered width (231px) plus padding/border, so the field
stacks full-width rather than clipping the label. `color-scheme: dark` at
`:root` makes the native popup and its scrollbar render dark.
Model `<select>` pairs with `#modelHint`, a `--text-2xs`/`--text-muted` line
updated on `change` from each `<option>`'s `data-hint` attribute.

**Checkbox** (`input[type="checkbox"]`)
24×24 CSS px (WCAG 2.2 §2.5.8 minimum target size), `accent-color: var(--accent)`.
Hover: `accent-color: var(--accent-hover)`. Disabled: `opacity: 0.5`.
`color-scheme: dark` gives the native dark checkbox chrome. Each checkbox's
paired `<label>` carries an inline `font-weight: normal` override — checkbox
labels are visually distinct (400) from field labels (600 by default). All
three checkboxes live inside one `<fieldset><legend>Options</legend>`, the
legend styled identically to a field label.

**Progress bar** (`.progress-bar-container`/`.progress-bar-fill`,
`#progressBarTrack`)
Track: 12px tall, bg `--surface-1`, `border-radius: 6px`,
`role="progressbar"` with `aria-valuemin/valuemax="0"/"100"`, live
`aria-valuenow`/`aria-valuetext`, `aria-labelledby` pointing at the
sr-only `#progressHeading`. Fill: bg `--accent`, width set by JS on every
500ms poll, `transition: width 450ms linear`. States: idle "Ready to
start"/0%; running (live); completed 100%; failed/cancelled freeze at
whatever value the bar last reached — nothing resets it except the next
`startUpscale()` call.

**Worker row** (`.worker-row`, dynamically created/keyed per active segment
in `renderWorkers()`)
One row per in-flight chunk, keyed by a sanitized segment id so an existing
row's bar animates in place across polls instead of being torn down and
rebuilt. `.worker-label` fixed 150px with ellipsis truncation.
`.worker-bar-container` (`role="progressbar"`, 6px track, bg `--surface-1`)
+ `.worker-bar-fill` (bg `--accent`, same `450ms linear` as the main bar).
`.worker-pct` fixed 48px, right-aligned, tabular-nums. Rows not present in
the latest poll's worker list are removed outright (`seen`-set diff) — no
exit transition.

**Status badge** (`.status-badge.status-{idle|running|cancelling|completed|
failed|cancelled}`)
Pill: `padding: 6px 12px`, `--radius-xl`, `--text-xs`/600. Transition:
`background-color 200ms ease-out, color 200ms ease-out` (the one component
on a 200ms rather than 180ms duration). Six state classes map 1:1 to the six
surface/text token pairs in Colors above; label text always comes from the
`STATUS_LABELS` JS map alongside the class swap — state is never color-only.

**Log panel** (`#logTerminal` inside `.log-terminal-wrap`)
`.log-terminal-wrap` is `position: relative; flex: 1; min-height: 0;
display: flex;` inside `.progress-card` (itself `flex-direction: column`) —
this is what lets `.log-terminal { flex: 1; }` actually receive the
remaining vertical space; nothing in the current JS ever sets an inline
`display` on `#progressCard` that would defeat that flex chain.
`.log-terminal`: bg `--terminal-bg` (`--surface-3`), monospace stack,
`--text-xs`, text `--terminal-text`, `overflow-y: auto`,
`white-space: pre-wrap`, `role="log"`, `aria-live="off"`, `tabindex="0"`
(keyboard-scrollable). Empty state (`#logEmpty`, centered icon + copy) is
present in the initial markup and is destroyed the moment either
`startUpscale()` or the first `pollStatus()` tick sets
`logTerminal.innerText`, which replaces the element's entire content.
Auto-scroll: `pollStatus()` checks `isLogAtBottom()` *before* rewriting
`innerText`; if the user was at the bottom it re-pins to the bottom
(`scrollLogToBottom()`), otherwise it reveals `#jumpToLatestBtn` (a pill,
`.jump-to-latest`, `position: absolute; bottom/right: 12px;`, `hidden`
attribute toggled) instead of forcing the view down. Announcements to
assistive tech do **not** go through this `aria-live="off"` panel — a
separate `#liveAnnouncer` (`.sr-only`, `aria-live="polite"`) is updated only
on a segment-text change or a crossed ~10% milestone, not on every poll.

**Dialog — file explorer** (`dialog#explorerModal`)
Native `<dialog>` + `showModal()`: top layer, native Escape-to-close, native
focus trap, native inertness of the rest of the page, all for free per the
code's own comment. Browser-fallback path only — `openExplorer()` calls
`window.pywebview.api.select_file()/select_folder()` when that bridge
exists, and this dialog never opens in the shipped `.app`.
Backdrop: `::backdrop { background-color: color-mix(in oklch, var(--bg) 85%,
transparent); }` — solid scrim, explicitly no `backdrop-filter` (comment:
"the ban applies without exceptions").
Close vectors, all routed through `closeExplorer()` via the dialog's native
`close` event: the `.close-btn` (X icon, `aria-label="Close file browser"`),
native Escape, a backdrop click (`e.target === dialog`), the footer "Close"
button, and "Select Current Folder." `closeExplorer()` also returns focus to
`explorerOpenerEl`, the element that had focus before the dialog opened.
Content: breadcrumbs (`.breadcrumb-segment`, `role="button"`,
`tabindex="0"`, click + Enter/Space handlers, one span per path component,
Finder-path-bar style) and a file list of real `<button class="file-item">`
rows built with `textContent` for the filename (never `innerHTML`) paired
with one of two static SVG icon constants — filesystem text is never
concatenated into markup. Rows get the global focus-visible ring; no
component-local override.

## Accessibility

Target stated in PRODUCT.md: WCAG 2.2 AA + full keyboard operation +
VoiceOver. What the current markup does toward that, as written:

- `color-scheme: dark` at `:root` — native form controls, scrollbars, and
  the `<select>` popup render dark instead of falling back to light UA
  chrome.
- Every interactive element gets a 3px `--accent` focus-visible outline by
  default (`:is(a, button, input, select, [tabindex]):focus-visible`);
  text inputs/selects substitute a border+glow ring instead (see
  Components) — both are visible indicators, styled per control type.
- `role="progressbar"` + live `aria-valuenow`/`aria-valuetext` on both the
  overall bar and every worker bar; `role="log"` on the terminal; a
  dedicated `aria-live="polite"` `#liveAnnouncer` throttled to
  segment-change/10%-milestone events carries the running commentary a
  40-minute job needs for a non-visual user.
- Checkbox targets are 24×24 CSS px (§2.5.8 minimum).
- `setFormDisabled()` disables every form control and toggles `inert` on
  `.form-side` while a job runs — belt-and-suspenders alongside the
  `display: none` from `.main-layout.processing`, so the idle form is
  provably out of the tab order and accessibility tree, not just visually
  hidden.
- The file-explorer `<dialog>` gets focus trap, Escape, and focus-restore
  from the native element (see Components) rather than hand-rolled JS.
- Status is always encoded as badge *text* (`STATUS_LABELS`) alongside the
  color class — never color alone.
- `@media (prefers-reduced-motion: reduce)` collapses every transition and
  animation to near-zero duration (see Motion).
- `--text-disabled` (2.12:1 on `--bg`) is the one color pair below AA body-
  text contrast; it is scoped to disabled input/select text only, which
  WCAG exempts.

## Do's and Don'ts

Carried forward from PRODUCT.md's anti-references — a future agent touching
this file should treat these as hard boundaries, not starting points to
soften:

- **No gradient text.** `background-clip: text` does not appear anywhere in
  the stylesheet. Do not reintroduce it on the `h1` wordmark or anywhere
  else — this is an absolute ban, not a style preference.
- **No indigo→cyan (or any) gradient as the identity color.** One solid
  accent (`--accent`, warm amber/gold) does every job gradients used to do:
  primary action, focus ring, progress fill, links.
- **No `backdrop-filter` glass on `.container` or any always-on surface.**
  The one remaining `backdrop-filter`-adjacent decision (the file-explorer
  dialog backdrop) was deliberately downgraded to a flat `color-mix` scrim;
  don't restore blur there or anywhere else that renders for the life of a
  20-60 minute job.
- **No radial background blobs, no decorative gradients anywhere.**
  `grep -n gradient gui.py` returns nothing — keep it that way.
- **No emoji icons.** Every glyph in the file is an inline static SVG
  (folder, file, close-X, chevron, document). No emoji appear anywhere in
  `HTML_CONTENT`.
- **No web fonts, no Google Fonts, no network font request.** The family
  stack is system-only (`-apple-system, BlinkMacSystemFont, 'SF Pro Text',
  system-ui, sans-serif`) — this is an offline desktop app; any `@font-face`
  or remote `<link>` breaks that contract outright.
- **No glow shadows or `translateY` lift on buttons.** Interactive feedback
  is background-color/border-color only; `grep -n translateY gui.py`
  returns nothing.
- **No `transition: all`.** Every transition names its specific
  properties; `grep -n "transition: all" gui.py` returns nothing.
- **Cancelled is not failed, at the token level.** `--cancelled-surface` is
  pinned to `--surface-2` by comment, not accident. Don't give "cancelled"
  its own alarming color — it reuses the neutral idle palette on purpose.
- **Quiet under load.** No `@keyframes`, no pulsing/glowing/drifting motion
  outside the reduced-motion override. Motion exists only to explain a
  state change (button hover, focus, a value updating) — never as ambient
  decoration on a screen that stays open for an hour.
