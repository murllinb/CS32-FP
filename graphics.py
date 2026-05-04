# graphics.py
import turtle

# Map row, col to exact X, Y coordinates on the turtle screen
COORDS = {
    (0, 0): (-100, 100), (0, 1): (0, 100), (0, 2): (100, 100),
    (1, 0): (-100, 0),   (1, 1): (0, 0),   (1, 2): (100, 0),
    (2, 0): (-100, -100),(2, 1): (0, -100),(2, 2): (100, -100)
}

def setup_turtle_screen():
    screen = turtle.Screen()
    screen.title("Galaxy Tic-Tac-Toe")
    screen.setup(width=600, height=600)
    
    try:
        screen.bgpic("galaxy.gif")
    except turtle.TurtleGraphicsError:
        screen.bgcolor("black") 
        
    screen.tracer(0) 
    
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.pensize(5)
    return screen, pen

def draw_grid(pen):
    pen.color("cyan") 
    
    # Vertical lines
    for x in [-50, 50]:
        pen.penup()
        pen.goto(x, 150)
        pen.pendown()
        pen.goto(x, -150)

    # Horizontal lines
    for y in [50, -50]:
        pen.penup()
        pen.goto(-150, y)
        pen.pendown()
        pen.goto(150, y)

def draw_x(pen, x, y):
    pen.color("red")
    pen.penup()
    pen.goto(x - 30, y + 30)
    pen.pendown()
    pen.goto(x + 30, y - 30)
    pen.penup()
    pen.goto(x + 30, y + 30)
    pen.pendown()
    pen.goto(x - 30, y - 30)

def draw_o(pen, x, y):
    pen.color("lime")
    pen.penup()
    pen.goto(x, y - 30) 
    pen.pendown()
    pen.circle(30)

def sync_turtle_board(board, pen, screen):
    pen.clear() 
    draw_grid(pen) 
    
    for row in range(3):
        for col in range(3):
            mark = board[row][col]
            if mark != " ":
                x, y = COORDS[(row, col)]
                if mark == "X":
                    draw_x(pen, x, y)
                elif mark == "O":
                    draw_o(pen, x, y)
                    
    screen.update()
