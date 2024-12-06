
from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.generation.manim.utils.dimensions import fitting_text
from yta_multimedia.video.position import Position
from manim import *


class RainOfWordsManimAnimation(BaseManimAnimation):
    """
    This is a rain of the provided 'words' over the screen, that
    appear in random positions.
    """
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, words: list[str], duration: float, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid.
        """
        # Check and validate all parameters
        parameters = {}

        if super().parameter_is_mandatory('words', self.required_parameters) and not words or len(words) <= 0:
            raise Exception('Field "text" is mandatory. Aborting manim creation...')
        
        parameters['words'] = words

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
        each_word_time = self.parameters['duration'] / len(self.parameters['words'])
        # Adjust the divisor number to modify word size
        for word in self.parameters['words']:
            text = fitting_text(word, 1920 / 6)
            random_coords = Position.RANDOM_INSIDE.get_manim_position((text.width, text.height))
            text.move_to([random_coords['x'], random_coords['y'], 0])
            self.add(text)
            self.wait(each_word_time)
        