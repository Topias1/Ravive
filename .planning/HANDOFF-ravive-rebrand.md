# HANDOFF — Rebrand "Ravive" : STATUT = TERMINÉ

**Date**: 2026-07-03 · **Repo**: `Topias1/Ravive` (ex-VideoUpscalAI) · **Branche**: main

## Décision de naming (NE PAS relitiger)

Le nom **Ravive** (de "raviver" — redonner vie) a été choisi après 3 sessions et ~50 candidats
éliminés, validé par un sweep multi-agents (GitHub + web + panel branding).
- Tagline retenue : **"Ravive — AI-powered video & image upscaler"** (média-agnostique : l'upscale
  d'images arrivera plus tard, ne jamais écrire "video-only" dans le branding).
- L'IA vit dans la tagline, PAS dans le nom (pas de "RaviveAI").
- Rejetés (ne pas re-proposer) : Revif, Rialza, Nitore, Detayl, Detale, Loupe, Magnifiq, Restory,
  Vivyd, Skayl, MacVideoUpscaler, VidScale…

## Tout est fait ✅

1. Repo GitHub renommé `Topias1/VideoUpscalAI` → `Topias1/Ravive` (redirect auto).
2. Description GitHub à jour : "AI video upscaler for macOS & Linux — Real-ESRGAN,
   GPU-accelerated, resumable pipeline, native Apple Silicon".
3. 12 topics GitHub posés.
4. Remote local à jour (`git@github.com:Topias1/Ravive.git`).
5. `Ravive.spec` (bundle id `com.electrateam.ravive`), `gui.py`, `README.md` rebrandés
   (commit `e97cf48`).
6. **README refondu** (commit `0b74b11`) : badges (release/license/platform), tagline SEO en
   ouverture, section Roadmap (mentionne l'upscale d'images à venir), tableau comparatif vs
   video2x / QualityScaler — claims vérifiées via recherche web avant publication (corrections :
   QualityScaler a bien un stop&resume, video2x macOS = Docker only, pas de preuve de signature
   pour l'exe QualityScaler).
7. **Screenshot re-capturé** (commit `07c1ad8`) : l'ancien montrait encore "VideoUpscalAI" (bug —
   un vieux process zombie squattait le port 8080 et servait l'ancienne version en mémoire même
   après édition du fichier ; toujours vérifier `lsof -iTCP:8080` avant de re-capturer un
   screenshot du GUI local). Capture faite via `Google Chrome --headless --screenshot=...`
   (screencapture/osascript indisponibles dans cet environnement sandboxé — pas de permission
   Screen Recording/Accessibility).
8. **Rebuild + signature** : `pyinstaller Ravive.spec` → `dist/Ravive.app`, signé
   "Developer ID Application: Antoine Weytens (K9KAJBBY5C)", bundle id `com.electrateam.ravive`.
   Testé : lance sans crash, serveur GUI local répond (HTTP 200 sur :8080).
9. **Notarisation** : DMG (`dist/Ravive.dmg` via `hdiutil create`) soumis et **Accepted** via
   `xcrun notarytool submit --keychain-profile "notary-profile" --wait`, puis
   `xcrun stapler staple`. Vérifié : `spctl -a -vv` sur l'app extraite du DMG monté →
   `accepted, source=Notarized Developer ID`.
   ⚠️ **Le nom du profil keychain est `notary-profile`** (pas "Ravive", pas le nom du compte Apple).
   Il n'était pas dans le trousseau local sous un nom "logique" — retrouvé en grepant les logs
   d'une session **Antigravity** antérieure (voir mémoire `reference-antigravity-sessions` /
   `project-ravive-notarization-blocker` dans le système de mémoire Claude Code : commande exacte
   trouvée dans `~/.gemini/antigravity-cli/brain/f414a777-8e13-4ef1-80bc-9aaca10b2690/`).
10. **Release v1.0 re-cut** : `gh release upload v1.0 dist/Ravive.dmg --clobber` (nouveau DMG
    signé+notarisé, 206 MB), notes de release mises à jour ("Ravive (formerly VideoUpscalAI)").
11. **Vérifications finales** : lien de téléchargement DMG → 200, screenshot brut GitHub → 200,
    page repo → 200.

## Reste en trainant (non bloquant, cosmétique)

- `GEMINI.md` référence encore l'ancien nom (`AppleSiliconVideoUpscaler.spec`,
  `AppleSiliconVideoUpscaler.app`) — doc dev, jamais mise à jour, à corriger un jour si quelqu'un
  s'en sert vraiment.
- `.planning/PROJECT.md`, `REQUIREMENTS.md`, `ROADMAP.md` ont encore "VideoUpscalAI" en titre —
  artefacts de planning historiques, pas la priorité.
- Le logo (`logo.jpg`/`logo.icns`) n'a pas été refait — il est déjà générique ("UPSCALER HD AI",
  pas de texte "VideoUpscalAI" dedans), donc pas de conflit de branding, mais pas franchement
  "Ravive" non plus si on veut pousser l'identité visuelle plus loin.
- Indexation Google/GitHub du nouveau nom : rien à faire, ça se fait tout seul sous quelques jours.

## Pièges à retenir pour la prochaine session

- **Toujours vérifier `lsof -iTCP:8080`** avant de tester/screenshotter le GUI local : un vieux
  process d'une session précédente peut squatter le port et servir du code obsolète même si le
  fichier source a été édité entre-temps (piégeant, ça ressemble à un bug de cache alors que c'est
  juste un process fantôme).
- **Le trousseau macOS peut contenir des credentials créés par un autre outil** (ici Antigravity,
  pas Claude Code) sous un nom non-évident. Avant de demander à l'utilisateur de recréer des
  credentials, chercher dans `~/.gemini/antigravity-cli/brain/*/` (ou l'équivalent d'autres agents
  installés sur la machine) — souvent plus rapide que de refaire la procédure Apple.
- `screencapture`/`osascript` ne fonctionnent pas dans cet environnement (sandbox, pas de
  permission Screen Recording/Accessibility) → utiliser Chrome headless (`--headless
  --screenshot=... --window-size=W,H URL`) pour capturer une UI web locale.

## Contexte utilisateur

- Répondre en français, style télégraphique (cf. CLAUDE.md global).
- Fichiers untracked à ignorer : `ffmpeg`, `ffprobe`, `test_work/`, `.planning/`.
- L'app : pipeline Real-ESRGAN-ncnn-vulkan + ffmpeg, GUI = serveur web local dans `gui.py`.
