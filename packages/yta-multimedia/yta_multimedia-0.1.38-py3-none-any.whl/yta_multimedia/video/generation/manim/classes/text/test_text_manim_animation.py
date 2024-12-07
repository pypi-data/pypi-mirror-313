from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from manim import *


class TestTextManimAnimation(BaseManimAnimation):
    """
    Animation just for testing with texts.
    """
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, text: str, duration: float, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid. The 
        'text' parameter is limited to 30 characters.
        """
        # Check and validate all parameters
        parameters = {}

        # Empty, for testing

        if not output_filename:
            output_filename = 'output.mov'

        # Generate the animation when parameters are valid
        super().generate(parameters, output_filename = output_filename)

        return output_filename
    
    def animate(self):
        """
        This code will generate the manim animation and belongs to the
        Scene manim object.
        """
        text = Text('Texto de prueba')

        # TODO: Move this to a utils: this make it dissapear like an helicopter
        # def x(mob, alpha):
        #     mob.shift(interpolate(0, 1, alpha)).rotate(interpolate(0, 90 * DEGREES, alpha))
        # self.play(
        #     UpdateFromAlphaFunc(text, x)
        # )


        # def x(mob, alpha):
        #     mob.shift(interpolate(0, 1 * UP, alpha)).rotate(interpolate(0, 90 * DEGREES, alpha))
        # self.play(UpdateFromAlphaFunc(text, x), run_time = 2)

        #self.play(text.animate.scale(2).rotate(90 * DEGREES), run_time = 2, rate_func = linear)

        # TODO: This plays the two animaions
        # self.play(
        #     Succession(
        #         ApplyMethod(text.scale, 2),
        #         ApplyMethod(text.scale, 0.5),
        #     ), # this is equivalent to the one below (please check manim code)
        #     text.animate.rotate(90 * DEGREES),
        #     run_time = 2,
        #     rate_func = linear
        # )

        # # TODO: This plays only the last animation
        # # Simple form
        # self.play(
        #     text.animate.scale(2), 
        #     text.animate.rotate(-90 * DEGREES), # Even if they are different
        #     run_time = 1
        # )

        # This plays the two animations at the same time
        # self.play(
        #     text.animate.scale(2).rotate(-90 * DEGREES),
        #     run_time = 1
        # )

        # This saves a single animation (with specific runtime) to be played later
        # anim = text.animate.shift(RIGHT * 2).set_run_time(2)
        # self.play(
        #     anim,
        #     run_time = 1
        # )

        # TODO: This only plays the last animation
        # self.play(
        #     Succession(
        #         text.animate.rotate(90 * DEGREES).set_runtime(1)
        #         text.animate.rotate(90 * DEGREES).set_runtime(2)
        #         text.animate.rotate(90 * DEGREES).set_runtime(1)
        #         text.animate.rotate(90 * DEGREES).set_runtime(2) # This
        #     ),
        #     run_time = 1
        # )

        def play_animations(animations, text):
            """
            Returns all the animations that must be played for each frame
            (with 'run_time = 1 / 60'). If an animation is None, a wait 
            must be played.
            """
            # I Have animations that include the name, the params, the moments
            # and I have to make animations frame by frame to be able to handle
            # Example: rotate 360 from 0 to 1.5s (frames 0 to 90), shift 3 from 0.75
            # to 1.24s (frames 75 to 105)
            animations = [
                {
                    'mobject': text,
                    'name': 'rotate',
                    'params': 360 * DEGREES,
                    'time': [0, 1.5]
                },
                {
                    'mobject': text,
                    'name': 'shift',
                    'params': 3 * LEFT,
                    'time': [0.75, 1.25]
                }
            ]

            animations_to_play = []
            # TODO: Obtain the greates 'time'
            greatest_time = 1.5 # Manually set by now
            FPS = 60
            for frame in range(int(FPS * greatest_time)):
                animation_to_add = None
                for animation in animations:
                    if frame >= (animation['time'][0] * FPS) and frame < (animation['time'][1] * FPS):
                        # TODO: What about non-divisible animations or progressive ones (?)
                        # It is not the same to play a scale 2x once that play consecutive
                        # scalations...
                        params = animation['params']
                        # Param must be according to the number of frames
                        # We substract 1 frame because if you have 3 frames you can only make
                        # 2 animations: the 0-1 and the 1-2, so if you want to rotate
                        # from 0 to 360 in 3 frames, yo cannot do 120-120-120, you only
                        # have 2 animations, so it must be 180-180. Thats the reason of
                        # the - (1 / 60)
                        params = params / ((animation['time'][1] - animation['time'][0] - (1 / 60)) * 60)
                        print(params)
                        if animation_to_add is None:
                            # Dynamically call the animation method
                            # print(animation['mobject'].animate)
                            # func = getattr(animation['mobject'].animate, animation['name'])
                            # print(func)
                            # method_name = "rotate"  # Por ejemplo, 'rotate' o 'shift'
                            # method = getattr(animation['mobject'].animate, method_name)
                            # print(method)
                            #self.play(method(*method_args))
                            animation_to_add = getattr(animation['mobject'].animate, animation['name'])(params)
                        else:
                            animation_to_add = getattr(animation_to_add, animation['name'])(params)
                    
                print(f'frame {str(frame)}')
                if animation_to_add is not None:
                    self.play(animation_to_add, run_time = 1 / 60, rate_func = linear)
                    #animations_to_play.append(animation_to_add)
                else:
                    self.wait(1 / 60)
                    #animations_to_play.append(None)

            #return animations_to_play

        # This is working, slow, but working. Maybe it could be a way of
        # handle a timeline with animations so we just define when and how
        # and they are built with this automatic system.
        #animations_to_play = play_animations('', text)

        kwargs = {
            'color': BLUE,
            'font_size': 22
        }
        self.play(Text('hola', **kwargs).animate.rotate(90 * DEGREES), run_time = 2)

        # This doesn't work as expected
        # self.play(text.animate.rotate(360 * DEGREES * (2 / 4)), run_time = 2)
        # self.play(text.animate.rotate(360 * DEGREES * (1 / 4)).shift(2 * LEFT), run_time = 1)
        # self.play(text.animate.rotate(360 * DEGREES * (1 / 4)), run_time = 1)

        # for animation in animations_to_play:
        #     if animation is None:
        #         self.wait(1 / 60)
        #     else:
        #         print(animation)
        #         self.play(animation, run_time = 1 / 60)

        # TODO: This below is working, but not if stored in array with method
        # for frame in range(int(60 * 0.5)):
        #     x = getattr(text.animate, 'rotate')(45 * DEGREES / (60 * 0.5))
        #     #x = text.animate.rotate(45 * DEGREES / (60 * 0.5))
        #     if frame > 5 and frame < 15:
        #         x = getattr(x, 'shift')(0.5 * LEFT / (60 * 0.5))
        #         #x = x.shift(0.5 * LEFT / (60 * 0.5))

        #     self.play(x, run_time = 1 / 60)
        #     #self.play(text.animate.rotate(45 * DEGREES / (60 * 0.5)).shift(0.5 * LEFT / (60 * 0.5)), run_time = 1 / 60)

        # self.play(text.animate.rotate(45 * DEGREES).shift(0.5 * LEFT), run_time = 1 / 8)
        # self.play(text.animate.rotate(45 * DEGREES).shift(0.5 * LEFT), run_time = 1 / 8)
        # self.play(text.animate.rotate(45 * DEGREES).shift(0.5 * LEFT), run_time = 1 / 8)
        # self.play(text.animate.rotate(45 * DEGREES).shift(0.5 * LEFT), run_time = 1 / 8)
        # self.play(text.animate.rotate(45 * DEGREES).shift(0.5 * LEFT), run_time = 1 / 8)
        # self.play(text.animate.rotate(45 * DEGREES).shift(0.5 * LEFT), run_time = 1 / 8)
        # self.play(text.animate.rotate(45 * DEGREES).shift(0.5 * LEFT), run_time = 1 / 8)
        # self.play(text.animate.rotate(45 * DEGREES).shift(0.5 * LEFT), run_time = 1 / 8)

        # self.play(
        #     Succession(
        #         ApplyMethod(text.rotate, 45 * DEGREES, run_time = 1),
        #         ApplyMethod(text.rotate, 45 * DEGREES, run_time = 1),
        #         ApplyMethod(text.rotate, 45 * DEGREES, run_time = 1),
        #         ApplyMethod(text.rotate, 45 * DEGREES, run_time = 1),
        #         ApplyMethod(text.rotate, 45 * DEGREES, run_time = 1),
        #         ApplyMethod(text.rotate, 45 * DEGREES, run_time = 1),
        #         ApplyMethod(text.rotate, 45 * DEGREES, run_time = 1),
        #         ApplyMethod(text.rotate, 45 * DEGREES, run_time = 1),
        #     ),
        #     run_time = 1
        # )

        # anim1 = text.animate.rotate(90 * DEGREES).set_run_time(2)
        # anim2 = text.animate.scale(2).set_run_time(1)
        # self.play(
        #     AnimationGroup([anim1, anim2]),
        #     run_time = 2
        # )

        # # TODO: This plays two animations consecutively
        # # Simple form
        # self.play(text.animate.scale(0.5), run_time = 0.5)
        # self.play(text.animate.scale(2), run_time = 0.5)

        # # TODO: This plays two animations consecutively
        # # Succession form
        # # TODO: Can I make that the succession, that is supposed
        # # to last 4 seconds, to last only 2 by passing a run_time
        # # to the 'self.play()' because the other run_times are
        # # updated according to the general one (?) That would be
        # # awesome
        # self.play(
        #     Succession(
        #         ApplyMethod(text.scale, 0.5, run_time = 15 / 60),
        #         ApplyMethod(text.scale, 2, run_time = 45 / 60),
        #     ),
        #     run_time = 4
        # )

        # # TODO: This plays two animations at the same one, and
        # # the first one is two animations consecutively
        # self.play(
        #     AnimationGroup(
        #         Succession(
        #             ApplyMethod(text.scale, 0.5, run_time = 2),
        #             ApplyMethod(text.scale, 2, run_time = 2),
        #         ),
        #         ApplyMethod(text.set_color, RED, run_time = 1)
        #         # Succession(
        #         #     #ApplyMethod(text.set_color(BLUE), run_time = 1 / 60),
        #         #     # TODO: How can I make this wait between animations (?)
        #         #     #ApplyMethod(self.wait, 1),
        #         #     #Wait(1), # This blocks the other ones
        #         #     ApplyMethod(text.set_color, RED, run_time = 2) # This blocks the previous succession
        #         # )
        #     )
        # )

        # TODO: I want to be able to do this below
        # What if I want to use animations like:
        # mobj1.animate.X  -> from 0 to 1 do this, then from 1 to 2 wait
        # mobj2.animate.Y  -> from 0 to 1 wait, from 1 to 2 do this

        """self.play(
            AnimationGroup([
                Succession(
                    ApplyMethod(text.scale, 2),
                    ApplyMethod(text.scale, 0.5),
                ),
                text.animate.rotate(90 * DEGREES)
            ],
            run_time = 2),
            rate_func = linear
        )"""

        # die1 = RoundedRectangle(height=1, width=1, corner_radius=0.2).move_to([0, 0, 0])
        # die1.save_state()
        # def update_die1(mob, alpha):
        #     mob.restore()
        #     mob.become(
        #         RoundedRectangle(
        #             height=1,
        #             width=1,
        #             corner_radius=0.2,
        #         ).move_to([interpolate(0, 1.9, alpha), 0, 0]).rotate(interpolate(0, 90*DEGREES, alpha))
        #     )
        # self.play(
        #     UpdateFromAlphaFunc(die1, update_die1)
        # )
        # self.wait()

        # self.play(
        #     AnimationGroup(
        #         [
        #             text.animate.shift(UP),
        #             text.animate.rotate(PI / 8),
        #             text.animate.scale(2)
        #         ]
        #     ), 
        #     run_time = 2
        # )

        # self.wait(1)