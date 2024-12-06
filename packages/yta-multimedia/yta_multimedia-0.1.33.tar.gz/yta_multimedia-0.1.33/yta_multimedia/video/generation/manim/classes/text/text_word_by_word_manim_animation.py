from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.generation.manim.utils.dimensions import fitting_text, manim_width_to_width
from yta_multimedia.video.generation.manim.constants import SCENE_WIDTH
from manim import *


class TextWordByWordManimAnimation(BaseManimAnimation):
    """
    The provided 'text' is shown word by word in the center of the scene
    with a fixed width.
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
        the manim animation if those parameters are valid.
        """
        # Check and validate all parameters
        parameters = {}

        if super().parameter_is_mandatory('text', self.required_parameters) and not text:
            raise Exception('Field "text" is mandatory. Aborting manim creation...')
        
        parameters['text'] = text

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
        words = self.parameters['text'].split(' ')
        word_duration = float(self.parameters['duration']) / len(words)
        for word in words:
            text = fitting_text(word, manim_width_to_width(SCENE_WIDTH / 6))
            text = Text(word, font_size = text.font_size, stroke_width = 2.0, font = 'Arial').shift(DOWN * 0)
            self.add(text)
            self.wait(word_duration)
            self.remove(text)

    