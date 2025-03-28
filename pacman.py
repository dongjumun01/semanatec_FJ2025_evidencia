"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import choice  # Import choice for random ghost movement
import turtle  # Import turtle for graphics
from freegames import floor, vector  # Import helper and vector for movement

# Global state dictionary to track the game score
state = {'score': 0}

# Turtle objects for drawing
path = turtle.Turtle(visible=False)  # Used to draw the maze
writer = turtle.Turtle(visible=False)  # Used to display the score

point = turtle.Turtle(visible=False)  # New turtle for points
point.speed(0)  # No animation
point.up()  # Lift pen to move it

# Pacman's movement direction
aim = vector(5, 0)

# Initial position of Pacman
pacman = vector(-40, -80)

# List of ghosts with their starting positions and movement directions
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
# Maze layout: 0 represents walls, 1 represents paths with dots
# fmt: off
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
# fmt: on


def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world():
    """Draw world using path."""
    # 1. Changing the board's color
    turtle.bgcolor('red')
    path.color('black')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                # 2. Changing the shape and color of the points
                point.goto(x + 6, y + 6)  # Adjust position
                point.down()
                point.color('green')  # Change color of points
                point.begin_fill()
                for _ in range(4):  # Draw a small square for points
                    point.forward(8)
                    point.left(90)
                point.end_fill()
                point.up()  # Lift the pen to prevent unwanted lines


def move():
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'])

    turtle.clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    turtle.up()
    turtle.goto(pacman.x + 10, pacman.y + 10)
    turtle.dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            # 3. Making the ghosts go faster
            # Increasing the magnitude of their movement
            options = [
                vector(20, 0),
                vector(-20, 0),
                vector(0, 20),
                vector(0, -20),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        turtle.up()
        turtle.goto(point.x + 10, point.y + 10)
        turtle.dot(20, 'red')

    turtle.update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return
    # Move every 50 milliseconds (faster)
    turtle.ontimer(move, 50)


def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


# Set up the game window
turtle.setup(420, 420, 370, 0)
turtle.hideturtle()
turtle.tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])

# Listen for keyboard inputs
turtle.listen()
turtle.onkey(lambda: change(5, 0), 'Right')
turtle.onkey(lambda: change(-5, 0), 'Left')
turtle.onkey(lambda: change(0, 5), 'Up')
turtle.onkey(lambda: change(0, -5), 'Down')

# Initialize game world and movement
world()
move()
turtle.done()
