# Dots and Boxes for the TI-84 Evo-T

The pen-and-paper game **Dots and Boxes** for the **TI-84 Evo-T** graphing calculator, written in Python.
For 2 to 4 players. Empty seats can be played by the calculator.

> **Made with AI:** this game and this README were created with the help of AI (Claude by Anthropic).
> Everything was tested on a real TI-84 Evo-T.

## What is Dots and Boxes?

- The board has **6 × 6 dots**, so there are **25 boxes**.
- Players take turns drawing **one line** between two dots next to each other.
- Draw the **4th side** of a box and the box is **yours**, and you **draw again**.
- When all lines are drawn, the player with the **most boxes** wins.

**Tip:** try **not** to draw the 3rd side of a box. That gives the next player an easy box,
and often a whole row of them.

## Features

- **2 to 4 players**: red, green, yellow and blue
- **Computer players** for empty seats (marked with a **C**)
- The score list on the right, with **>** showing whose turn it is
- Wins per colour stay saved after you quit

## What you need

- A **TI-84 Evo-T** calculator
- A USB cable to connect it to your computer
- **Google Chrome** or **Microsoft Edge** (Safari and Firefox do not work with the TI tool)
- The file [`dots.py`](dots.py) from this repo

## Setup

1. Download [`dots.py`](dots.py) to your computer.
2. Connect the calculator to your computer with the USB cable.
   Leave the calculator on the **home screen**.
3. Open **https://connectevo.ti.com** in **Chrome** or **Edge**.
4. Connect to your calculator in the page and allow access when the browser asks.
5. Drag `dots.py` onto the page to send it to the calculator.
6. **Choose RAM** to play right away.
   The Python app on the Evo-T only shows files that are in RAM.
   (Want to keep the game safe? See [Don't lose the game](#dont-lose-the-game).)

> **Already sent it to Archive?** On the **home screen** (not in the Python app) press **2nd → mem → Mem Management**,
> find **DOTS** and press **enter**. The `*` in front of the name disappears, which means
> it is now in RAM.

## Start the game

1. Open the **Python** app on the calculator.
2. Choose **DOTS** and run it.
3. Choose **2, 3 or 4 players** with ▲ ▼ and press **enter**.
4. Choose how many are the **calculator** ("All people", "1 computer" …).

## Keys

| Key | What it does |
|---|---|
| ◀ ▶ ▲ ▼ | Choose a box |
| 2nd | Choose which side of that box (top, right, bottom, left) |
| enter | Draw that line |
| clear | Quit |

The line you are about to draw is **yellow**. If it is **orange**, that line is already drawn.

## Don't lose the game

The Evo-T **deletes RAM** when it stays turned off for a while.
A normal turn-off is fine, but after some time the game is gone.

**Best way:**

1. Keep the game in **Archive**. Archive is never deleted.
2. Go to the **home screen**. If you are in the Python app, leave it with **2nd → quit**
   (quit is above the **mode** key). In the Python app, **2nd → mem** does nothing.
3. Press **2nd → mem** (mem is above the **+** key) and choose **2: Mem Management**.
4. Choose the list with Python programs (or **All**).
5. Find **DOTS** and press **enter**. The `*` disappears, which means the game is now in RAM.
6. Open the **Python** app and play.

Programs can't move files between Archive and RAM by themselves, so this step can't be automatic.
The wins list **DOTS** is in RAM too, so it can be deleted the same way.

## Wins

The wins of each colour are saved in a calculator list called **DOTS**, so they stay after you quit.
The start screen shows them.

- To reset them, delete the list **DOTS** in **2nd → mem → Mem Management** (on the home screen).
- A calculator reset (RAM clear) also resets them.

## Good to know

- Keep `dots.py` on your computer too, so you can always send it again.
- Made for the TI-84 Evo-T. Other TI-84 models are not tested.
