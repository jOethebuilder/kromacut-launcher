SEND TO KROMACUT - Inkscape extension (first working draft)
=============================================================

WHAT THIS DOES
--------------
Adds "Extensions > Kamillion > Send to Kromacut" in Inkscape.
When you run it:
  1. Exports your current document as a PNG
  2. If mode = Lithophane: converts to grayscale + auto-contrast
     (color-layer processing is NOT decided yet - currently passes
     the image through unchanged for that mode)
  3. Launches Kromacut, passing the processed PNG as an argument

INSTALL (one-time, manual for now - the "manager" will automate this later)
----------------------------------------------------------------------------
1. Find your Inkscape user extensions folder:
   - Windows: %APPDATA%\Inkscape\extensions
   - Mac:     ~/Library/Application Support/org.inkscape.Inkscape/config/inkscape/extensions
   - Linux:   ~/.config/inkscape/extensions
2. Copy both send_to_kromacut.inx and send_to_kromacut.py into that folder
3. Restart Inkscape
4. First time you run it, type the full path to your Kromacut executable
   into the "Kromacut executable" field - it's saved after that
   (~/.kamillion/config.json) so you won't need to enter it again

REQUIRES
--------
- Pillow, inside Inkscape's own bundled Python:
    <path-to-inkscape-python> -m pip install Pillow
  (Inkscape 1.x ships its own Python; you can't just "pip install" globally
  and expect Inkscape to see it)

NOT YET DONE / KNOWN GAPS
--------------------------
- Color-layer image processing pipeline: still undecided what
  adjustments should auto-run. Currently a no-op passthrough.
- This hasn't been tested inside a real Inkscape install yet - I don't
  have Inkscape available to run it in this environment. Try it and
  tell me what breaks.
- Kromacut's fork doesn't yet read a command-line file argument on
  startup - that side still needs to be added for the auto-load to work.
