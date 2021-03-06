'''Where the colors live'''
#STANDARDS
RED = (0,0,255)
BLUE = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
CYAN = (255,255,0)
YELLOW = (0,255,255)
MAGENTA = (255,0,255)

#HEX STANDARDS:
def to_hex(color):
    '''Returns hex from BGR tuple'''
    (blue, green , red) = (color)
    return '#%02x%02x%02x' % (red, green, blue)

#GOGOPHERS
MAROON = (25,0,122)
GOLD = (51,204,255)

#CUSTOMCOLORS
CORAL = (80,127,255)
LAVENDER = (210,151,193)

#FIVETHIRTYEIGHT
FIVETHIRTYEIGHT_BLUE = (218,162,48)
FIVETHIRTYEIGHT_ORANGE = (48,79,252)
FIVETHIRTYEIGHT_YELLOW = (56,174,229)
FIVETHIRTYEIGHT_GREEN = (79,144,109)
FIVETHIRTYEIGHT_GRAY = (139,139,139)
