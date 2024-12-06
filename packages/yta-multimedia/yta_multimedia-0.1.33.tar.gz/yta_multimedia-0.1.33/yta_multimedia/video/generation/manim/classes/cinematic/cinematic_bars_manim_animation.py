from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.generation.manim.constants import SCENE_HEIGHT, SCENE_WIDTH, HALF_SCENE_HEIGHT
from manim import *


class CinematicBarsManimAnimation(BaseManimAnimation):
    """
    Black bars that appear to make the scene cinematic.
    """
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, duration: float = 2, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid.
        """
        # Check and validate all parameters
        parameters = {}

        if super().parameter_is_mandatory('duration', self.required_parameters) and not duration:
            raise Exception('Field "duration" is mandatory. Aborting manim creation...')
        if duration < 0 or duration > 100:
            raise Exception('Field "duration" value is not valid. Must be between 0 and 100')
        
        parameters['duration'] = duration

        if not output_filename:
            output_filename = 'output.mov'

        # Generate the animation when parameters are valid
        super().generate(parameters, output_filename = output_filename)

        return output_filename

    def animate(self):
        top_bar = Rectangle(BLACK, stroke_width = 0, fill_color = BLACK, fill_opacity = 1, height = SCENE_HEIGHT * 0.15, width = SCENE_WIDTH)
        bottom_bar = top_bar.copy()

        START_TOP_POSITION = (0, HALF_SCENE_HEIGHT + (top_bar.height / 2), 0)
        STAY_TOP_POSITION = (0, HALF_SCENE_HEIGHT, 0)
        START_BOTTOM_POSITION = (0, -HALF_SCENE_HEIGHT - (bottom_bar.height / 2), 0)
        STAY_BOTTOM_POSITION = (0, -HALF_SCENE_HEIGHT, 0)

        top_bar.move_to(START_TOP_POSITION)
        bottom_bar.move_to(START_BOTTOM_POSITION)

        self.add(top_bar)
        self.add(bottom_bar)

        # Appearing and dissapearing animation can be 2 seconds
        # longer as maximum (each one). If this happens, the 
        # stay will be longer
        animation_duration = 0.2 * self.parameters['duration']
        stay_duration = 0.6 * self.parameters['duration']
        if animation_duration > 2:
            stay_duration += (animation_duration - 2) * 2

        self.play(AnimationGroup([
            top_bar.animate.move_to(STAY_TOP_POSITION),
            bottom_bar.animate.move_to(STAY_BOTTOM_POSITION)
        ]), run_time = animation_duration, rate_func = linear)

        self.wait(stay_duration)

        self.play(AnimationGroup([
            top_bar.animate.move_to(START_TOP_POSITION),
            bottom_bar.animate.move_to(START_BOTTOM_POSITION)
        ]), run_time = animation_duration, rate_func = linear)