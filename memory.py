"""Memory, puzzle game of number pairs.

Exercises:

1. Count and print how many taps occur.
2. Decrease the number of tiles to a 4x4 grid.
3. Detect when all tiles are revealed.
4. Center single-digit tile.
5. Use letters instead of tiles.
"""

from random import *
from turtle import *

from freegames import path

car = path('car.gif')
tiles = list(range(18)) * 2
state = {'mark': None}
hide = [True] * 36
pairs = 0

def show_pairs():
    """Show how many pairs have been revealed"""
    up()
    goto(-375, 170)
    color('blue')
    write('Pairs: ' + str(pairs), 
    font=('Arial', 30, 'normal'))


def draw_ending():
    """Display message when all pairs 
    have been revealed"""
    up()
    goto(-250, 210)
    color('red')
    write('Congratulations! You found all the pairs', 
    font=('Arial', 30, 'normal'))


def square(x, y):
    """Draw white square with black outline at (x, y)."""
    up()
    goto(x, y)
    down()
    color('black', 'white')
    begin_fill()
    for count in range(4):
        forward(67)
        left(90)
    end_fill()


def index(x, y):
    """Convert (x, y) coordinates to tiles index."""
    return int((x + 201) // 67 + ((y + 201) // 67) * 6)


def xy(count):
    """Convert tiles count to (x, y) coordinates."""
    return (count % 6) * 67 - 201, (count // 6) * 67 - 201


def tap(x, y):
    """Update mark and hidden tiles based on tap."""
    spot = index(x, y)
    mark = state['mark']
    global pairs 

    if mark is None or mark == spot or tiles[mark] != tiles[spot]:
        state['mark'] = spot
        
    else:
        hide[spot] = False
        hide[mark] = False
        state['mark'] = None
        pairs = pairs + 1
        show_pairs()


def draw():
    """Draw image and tiles."""
    clear()
    goto(0, 0)
    shape(car)
    stamp()
    show_pairs()

    for count in range(36):
        if hide[count]:
            x, y = xy(count)
            square(x, y)

    mark = state['mark']

    if mark is not None and hide[mark]:
        x, y = xy(mark)
        up()
        goto(x + 2, y)
        color('black')
        write(tiles[mark], font=('Arial', 30, 'normal'))
    if pairs == 18:
        draw_ending()

    update()
    ontimer(draw, 100)

shuffle(tiles)
setup(850, 520, 370, 0)
addshape(car)
hideturtle()
tracer(False)
onscreenclick(tap)
draw()
done()
