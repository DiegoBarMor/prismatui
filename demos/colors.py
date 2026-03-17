import curses

import os, sys; sys.path.insert(0, os.getcwd()) # allow imports from root folder
import prismatui as pr

# //////////////////////////////////////////////////////////////////////////////
class TUI(pr.Terminal):
    def __init__(self):
        super().__init__()
        self.chars: list[str] = []
        self.attrs: list[list[int]] = []

    # --------------------------------------------------------------------------
    def on_start(self):
        for i in range(1, pr.MAX_PALETTE_COLORS):
            ### notice that pair 0 is the only one initialized by default (curses)
            ### it corresponds to white FG and black BG
            ###
            ### colors, on the other hand, are initialized with defualt values
            ### in this example, pairs will be assigned to their corresponding color,
            ### starting from 1 (note that color 0 is black)
            pr.init_pair(i, pr.COLOR_BLACK, i)

        self._update_matrices()

    # --------------------------------------------------------------------------
    def on_update(self):
        match self.key:
            case pr.KEY_P_LOWER: self._toggle_palette()
            case pr.KEY_P_UPPER: self._toggle_palette()

        self.draw_matrix(0, 0, self.chars, self.attrs)
        self.draw_text('b','l', "Press q to exit", pr.get_color_pair(6))

    # --------------------------------------------------------------------------
    def on_resize(self):
        self._update_matrices()

    # --------------------------------------------------------------------------
    def should_stop(self):
        return self.key in (pr.KEY_Q_LOWER, pr.KEY_Q_UPPER)

    # --------------------------------------------------------------------------
    def _update_matrices(self):
        def get_mat_idx(row: int, col: int, wpr) -> int:
            return (row * wpr + col) % pr.MAX_PALETTE_COLORS

        def get_color_str(i: int) -> str:
            return f"color{i:03d} "

        len_word = len(get_color_str(0))
        nrows = self.h - 2
        words_per_row = self.w // len_word

        self.chars = [
            ''.join(
                get_color_str(get_mat_idx(i,j,words_per_row))
                for j in range(words_per_row)
            )
            for i in range(nrows)
        ]
        self.attrs = [
            [
                pr.get_color_pair(get_mat_idx(i,j,words_per_row))
                for j in range(words_per_row)
                for _ in range(len_word)
            ]
            for i in range(nrows)
        ]

    # --------------------------------------------------------------------------
    def _toggle_palette(self):
        pr.Palette.load_pal("demos/data/cat.pal").apply()


################################################################################
if __name__ == "__main__":
    tui = TUI()
    tui.run()


################################################################################
