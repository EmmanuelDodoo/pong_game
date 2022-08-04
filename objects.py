"""Object Classes Used in pong game"""
# For getting active window
import win32gui
import re
# To solve an error which appeared
import win32com.client  # FUll solution in WindowMgr.set_foreground


class Rectangle:
    """Rectangle Object for the pong game.
       Class Attributes: LEFT=10, WIDTH=127, HEIGHT=38"""

    # Starting positions in pixels
    LEFT = 10
    WIDTH = 127
    HEIGHT = 27

    def __init__(self, color: tuple = (0, 0, 0), top: bool = False) -> None:
        """ color: rgb
        """
        self.color = color
        self.left = self.LEFT
        self.top = 5 if top else 640
        self.position = (self.left, self.top, self.WIDTH, self.HEIGHT)

    def move(self, l: int) -> None:
        """ Moves the rectangle horizontally. Padding of 5px on each side
        l: an int representing move distance
        """
        assert isinstance(l, int), 'Invalid move. `l` must be an int'

        if self.left+l < 5:
            self.left = 5
        elif self.left+l > 768:
            self.left = 768
        else:
            self.left += l

        self.position = (self.left, self.top, self.WIDTH, self.HEIGHT)

    def __str__(self) -> str:
        return f'Rectangle with left = {self.left}, top = {self.top}, width = {self.WIDTH}, height = {self.HEIGHT}'


class Ball:
    """Ball Object for pong game.
       Class Attributes: Radius=13, X= 451, Y=337
       Instance Attributes:
       `color`: rgb color of ball
       `speed`: ball movement speed. (s)low, (m)edium, (f)ast"""

    # Starting positions
    RADIUS = 13
    X = 451
    Y = 337

    def __init__(self, color: tuple = (0, 0, 0), speed: str = 'm') -> None:

        assert isinstance(color, tuple) and len(
            color) == 3, 'color must be a tuple of rgb values'
        assert isinstance(speed, str) and speed.lower() in (
            's', 'm', 'f'), 'speed must be a string of `s`, `m` or `f`'

        self.speed = speed.lower()
        self.color = color
        self.x = self.X
        self.y = self.Y
        self.position = (self.x, self.y)

    def chspeed(self, new_s: str) -> None:
        """CHanges the speed of the Ball object.
           `new_s` should have the same values as earlier."""
        if not new_s:  # Don't change anything if no input is provided
            return

        assert isinstance(new_s, str) and new_s.lower() in ['s', 'm', 'f']
        new_s = new_s.lower()

        if new_s == self.speed:
            return
        else:
            self.speed = new_s

    def calc_speed(self) -> tuple[int]:
        """Assigns speed values of Ball based on speed"""

        if self.speed == 's':
            self.speedval = (3, 3)
        elif self.speed == 'm':
            self.speedval = (4, 3)
        else:
            self.speedval = (8, 6)

    def move(self, value: int) -> None:
        """moves ball in a direction according to these `value` presets:
           1:top left to bottom right,
           2: vertical,
           3: top right to bottom left
           negating the value moves it in the exact opposite direction."""

        assert abs(value) in (
            1, 2, 3), 'Value has to be one of (-3,-2,-1,1,2,3)'

        self.calc_speed()
        match value:
            case 1:
                self.x += self.speedval[0]
                self.y += self.speedval[1]
            case 2:
                self.y += self.speedval[1]
            case 3:
                self.x -= self.speedval[0]
                self.y += self.speedval[1]
            case -1:
                self.x -= self.speedval[0]
                self.y -= self.speedval[1]
            case -2:
                self.y -= self.speedval[1]
            case -3:
                self.x += self.speedval[0]
                self.y -= self.speedval[1]

        self.position = (self.x, self.y)

    def __str__(self) -> str:
        match self.speed:
            case 's':
                str_speed = 'slow'
            case 'm':
                str_speed = 'medium'
            case 'f':
                str_speed = 'fast'
        return f'Ball with a radius:{self.RADIUS} in position:{self.position} with speed:{str_speed}.'

# I was trying to grab the active window and saw this solution on stackoverflow
# https://stackoverflow.com/questions/2090464/python-window-activation
# Ngl, I don't understand it fully


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(self._handle)
