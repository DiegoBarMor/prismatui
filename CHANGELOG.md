# Changelog

## [0.3.2] - 2026-02-19
- Fixed bug where negative y/x positions were not dealt with correctly by the draw methods.
- Removed visual artifacts remaining after a terminal resize.

## [0.3.1] - 2026-02-18
- `draw_text` methods now return the length of the string provided to them (before any processing, including `\n` characters).
- `draw_text` methods can now receive an attribute matrix directly.
- Fixed bug where PrismaTUI would crash if a `draw_matrix` method received an empty list.

## [0.3.0] - 2026-01-26
- Renamed package again from `prisma-tui` to `prismatui` for simplicity.
- Removed nested `_tui` directory.
- Added more constants for the ASCII characters (32-126).

## [0.2.1] - 2025-11-30
- Attempted to reduce input lag by exhausting repeated keys in `BackendCurses._get_key`.
- Palettes can now be loaded directly from a dictionary instead of a JSON file.
- Package no longer nested inside a `src/` directory.

## [0.2.0] - 2025-10-07
- Renamed the package from `prisma` into `prisma-tui` to avoid name conflicts with other packages using the word "prisma".

## [0.1.1] - 2025-06-01
- Added README and some documentation.

## [0.1.0] - 2025-05-30
- Initial upload to PyPI of a preliminary **Prisma TUI**.
