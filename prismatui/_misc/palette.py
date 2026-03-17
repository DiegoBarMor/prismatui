import json

import prismatui as pr

# ------------------------------------------------------------------------------
def apply_int(lst: list[tuple]) -> list[tuple[int]]:
    """Just to make sure all values in the list of tuples are integers..."""
    return [tuple(int(x) for x in tup) for tup in lst]


# //////////////////////////////////////////////////////////////////////////////
class Palette:
    """Class to manage colors and palette files."""
    def __init__(self,
        offset: int = 8,
        colors: list[tuple[int,int,int]] = None,
        pairs: list[tuple[int,int]] = None
    ):
        self.offset = offset
        self.colors = [] if colors is None else apply_int(colors)
        self.pairs  = [] if pairs  is None else apply_int(pairs )

    # --------------------------------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict) -> "Palette":
        """
        Load a palette from a dictionary. It must contain the following keys: 'offset', 'colors', 'pairs'.
        Offset is the starting index for custom colors (default is 8, since 0-7 are usually reserved for default curses colors).
        Colors should be a list of (r,g,b) values in the range 0-1000.
        Pairs should be a list of (fg,bg) indices.
        """
        for key in ("offset", "colors", "pairs"):
            assert key in data, f"Palette dictionary must contain '{key}' key."

        return cls(int(data["offset"]), data["colors"], data["pairs"])

    # --------------------------------------------------------------------------
    @classmethod
    def load_json(self, path_json: str) -> "Palette":
        """Load a palette from a JSON file."""
        with open(path_json, 'r') as file:
            return self.from_dict(json.load(file))

    # --------------------------------------------------------------------------
    @classmethod
    def load_pal(self, path_pal: str) -> "Palette":
        """Alias for `Palette.load_json()`"""
        return self.load_json(path_pal)

    # --------------------------------------------------------------------------
    def save_pal(self, path_pal: str) -> None:
        """Save the current palette to a JSON file."""
        data = {
            "offset": self.offset,
            "colors": self.colors,
            "pairs": self.pairs
        }
        with open(path_pal, 'w') as file:
            json.dump(data, file)

    # --------------------------------------------------------------------------
    def apply(self) -> None:
        """
        Apply the palette to the current backend. This will initialize the colors and pairs in the terminal.
        """
        if not pr._CURRENT_BACKEND.supports_color(): return

        max_colors = pr.MAX_PALETTE_COLORS - self.offset
        max_pairs  = pr.MAX_PALETTE_PAIRS  - pr.COLOR_PAIR_OFFSET

        if len(self.colors) > max_colors:
            raise ValueError(f"Palette has {len(self.colors)} colors, max is {max_colors}.")
        if len(self.pairs) > max_pairs:
            raise ValueError(f"Palette has {len(self.pairs)} pairs, max is {max_pairs}.")

        for i,(r,g,b) in enumerate(self.colors):
            pr._CURRENT_BACKEND.init_color(self.offset + i, r, g, b)

        for i,(fg,bg) in enumerate(self.pairs):
            pr._CURRENT_BACKEND.init_pair(pr.COLOR_PAIR_OFFSET + i, fg, bg)


# //////////////////////////////////////////////////////////////////////////////
