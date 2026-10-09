# Dots and Boxes for the TI-84 Evo (2-4 players, some can be the calculator)
# Take turns drawing a line between two dots. Close a box and it's yours,
# and you draw again. Most boxes wins.
# Keys: arrows = choose a box, 2nd = choose its side, enter = draw, clear = quit
import random
from ti_draw import clear, set_color, draw_text
from ti_draw import fill_rect as ti_fill_rect
try:
    from ti_draw import get_screen_dim
    SW, SH = get_screen_dim()
except:
    SW, SH = 319, 209

# Keep every box inside the screen and never stop the game over one box.
# The Evo draws boxes 1 pixel too small, so we ask for 1 pixel more.
def fill_rect(x, y, w, h):
    if x < 0:
        w, x = w + x, 0
    if y < 0:
        h, y = h + y, 0
    w, h = min(w, SW - x), min(h, SH - y)
    if w > 0 and h > 0:
        try:
            ti_fill_rect(x, y, w + 1, h + 1)
        except:
            pass
# Draw in a hidden buffer and show the finished picture at once: no flicker
try:
    from ti_draw import use_buffer, paint_buffer
    use_buffer()
except:
    paint_buffer = None
try:
    from ti_system import get_key as read_key
except:
    from ti_system import getKey as read_key
# On the Evo get_key wants one number. Find out once at the start.
try:
    read_key()
    key = read_key
except TypeError:
    def key():
        return read_key(0)
try:
    from ti_system import store_list, recall_list
except:
    store_list = recall_list = None
try:
    from time import sleep
except:
    from ti_system import sleep
try:
    import gc
except:
    gc = None

LEFT = (2, 24)
RIGHT = (1, 26)
UP = (3, 25)
DOWN = (4, 34)
OK = (5, 105)                 # enter
SECOND = (21, 22)             # 2nd, mode
QUIT = (9, 45)                # clear
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (150, 150, 150)
YELLOW = (255, 220, 0)

def paint():
    if paint_buffer:
        paint_buffer()

def write(x, y, s):                    # text that can never stop the game
    try:
        draw_text(x, y, s)
    except:
        pass

def wait_for(keys):
    paint()
    while True:
        k = key()
        if k in keys:
            return k
        sleep(0.05)

# Numbers saved in a calculator list, so they stay after quitting
def load(name, n):
    try:
        l = [int(v) for v in recall_list(name)]
    except:
        l = []
    return (l + [0] * n)[:n]

def save(name, l):
    try:
        store_list(name, l)
    except:
        pass

# Text panel on the right side: rows 30 px high, the whole row is wiped first
def text(row, s, col=WHITE):
    set_color(*BLACK)
    fill_rect(TX, row * 30, SW - TX, 29)
    set_color(*col)
    write(TX, row * 30 + 22, s)

def box_frame(x, y, w, h, t, col):     # a frame t pixels thick
    set_color(*col)
    fill_rect(x, y, w, t)
    fill_rect(x, y + h - t, w, t)
    fill_rect(x, y, t, h)
    fill_rect(x + w - t, y, t, h)

