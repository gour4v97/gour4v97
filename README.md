# Hi, I'm Gourav

Data Science undergraduate at IIT Madras interested in applied ML, AI systems, and privacy-focused software engineering.

![Visitors](https://komarev.com/ghpvc/?username=gour4v97&label=visitors&color=0f766e&style=flat-square)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-activity-dark.svg" />
  <img width="100%" src="./assets/profile-activity-light.svg" alt="Build activity over the last 12 months: total commits, active days, monthly commits, and commits by weekday" />
</picture>
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/profile-stack-dark.svg" />
  <img width="100%" src="./assets/profile-stack-light.svg" alt="Projects and stack: language mix across public projects, with each project's commit count and last push date" />
</picture>

## Projects

### [Remi](https://github.com/gour4v97/remi) — Remi Suite

Two Windows voice apps in pure Python, sharing one local voice engine, now built as a modular assistant platform. Everything runs locally — your voice never leaves the machine.

- **Voice Trans** — push-to-talk dictation (`Ctrl+Alt+Space`): speak in English, Hindi, or Hinglish, and the transcript is typed into whatever app has focus, with Devanagari → Roman transliteration and a pronunciation dictionary.
- **Remi Browser** — a voice-controlled browser (`Ctrl+Alt+B`): 40+ commands in English/Hindi/Hinglish drive Chrome/Edge over the Chrome DevTools Protocol — open, search, scroll, tabs, click, play/pause — with spoken confirmations.
- A persistent whisper.cpp server keeps the model warm and shared between both apps; on an NVIDIA GPU transcription takes ~0.3 s (CUDA build), with a transparent CPU fallback.
- Local LLM support: conversational commands are resolved on-device through Ollama, LM Studio, or llama.cpp backends, with a modular skills system for custom commands.
- A local REST API (`remi serve`), a Click CLI (`remi setup`, `remi doctor`, `remi llm`, `remi skill`), and a one-click Windows installer with a setup wizard.

### Voice Trans

Push-to-talk dictation for Windows, in Python. Press the hotkey (`Ctrl+Alt+Space`), speak in Hindi, English, or Hinglish, press it again, and the transcript is typed into whatever app has focus.

- Local Whisper transcription via whisper.cpp — nothing leaves the machine.
- Devanagari → Roman transliteration for Hinglish output, a pronunciation dictionary, and local-only history.
- Voice Trans is now part of the [Remi Suite](https://github.com/gour4v97/remi) above, where it is maintained and developed; its original standalone repository is private.

### [3D Cardiovascular Risk Explorer](https://github.com/gour4v97/3d-cardiovascular-risk-explorer)

An educational ML prototype that estimates cardiovascular-risk likelihood from clinical features, with interactive 3D visualisation, a FastAPI backend, SHAP explanations, and documented model limitations.

- End-to-end Python ML application, built and deployed.
- Nested cross-validation, calibration, leakage checks, and model-quality reporting — including the targets that fall below their validation bars, kept visible on purpose.
- Input validation on `/predict` and `/explain`: null, out-of-range, and unknown-category values return 422 instead of a confident wrong prediction; model artifacts are cached per request.
- An educational prototype, not a clinical diagnostic tool.
- [Repository](https://github.com/gour4v97/3d-cardiovascular-risk-explorer) · [Live demo](https://3d-cardiovascular-risk-explorer-pgd4.vercel.app)

### [GlassTab](https://github.com/gour4v97/glasstab)

A Comet-style glassmorphism New Tab page for Brave and Chrome, built as a Manifest V3 extension in vanilla JavaScript — no build step, no frameworks, no tracking.

- AI-first search pill that hands off to Gemini, Perplexity, ChatGPT, Claude, or Duck.ai.
- Frosted-glass cards with adjustable blur, opacity, and radius; animated mesh-gradient backgrounds, quick links, weather (Open-Meteo, no API key), and recent bookmarks.
- Video wallpaper and motion preferences; recent performance work batches settings updates and cuts background paint cost.
- Settings sync via `chrome.storage.sync`; reduce-transparency and reduced-motion support built in.

### [Windows Bar](https://github.com/gour4v97/windowbar) — Windows Bar

A smart dock for Windows 10/11, written in Python (PySide6): 28 live widgets — next calendar event, now playing, weather, CPU/RAM/battery, GitHub, Stripe balance, screen time, open windows, focus timer — in a glass dock that reserves screen space and can stand in for the taskbar. No account, no telemetry; everything runs locally.

- Next event from a secret iCal link (Google, Outlook, iCloud), with an automation that pauses music a minute before a meeting.
- Acrylic glass, top or bottom (drag it to an edge), full-width or pill, taskbar auto-hide restored safely on quit or crash.
- Alt+Space keyboard launcher with fuzzy search, plus a theme engine with built-in and custom JSON themes, a theme gallery, and a wallpaper-derived dynamic accent.
- Ships with a one-click installer (`setup.bat`) and auto-hide for fullscreen apps; releases on GitHub.
- Also: quick toggles (Wi-Fi, Bluetooth, airplane), volume control, world clocks, storage/network/progress widgets, a script widget, pinned apps with running dots and Alt+1–9 switching, and per-widget popups (calendar month view, full todos, multiple notes).
- Now growing into a desktop shell: split toolbar and dock layouts, a bar on each display, workspaces with virtual desktops, a custom Alt+Tab switcher, draggable desktop widgets, and an opt-in tiling window manager (BSP, Columns, Master/stack).

## What I work with

Python · pandas · NumPy · scikit-learn · FastAPI · PySide6 · JavaScript · HTML/CSS · Three.js · Whisper (whisper.cpp) · Ollama · Chrome DevTools Protocol · Git/GitHub

## Currently exploring

Statistical inference, SQL, model evaluation, and production-oriented machine-learning workflows.

## Contact

- Email: gouravmanjhi97@gmail.com
- LinkedIn: [linkedin.com/in/gourav-manjhi-94335b312](https://www.linkedin.com/in/gourav-manjhi-94335b312/)
- GitHub: [github.com/gour4v97](https://github.com/gour4v97)
