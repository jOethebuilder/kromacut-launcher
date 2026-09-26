#!/usr/bin/env python3
"""
Send to Kromacut - Inkscape extension

Exports the current document as a PNG, runs a processing pass depending on
the chosen target type (lithophane / color layer), then launches Kromacut
with the processed image as a command-line argument so Kromacut can auto-load
it on startup.

Requires: inkex (bundled with Inkscape), Pillow (for image processing).
Install Pillow into Inkscape's bundled Python if it's missing:
    <inkscape-python> -m pip install Pillow
"""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import inkex

CONFIG_DIR = Path.home() / ".kamillion"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config():
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


def find_inkscape_binary():
    """Best-effort guess at the running Inkscape executable, so we can
    shell out to it again to render the export. Inkscape sets this for
    extensions in some versions; fall back to 'inkscape' on PATH."""
    return os.environ.get("INKSCAPE_COMMAND", "inkscape")


class SendToKromacut(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--mode", type=str, default="lithophane")
        pars.add_argument("--kromacut_path", type=str, default="")

    def effect(self):
        cfg = load_config()

        # Resolve the Kromacut executable path: use what was typed in,
        # otherwise fall back to whatever was saved from a previous run.
        kromacut_path = self.options.kromacut_path.strip()
        if kromacut_path:
            cfg["kromacut_path"] = kromacut_path
            save_config(cfg)
        else:
            kromacut_path = cfg.get("kromacut_path", "")

        if not kromacut_path:
            raise inkex.AbortExtension(
                "No Kromacut executable path set. Enter it once and it will "
                "be remembered for next time."
            )
        if not Path(kromacut_path).exists():
            raise inkex.AbortExtension(
                f"Kromacut executable not found at: {kromacut_path}"
            )

        # 1. Export the current document to a temp PNG.
        raw_png = Path(tempfile.gettempdir()) / "kamillion_staged_raw.png"
        self._export_png(raw_png)

        # 2. Process it based on target type.
        final_png = Path(tempfile.gettempdir()) / "kamillion_staged.png"
        if self.options.mode == "lithophane":
            self._process_lithophane(raw_png, final_png)
        else:
            # Color-layer processing pipeline isn't decided yet - passing
            # the image through unchanged until that's scoped out.
            final_png.write_bytes(raw_png.read_bytes())

        # 3. Launch Kromacut with the processed file as an argument.
        subprocess.Popen([kromacut_path, str(final_png)])

    def _export_png(self, out_path: Path):
        svg_path = self.options.input_file
        inkscape_bin = find_inkscape_binary()
        result = subprocess.run(
            [
                inkscape_bin,
                svg_path,
                "--export-type=png",
                f"--export-filename={out_path}",
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0 or not out_path.exists():
            raise inkex.AbortExtension(
                f"Export to PNG failed: {result.stderr.strip()}"
            )

    def _process_lithophane(self, src: Path, dst: Path):
        """Settled pipeline for lithophane targets: grayscale + contrast
        stretch so the brightness range actually spans light-to-dark."""
        try:
            from PIL import Image, ImageOps
        except ImportError:
            raise inkex.AbortExtension(
                "Pillow is required for lithophane processing. Install it "
                "into Inkscape's Python with: pip install Pillow"
            )

        img = Image.open(src).convert("L")  # grayscale
        img = ImageOps.autocontrast(img, cutoff=1)  # stretch contrast
        img.save(dst)


if __name__ == "__main__":
    SendToKromacut().run()
