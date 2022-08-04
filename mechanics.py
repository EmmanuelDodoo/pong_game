
from random import randint
import pygame
from objects import Rectangle, Ball, WindowMgr

# Colors to be used later
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ANTIQUEWHITE = (250, 235, 215)
TOMATO = (255, 99, 71)
IVORY = (255, 255, 240)
GREY = (70, 68, 76)  # Actual name is night grey


pygame.init()
# Display size. Linked with the values in object.py
display = pygame.display.set_mode((900, 675))
pygame.display.set_caption('Emmanuel\'s pong')
# Sets how often key presses are registered in milliseconds
pygame.key.set_repeat(100)
clock = pygame.time.Clock()  # Used later on to set the frame rate

# Bring game WIndow to foreground
w = WindowMgr()
w.find_window_wildcard("Emmanuel's pong")
w.set_foreground()


def draw(r1: Rectangle, r2: Rectangle, b: Ball) -> None:
    """Draws the rectangles and ball for the pong games
       `r1` & `r2` must be Rectangle objects. `b` must be a Ball object.
    """
    assert isinstance(r1, Rectangle)
    assert isinstance(r2, Rectangle)
    assert isinstance(b, Ball)

    display.fill(ANTIQUEWHITE)
    # Draw Rectangles
    pygame.draw.rect(display, r1.color, r1.position)
    pygame.draw.rect(display, r2.color, r2.position)

    # Draw ball
    pygame.draw.circle(display, b.color, b.position, b.RADIUS)

    # Update the display with drawn objects
    pygame.display.update()


def bounce(rect: Rectangle, b: Ball, m: int, TOP: bool = True) -> int:
    """Determines how the ball should bounce on interaction with the rectangles.
       Returns an int for Ball.move()
       rect: Rectangle Object
       b: Ball object
       m: current Ball.move() code
       TOP: whether rect is top or bottom"""

    assert isinstance(rect, Rectangle), '`rect` must be a Rectangle Object'
    assert isinstance(b, Ball), '`b` must be a Ball Object'
    assert isinstance(m, int) and abs(m) in (
        1, 2, 3), '`m` must have an absolute value in (1,2,3)'
    assert isinstance(TOP, bool)

    """The rectangle is divided into 3 subregions. The ball's bounce direction is determined
    by which region it hits"""
    edge1 = rect.left  # the left most edge
    edge2 = edge1 + 60  # the next edge.
    # Region 1 is therefore 60px wide
    edge3 = edge2 + 7  # 3rd edge
    # Region 2 is 7px wide
    edge4 = rect.left + rect.WIDTH + 5  # ball passes through without the 5
    # Region 3 is the rest of the width

    if b.x >= edge1 and b.x < edge2:  # bounce on the left subregion
        if TOP:
            # making sure the ball is above the rectangle when bouncing
            if b.y <= (rect.top+rect.HEIGHT+b.RADIUS):
                return 1
            else:
                return m
        else:
            if b.y >= rect.top - b.RADIUS:  # counting from top to bottom
                return -1
            else:
                return m

    elif b.x >= edge2 and b.x < edge3:  # bounce on the middle region
        if TOP:
            if b.y <= rect.top + rect.HEIGHT + b.RADIUS:
                return 2
            else:
                return m
        else:
            if b.y >= rect.top - b.RADIUS:
                return -2
            else:
                return m

    elif b.x >= edge3 and b.x <= edge4:  # bounce on the right region
        if TOP:
            if b.y <= rect.top + rect.HEIGHT + b.RADIUS:
                return 3
            else:
                return m
        else:
            if b.y >= rect.top - b.RADIUS:
                return -3
            else:
                return m
    else:
        return m


def boundaries(b: Ball, m: int) -> int:
    """Determines ball, `b`, movement at boundaries
       m: current Ball.move() code. Must have absolute value of 1,2 or 3"""

    assert isinstance(b, Ball), '`b` must be a Ball object'
    assert isinstance(m, int) and abs(m) in (1, 2, 3), 'Invalid m input'

    dis_x, dis_y = pygame.display.get_window_size()  # get size of window

    # For vertical boundaries
    if b.x >= dis_x - b.RADIUS or b.x <= b.RADIUS:  # At the boundaries

        if b.x > dis_x-b.RADIUS:  # on the right boundary
            b.x = dis_x-b.RADIUS
        if b.x < b.RADIUS:  # on the left boundary
            b.x = b.RADIUS
        # Change ball direction
        match m:
            case 1:
                m = 3
            case 3:
                m = 1
            case -1:
                m = -3
            case -3:
                m = -1
            case _:
                m = -m

    # For Horizontal boundaries
    if b.y >= dis_y-b.RADIUS or b.y <= b.RADIUS:
        if b.y >= dis_y-b.RADIUS:  # on the bottom boundary
            b.y = dis_y-b.RADIUS
        if b.y <= b.RADIUS:  # on the top boundary
            b.y = b.RADIUS
        # Change ball direction
        match m:
            case 1:
                m = -3
            case 3:
                m = -1
            case -1:
                m = 3
            case -3:
                m = 1
            case _:
                m = -m

    return m


def speedchange(b: Ball, reverse: bool = False) -> None:
    """Auxillary function to cycle through ball speed
       `b`: a Ball object
       `reverse`: boolean value to determine an increase or decrease
       `reverse[True]: decreases
       `reverse[False]: increases"""

    assert isinstance(b, Ball), 'Invalid `b` input'
    assert reverse in (True, False)

    if not reverse:
        match b.speed:
            case 's':
                b.chspeed('m')
            case 'm':
                b.chspeed('f')
            case _:
                return
    else:
        match b.speed:
            case 'f':
                b.chspeed('m')
            case 'm':
                b.chspeed('s')
            case _:
                return


def play(speed: str) -> None:
    """Starts the game. Top rectangle is controlled with a & d. Bottom rectangle controlled
       arrow keys
       speed:(s)low, (m)edium, (f)ast 
    """
    assert isinstance(speed, str) and speed.lower() in ['s', 'm', 'f']
    speed = speed.lower()

    s_d = randint(1, 3)  # Random starting direction for ball
    top_rect = Rectangle(GREY, True)
    bot_rect = Rectangle(GREY)
    ball = Ball(TOMATO, speed)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quits the game and stops the script if the window is closed
                pygame.quit
                quit()
            elif event.type == pygame.KEYDOWN:  # handles keyboard inputs
                match event.key:
                    case pygame.K_d:
                        top_rect.move(25)
                    case pygame.K_a:
                        top_rect.move(-25)
                    case pygame.K_LEFT:
                        bot_rect.move(-25)
                    case pygame.K_RIGHT:
                        bot_rect.move(25)

                    # To change the speed of ball
                    # need to increase key event interval for this specifically
                    case pygame.K_UP:
                        speedchange(ball)
                    case pygame.K_DOWN:
                        speedchange(ball, True)

                    # for debugging purposes
                    # case pygame.K_j:
                    #     print(top_rect)
                    # case pygame.K_k:
                    #     print(bot_rect)
                    # case pygame.K_l:
                    #     print(ball)

        s_d = boundaries(ball, s_d)
        s_d = bounce(top_rect, ball, s_d)
        s_d = bounce(bot_rect, ball, s_d, False)
        ball.move(s_d)
        draw(top_rect, bot_rect, ball)
        clock.tick(90)  # Set the frame-rate


'''................End..............'''
