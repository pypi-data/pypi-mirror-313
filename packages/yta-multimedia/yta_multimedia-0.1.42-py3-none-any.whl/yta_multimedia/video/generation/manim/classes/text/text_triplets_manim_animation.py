from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.generation.manim.utils.dimensions import fitting_text
from manim import *


class TextTripletsManimAnimation(BaseManimAnimation):
    """
    The provided 'text' is splitted in triplets and appear on the screen. This animation
    lasts 'duration' seconds. Each triplet appear each 'duration' / len(words).
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
        # We need to adjust the array to contain a multiple of 3 number of elements
        leftover_numbers = words[len(words) - len(words) % 3:]
        if len(leftover_numbers) > 0:
            words = words[:len(words) - len(leftover_numbers)]

        words_triplets = []
        subarray = []
        for word in words:
            subarray.append(word)
            if len(subarray) == 3:
                words_triplets.append(subarray)
                subarray = []
        if leftover_numbers:
            words_triplets += [leftover_numbers]
        each_triplet_time = self.parameters['duration'] / len(words_triplets)

        for triplet in words_triplets:
            str = ' '.join(triplet)
            # I don't know how to show one word before the other
            # Helping information:
            # For example say you would like to not render and skip the begin of a video , you put self.next_section(skip_animations=True) in the line after def construct(self): and put self.next_section() before the first line of the animation you want to render.
            # Thank you: https://www.reddit.com/r/manim/comments/tq1ii8/comment/ihzogki/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
            text = fitting_text(str, 1920 / 2)
            # Create 3 similar texts with each word
            self.add(text)
            self.wait(each_triplet_time)
            self.remove(text)


    