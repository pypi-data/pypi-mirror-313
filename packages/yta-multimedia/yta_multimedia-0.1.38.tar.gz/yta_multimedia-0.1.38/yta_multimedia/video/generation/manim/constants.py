"""
TODO: Please, put some structure here and more comments
"""
MANIM_RESOURCES_FOLDER = 'resources/manim/'

# Manim core
MANDATORY_CONFIG_PARAMETER = 1
OPTIONAL_CONFIG_PARAMETER = 0
# I obtained manim dimensions from here: https://docs.manim.community/en/stable/faq/general.html#what-are-the-default-measurements-for-manim-s-scene
SCENE_HEIGHT = 8 # 1080 equivalent
"""
8 (manim dimension). It is the equivalent, for our suposed scene,
to 1080 in pixels.
"""
SCENE_WIDTH = 14 + (2 / 9) # 1920 equivalent
"""
14 + 2/9 (manim dimension). It is the equivalent, for our suposed
scene, to 1920 in pixels.
"""
HALF_SCENE_HEIGHT = SCENE_HEIGHT / 2
"""
8 / 2 = 4 (manim dimension)
"""
HALF_SCENE_WIDTH = SCENE_WIDTH / 2
"""
(14 + 2/9) / 2 = 7 + 1/9 (manim dimension)
"""
LEFT_MARGIN = -HALF_SCENE_WIDTH
UP_MARGIN = HALF_SCENE_HEIGHT
STANDARD_HEIGHT = 1080
"""
This is our standard height (in pixels) as we will create animation
videos of 1920x1080.
"""
STANDARD_WIDTH = 1920
"""
This is our standard width (in pixels) as we will create animation
videos of 1920x1080.
"""

