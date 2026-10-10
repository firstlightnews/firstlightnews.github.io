# First Light News — saved ideas (not live)

This branch stores design ideas that were previewed but not published. The live site is on `main`.

## about-popup/
Clicking the script F (header tile in the Original look, footer F in both looks) spins/grows the logo, then opens an
"About First Light News" pop-up (Win95-style dialog in Original, newspaper notice box in Print Edition).
Previews: about-preview.png, spin-retro.mp4, spin-print.mp4. Saved 2026-10-10.
Restore: use about-popup/base-index.html and about-popup/classic2.css as the sources, then
`python3 build/finalbuild.py about-popup/base-index.html index.html` (the other CSS files live in build/).
Note: re-apply any later changes made on main (e.g. diff against main's index.html) before publishing.

## cover-graphics/
Drawn cover graphic for The day in brief: pixel/engraved hurricane inset map over the Gulf, and waving flags for
conflict stories. Previews: map-preview.png, flags-preview.png. Shelved 2026-10-10 ("no graphics").
Needs a `digest.cover` field from the morning refresh to show anything.
