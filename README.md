# Kromacut Launcher (part of the Kamillion project)

Extends [Kromacut](https://github.com/vycdev/Kromacut) (an open-source
HueForge-style multi-material 3D print tool) with:

- TD-1 hardware support (reads filament TD automatically instead of
  manual entry / print-and-measure calibration)
- An Inkscape bridge (process an image in Inkscape, send it straight
  into Kromacut with one button)
- Better print-swap output (filament names + a visual diagram instead
  of a raw hex-code list, plus real slicer/printer pause-insertion)

## Repo layout

```
kromacut-launcher/
├── inkscape-extension/   Inkscape menu extension - export + launch (working draft)
├── manager/              One-time setup program - installs everything (not started)
└── kromacut-fork/        NOT in this repo - see below
```

## About the Kromacut fork

The actual modified Kromacut (TD-1 Rust module, auto-load-on-launch,
better swap output) is **not** kept inside this repo. It should be a
real fork of https://github.com/vycdev/Kromacut on GitHub (using
GitHub's "Fork" button), since Kromacut is AGPL-3.0 licensed - any
modified/distributed version of it must stay AGPL and publish its
source. This repo (the Inkscape extension + manager) is separate
tooling around that fork, and can carry its own license.

## Status

- Inkscape extension: first working draft, untested in a real Inkscape
  install
- Manager: not started
- Kromacut fork: not started (repo doesn't exist yet)

See each folder's own README for details and open gaps.
