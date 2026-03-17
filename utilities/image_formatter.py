##### [WIP] Work In Progress #####

import numpy as np
from PIL import Image
from pathlib import Path
from collections import Counter

import prismatui as pr

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def open_img(PATH_IMG: Path) -> np.array:
    img = Image.open(PATH_IMG).convert("RGBA")
    return np.array(img)

# ------------------------------------------------------------------------------
def sep_channels(img: np.array) -> tuple[np.array]:
    rgb = img[:,:,:3]
    alpha = img[:,:,3]
    return rgb2curses(rgb), alpha

# ------------------------------------------------------------------------------
def rgb2curses(rgb):
    return 1000 * rgb.astype(int) / 255


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def generate_palette(img: np.array) -> np.array:
    rgb,alpha = sep_channels(img)
    bg = rgb[alpha >= pr.ALPHA_THRESHOLD]
    lst_colors = [tuple(color) for color in bg.reshape(-1,3)]

    colors = [
        t[0] for t in sorted(
            Counter(lst_colors).items(), key = lambda t: t[1], reverse = True
        )
    ]
    out_colors = colors[:pr.MAX_PALETTE_COLORS]
    out_pairs = [(-1, OFFSET_COLOR + i) for i in range(len(out_colors))]
    ### ^^^ fg is automatically set to -1 (i.e. default curses foreground) for all pairs
    ### this can be changed in the .pal file if needed

    print(f"Extracted {len(out_colors)}/{len(colors)} colors into palette")
    return out_colors, out_pairs


# ------------------------------------------------------------------------------
def to_palette_values(img: np.array, palcolors: np.array) -> np.array:
    rgb,alpha = sep_channels(img)
    w, h, _ = rgb.shape # (w,b,3)
    rgb_flat = rgb.reshape(-1, 3) # (w,h,3)->(w*h,3)
    rgb_broad = rgb_flat[:,None,:] # (w*h,3)->(w*h,1,3)
    palette_broad = palcolors[None,:,:] # (p,3)->(1,p,3)
    dists = np.sum((rgb_broad - palette_broad) ** 2, axis = 2) # (w*h,p)
    idxs = np.argmin(dists, axis = 1) # (w*h,)
    idxs = idxs.reshape(w,h) # (w,h)
    idxs[alpha < pr.ALPHA_THRESHOLD] = -pr.COLOR_PAIR_OFFSET # will be shifted to 0, which represents transparent pixels

    unique_colors = set([tuple(color) for color in rgb_flat])
    unique_palvals = set(idxs[idxs > -pr.COLOR_PAIR_OFFSET].flatten())

    print(f"Converted img from {len(unique_colors)} colors to {len(unique_palvals)} palette values")

    return idxs + pr.COLOR_PAIR_OFFSET # shift palette values to account for reserved default colors (0 is reserved for transparent pixels)


# ------------------------------------------------------------------------------
def main():
    img = open_img(PATH_IMG)
    colors, pairs = generate_palette(img)

    pal = pr.Palette(8, colors, pairs)
    pal.save_pal(PATH_PAL)

    pal = pr.Palette.load_pal(PATH_PAL)
    colors = np.array(pal.colors)
    arr = to_palette_values(img, colors)

    chars = np.full_like(arr, ' ', dtype = str)
    chars[arr > 0] = ' '
    chars = [''.join(row) for row in chars]

    pr.save_layer(
        PATH_PRI, pr.Layer(0, 0, chars = chars, attrs = arr)
    )


################################################################################
if __name__ == "__main__":
    # mode = sys.argv[1]
    # PATH_IMG = Path(sys.argv[2])
    PATH_IMG = Path("demos/data/cat.png")
    PATH_PAL = Path("demos/data/cat.pal")
    PATH_PRI = PATH_IMG.with_suffix(".pri")
    OFFSET_COLOR = 8
    main()


################################################################################
### Reference default colors:
# 0: curses.COLOR_BLACK   --> (  0,  0,  0)
# 1: curses.COLOR_RED     --> (680,  0,  0)
# 2: curses.COLOR_GREEN   --> (  0,680,  0)
# 3: curses.COLOR_YELLOW  --> (680,680,  0)
# 4: curses.COLOR_BLUE    --> (  0,  0,680)
# 5: curses.COLOR_MAGENTA --> (680,  0,680)
# 6: curses.COLOR_CYAN    --> (  0,680,680)
# 7: curses.COLOR_WHITE   --> (680,680,680)
