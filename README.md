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

### [Remi](https://github.com/gour4v97/remi)

A voice-controlled browser for Windows, in C#/.NET. Speak a command in English, Hindi, or Hinglish — "open youtube", "youtube kholo", "search ..." — and Remi drives the browser over the Chrome DevTools Protocol: opening sites, searching, scrolling, switching tabs, clicking, and playing or pausing media, with spoken confirmations.

- Speech is transcribed locally with Whisper — nothing leaves the machine by default.
- This repo is the Remi Suite: it contains both apps in one solution — Remi Browser and VoiceTrans (below) — sharing the same local voice engine, and both can run side by side.

### [Voice Trans](https://github.com/gour4v97/voice-trans)

Push-to-talk dictation for Windows, in C#/.NET. Press the hotkey, speak in Hindi, English, or Hinglish, press it again, and the transcript is typed into whatever app has focus.

- Local Whisper transcription (optional Groq cloud if you enable it yourself).
- Devanagari → Roman transliteration for Hinglish output, a pronunciation dictionary, and local-only history.
- This is the standalone repository for the dictation app; the same app also ships inside the [Remi](https://github.com/gour4v97/remi) suite repo, next to the voice browser.

### [3D Cardiovascular Risk Explorer](https://github.com/gour4v97/3d-cardiovascular-risk-explorer)

An educational ML prototype that estimates cardiovascular-risk likelihood from clinical features, with interactive 3D visualisation, a FastAPI backend, SHAP explanations, and documented model limitations.

- End-to-end Python ML application, built and deployed.
- Nested cross-validation, calibration, leakage checks, and model-quality reporting — including the targets that fall below their validation bars, kept visible on purpose.
- An educational prototype, not a clinical diagnostic tool.
- [Repository](https://github.com/gour4v97/3d-cardiovascular-risk-explorer) · [Live demo](https://3d-cardiovascular-risk-explorer-pgd4.vercel.app)

## What I work with

Python · pandas · NumPy · scikit-learn · FastAPI · C# · .NET · Whisper · Git/GitHub · HTML/CSS · Three.js

## Currently exploring

Statistical inference, SQL, model evaluation, and production-oriented machine-learning workflows.

## Contact

- Email: gouravmanjhi97@gmail.com
- LinkedIn: [linkedin.com/in/gourav-manjhi-94335b312](https://www.linkedin.com/in/gourav-manjhi-94335b312/)
- GitHub: [github.com/gour4v97](https://github.com/gour4v97)
