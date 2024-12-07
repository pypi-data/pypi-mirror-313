from manim import *


def base_text(text: str):
    # TODO: Build a preset
    return Text(text)

    self.play(AnimationGroup(
        square.animate.shift(RIGHT),  # Mover a la derecha
        square.animate.rotate(PI / 4)  # Rotar
    ))