def title_screen(name, col, line):
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    set_color(*col)
    write(SW // 2 - 80, 25, name)
    set_color(*WHITE)
    write(SW // 2 - 80, 55, line)

# A menu on the start screen. Returns the chosen number, or -1 for clear.
def menu(options, choice, hint):
    x = SW // 2 - 80
    set_color(*BLACK)
    fill_rect(0, 64, SW, SH - 64)
    set_color(*WHITE)
    write(x, 202, hint)
    while True:
        for i in range(len(options)):
            set_color(*BLACK)
            fill_rect(x - 20, 64 + i * 28, 230, 27)
            set_color(*(YELLOW if i == choice else GREY))
            write(x, 90 + i * 28, ("> " if i == choice else "  ") + options[i])
        k = wait_for(UP + DOWN + OK + QUIT)
        if k in QUIT:
            return -1
        if k in OK:
            return choice
        if k in UP:
            choice = (choice - 1) % len(options)
        if k in DOWN:
            choice = (choice + 1) % len(options)

ROWS, COLS = 5, 5             # boxes
S = 36                        # distance between dots
X0 = 14
Y0 = (SH - ROWS * S) // 2
TX = X0 + COLS * S + 16       # text panel (black, so text is fine)
PCOL = [(230, 30, 30), (0, 190, 0), (240, 200, 0), (30, 110, 255)]
PDIM = [(110, 20, 20), (0, 90, 0), (120, 100, 0), (10, 50, 130)]
PNAME = ["Red", "Green", "Yellow", "Blue"]
SHORT = ["Red", "Grn", "Yel", "Blu"]        # fits the narrow side panel
FREE = (45, 45, 45)           # a line nobody has drawn yet
TAKEN = (255, 140, 0)         # cursor on a line that is already drawn

hl = [[0] * COLS for r in range(ROWS + 1)]   # lines across: owner + 1, 0 = free
vl = [[0] * (COLS + 1) for r in range(ROWS)] # lines down
box = [[0] * COLS for r in range(ROWS)]      # box owner + 1

def side_line(r, c, s):        # side s of box r, c: 0 top, 1 right, 2 bottom, 3 left
    return (("h", r, c), ("v", r, c + 1), ("h", r + 1, c), ("v", r, c))[s]

def get(line):
    t, r, c = line
    return hl[r][c] if t == "h" else vl[r][c]

def boxes_of(line):            # the 1 or 2 boxes next to a line
    t, r, c = line
    out = []
    if t == "h":
        for rr in (r - 1, r):
            if 0 <= rr < ROWS:
                out.append((rr, c))
    else:
        for cc in (c - 1, c):
            if 0 <= cc < COLS:
                out.append((r, cc))
    return out

def sides(r, c):
    return sum(1 for s in range(4) if get(side_line(r, c, s)))

def free_lines():
    out = [("h", r, c) for r in range(ROWS + 1) for c in range(COLS) if not hl[r][c]]
    return out + [("v", r, c) for r in range(ROWS) for c in range(COLS + 1) if not vl[r][c]]

# ---------- drawing ----------
def dot(r, c):
    set_color(*WHITE)
    fill_rect(X0 + c * S - 2, Y0 + r * S - 2, 5, 5)

def draw_line(line, col=None):
    t, r, c = line
    o = get(line)
    set_color(*(col or (PCOL[o - 1] if o else FREE)))
    x, y = X0 + c * S, Y0 + r * S
    if t == "h":
        fill_rect(x + 4, y - 1, S - 7, 3)
    else:
        fill_rect(x - 1, y + 4, 3, S - 7)

def draw_box(r, c):
    set_color(*(PDIM[box[r][c] - 1] if box[r][c] else BLACK))
    fill_rect(X0 + c * S + 4, Y0 + r * S + 4, S - 7, S - 7)

def panel(n, scores, p, comps):
    text(0, "DOTS")
    for i in range(4):
        if i < n:
            text(i + 1, (">" if i == p else " ") + SHORT[i] + " " + str(scores[i])
                 + (" C" if i >= n - comps else ""), PCOL[i])     # C = calculator
        else:
            text(i + 1, "")

# ---------- computer player ----------
def ai_line():
    lines = free_lines()
    take = [l for l in lines if any(sides(r, c) == 3 for r, c in boxes_of(l))]
    if take:
        return random.choice(take)                  # close a box
    safe = [l for l in lines if all(sides(r, c) < 2 for r, c in boxes_of(l))]
    if safe:
        return random.choice(safe)                  # gives nothing away
    best, out = 9, []                               # give away as little as possible
    for l in lines:
        g = sum(1 for r, c in boxes_of(l) if sides(r, c) == 2)
        if g < best:
            best, out = g, [l]
        elif g == best:
            out.append(l)
    return random.choice(out)

# ---------- game ----------
def place(line, p):            # draw a line; returns how many boxes it closed
    t, r, c = line
    if t == "h":
        hl[r][c] = p + 1
    else:
        vl[r][c] = p + 1
    draw_line(line)
    got = 0
    for br, bc in boxes_of(line):
        if sides(br, bc) == 4 and not box[br][bc]:
            box[br][bc] = p + 1
            draw_box(br, bc)
            got += 1
    return got

def choose_players(stats):
    title_screen("DOTS AND BOXES", PCOL[3], "Wins " + " ".join(str(w) for w in stats))
    while True:
        n = menu(["2 players", "3 players", "4 players"], 0, "UP/DOWN + ENTER")
        if n < 0:
            return None
        n += 2
        c = menu(["All people"] + [str(k) + " computer" + ("s" if k > 1 else "") for k in range(1, n)],
                 0, "CLEAR: back")
        if c >= 0:
            return n, c

def game(n, comps):            # returns the scores, or None for quit
    for r in range(ROWS + 1):
        hl[r] = [0] * COLS
    for r in range(ROWS):
        vl[r] = [0] * (COLS + 1)
        box[r] = [0] * COLS
    clear()
    set_color(*BLACK)
    fill_rect(0, 0, SW, SH)
    for l in free_lines():
        draw_line(l)
    for r in range(ROWS + 1):
        for c in range(COLS + 1):
            dot(r, c)
    scores, p = [0] * n, 0
    br, bc, s = ROWS // 2, COLS // 2, 0
    text(6, "CLEAR:quit")
    while free_lines():
        panel(n, scores, p, comps)
        if p >= n - comps:                          # computer player
            paint()
            sleep(0.4)
            line = ai_line()
        else:
            while True:
                line = side_line(br, bc, s)
                draw_line(line, TAKEN if get(line) else YELLOW)
                k = wait_for(LEFT + RIGHT + UP + DOWN + SECOND + OK + QUIT)
                draw_line(line)
                if k in QUIT:
                    return None
                if k in OK and not get(line):
                    break
                if k in LEFT:
                    bc = max(0, bc - 1)
                elif k in RIGHT:
                    bc = min(COLS - 1, bc + 1)
                elif k in UP:
                    br = max(0, br - 1)
                elif k in DOWN:
                    br = min(ROWS - 1, br + 1)
                elif k in SECOND:
                    s = (s + 1) % 4
        got = place(line, p)
        if got:
            scores[p] += got                        # closed a box: go again
        else:
            p = (p + 1) % n
    panel(n, scores, -1, comps)
    return scores

# --- start ---
stats = load("DOTS", 4)        # wins per colour
while True:
    setup = choose_players(stats)
    if setup is None:
        break
    n, comps = setup
    scores = game(n, comps)
    if scores is None:
        continue
    top = max(scores)
    winners = [i for i in range(n) if scores[i] == top]
    if len(winners) == 1:
        stats[winners[0]] += 1
        save("DOTS", stats)
        text(5, SHORT[winners[0]] + " wins!", PCOL[winners[0]])
    else:
        text(5, "Draw!")
    text(6, "ENTER:menu")
    if wait_for(OK + QUIT) in QUIT:
        break
paint()
