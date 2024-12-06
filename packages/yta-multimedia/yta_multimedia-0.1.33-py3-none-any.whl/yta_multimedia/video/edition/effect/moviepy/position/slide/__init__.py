from yta_multimedia.video.position import Position
from random import randrange


def get_in_and_out_positions_as_list():
    """
    Returns a list of 2 elements containing the out edge from which
    the video will come into the screen, and the opposite edge to get
    out of the screen. This has been created to animate a random slide
    transition effect. The possibilities are horizontal, diagonal and
    vertical linear sliding transitions. The first element in the list
    is the initial position and the second one, the final position. 
    """
    rnd = randrange(0, 8)
    
    if rnd == 0:
        positions = [Position.OUT_RIGHT, Position.OUT_LEFT]
    elif rnd == 1:
        positions = [Position.OUT_TOP, Position.OUT_BOTTOM]
    elif rnd == 2:
        positions = [Position.OUT_BOTTOM, Position.OUT_TOP]
    elif rnd == 3:
        positions = [Position.OUT_TOP_LEFT, Position.OUT_BOTTOM_RIGHT] 
    elif rnd == 4:
        positions = [Position.OUT_TOP_RIGHT, Position.OUT_BOTTOM_LEFT]
    elif rnd == 5:
        positions = [Position.OUT_BOTTOM_LEFT, Position.OUT_TOP_RIGHT]
    elif rnd == 6:
        positions = [Position.OUT_BOTTOM_RIGHT, Position.OUT_TOP_LEFT]
    elif rnd == 7:
        positions = [Position.OUT_LEFT, Position.OUT_RIGHT]

    return positions