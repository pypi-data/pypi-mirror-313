from yta_multimedia.video.generation.manim.classes.base_three_d_manim_animation import BaseThreeDManimAnimation
from manim import *


class Axes3DExample(BaseThreeDManimAnimation):
    def construct(self):
        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)

        # 3D variant of the Dot() object
        dot = Dot3D()

        # zoom out so we see the axes
        self.set_camera_orientation(zoom=0.5)

        self.play(FadeIn(axes), FadeIn(dot), FadeIn(x_label), FadeIn(y_label))

        self.wait(0.5)

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)

        # one dot for each direction
        upDot = dot.copy().set_color(RED)
        rightDot = dot.copy().set_color(BLUE)
        outDot = dot.copy().set_color(GREEN)

        self.wait(1)

        self.play(
            upDot.animate.shift(UP),
            rightDot.animate.shift(RIGHT),
            outDot.animate.shift(OUT),
        )

        self.wait(2)

class Image3D(BaseThreeDManimAnimation):
    def construct(self):
        self.video1 = ImageMobject(
                filename_or_array = 'C:/Users/dania/Desktop/wallpaper1080.png',
            ).scale_to_fit_height(3)
        ax = Axes(
            x_range=[0, 10, 1],
            x_length=9,
            y_range=[0, 20, 5],
            y_length=6,
            axis_config={"include_numbers": True, "include_tip": False},

        ).to_edge(DL + RIGHT + UP, buff=1).scale(0.7)
        labels = ax.get_axis_labels()

        self.play(Create(VGroup(ax, labels)))
        self.play(FadeIn(self.video1))
        self.wait(3)
        self.move_camera(phi=0*DEGREES, theta= -90 * DEGREES, zoom= 0.7, run_time=0.4, gamma=0*DEGREES)

        self.begin_ambient_camera_rotation(90 * DEGREES / 3, about='phi')
        self.begin_ambient_camera_rotation(90 * DEGREES / 3, about='theta')
        self.wait(3)