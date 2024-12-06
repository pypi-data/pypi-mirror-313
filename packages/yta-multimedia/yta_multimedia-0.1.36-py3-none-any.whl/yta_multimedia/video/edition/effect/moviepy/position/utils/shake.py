from random import randint


# TODO: Apply RateFunctions here to be able to handle
# them not only in a 'linear' way
"""
        In place movements (static) effect position functions below
"""
def shake_movement(t, x, y):
    """
    Returns the (x, y) position tuple for the provided 't' of the moviepy
    '.with_position()' method that belongs to a constant shaking process.
    """
    pos = [x, y]
    speed = t * 4
    d = randint(0, 4)

    if 0 == d: #top
        return (pos[0], pos[1] + speed)
    elif 1 == d: #left
        return (pos[0] - speed, pos[1])
    elif 2 == d: #bot
        return (pos[0], pos[1] - speed)
    else: #right
        return (pos[0] + speed, pos[1])
    
def shake_increasing_movement(t, x, y, duration):
    """
    Returns the (x, y) position tuple for the provided 't' of the moviepy
    '.with_position()' method that belongs to a shaking process that
    increases slowly.
    """
    MAX_SHAKE_SPEED = 20
    pos = [x, y]
    # Speed will increase progressively from 0 to MAX_SHAKE_SPEED
    # and this process will last the whole clip duration
    speed = (t / duration) * MAX_SHAKE_SPEED
    d = randint(0, 4)

    if 0 == d: #top
        return (pos[0], pos[1] + speed)
    elif 1 == d: #left
        return (pos[0] - speed, pos[1])
    elif 2 == d: #bot
        return (pos[0], pos[1] - speed)
    else: #right
        return (pos[0] + speed, pos[1])
    
def shake_decreasing_movement(t, x, y, duration):
    """
    Returns the (x, y) position tuple for the provided 't' of the moviepy
    '.with_position()' method that belongs to a shaking process that
    decreases slowly.
    """
    MAX_SHAKE_SPEED = 20
    pos = [x, y]
    # Speed will increase progressively from 0 to MAX_SHAKE_SPEED
    # and this process will last the whole clip duration
    speed = MAX_SHAKE_SPEED - ((t / duration) * MAX_SHAKE_SPEED)
    d = randint(0, 4)

    if 0 == d: #top
        return (pos[0], pos[1] + speed)
    elif 1 == d: #left
        return (pos[0] - speed, pos[1])
    elif 2 == d: #bot
        return (pos[0], pos[1] - speed)
    else: #right
        return (pos[0] + speed, pos[1])
    