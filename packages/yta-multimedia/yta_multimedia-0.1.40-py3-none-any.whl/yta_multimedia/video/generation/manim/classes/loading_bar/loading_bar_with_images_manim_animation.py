from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.generation.manim.classes.loading_bar.parameter_classes.loading_bar_image import LoadingBarImage
from yta_multimedia.video.generation.manim.classes.loading_bar.mobjects.loading_bar_mobject import LoadingBarMobject
from yta_multimedia.video.generation.manim.utils.dimensions import manim_height_to_height
from manim import linear


class LoadingBarWithImagesManimAnimation(BaseManimAnimation):
    """
    Loading bar with images. It will go from 'start_percentage'
    to 'end_percentage' in the provided 'duration' time. It will
    show the bar progressing and also the 'images' if provided.

    Images will be displayed and will be static or in movement.
    If image 'start_percentage' and 'end_percentage' is the same,
    it will be static at that percentage position. If they are
    different, it will move from 'start_percentage' to
    'end_percentage' in the animation 'duration' time.

    You can put the same 'start_percentage' and 'end_percentage'
    in one image than in the loading bar to make it advance
    at the same time the progress bar does.

    Here is an example of 'images' object you can pass:
    loading_bar_images = [
        LoadingBarImage('minecraft_sword_128x128.png', 60, 0, 100),
        LoadingBarImage('arrow_up_128x128.png', -60, 0, 100),
        LoadingBarImage('minecraft_sword_128x128.png', 60, 40, 40),
        LoadingBarImage('minecraft_sword_128x128.png', 60, 78, 78)
    ]
    """
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, start_percentage: int = 0, end_percentage: int = 100, duration: float = 5, images: list[LoadingBarImage] = None, output_filename: str = None):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid.
        """
        # Check and validate all parameters
        parameters = {}

        # TODO: By now I will avoid using 'required_parameters' and use the
        # logic by itself just here:
        # start_percentage is mandatory
        # end_percentage is mandatory
        # duration is mandatory
        # images is optional

        # Mandatory parameters
        if start_percentage == None or start_percentage < 0:
            raise Exception('"start_percentage" parameter must be a valid int between [0, 100]')
        
        if end_percentage == None or end_percentage < 0:
            raise Exception('"end_percentage" parameter must be a valid int between [0, 100]')
        
        if duration == None or duration <= 0 or duration > 120:
            raise Exception('"duration" parameter must be a valid float between (0, 120]')
        
        parameters['start_percentage'] = start_percentage
        parameters['end_percentage'] = end_percentage
        parameters['duration'] = duration

        # Optional parameters
        parameters['images'] = []
        if images and len(images) > 0:
            # We need to pass the information as JSON to be written
            # TODO: Check 'images' parameter is valid
            for image in images:
                parameters['images'].append(image.toJSON())

        if not output_filename:
            output_filename = 'output.mov'

        # Generate the animation when parameters are valid
        super().generate(parameters, output_filename = output_filename)

        return output_filename

    def animate(self):
        loading_bar = LoadingBarMobject()
        
        # We make LoadingBarImages objects again
        images = []
        for image in self.parameters['images']:
            images.append(LoadingBarImage(image['image_filename'], manim_height_to_height(image['y']), image['start_percentage'], image['end_percentage']))

        loading_bar_animation = loading_bar.get_animation(images, self.parameters['start_percentage'], self.parameters['end_percentage'], self.parameters['duration'])

        # We add the mobjects to forze them to appear
        self.add(*loading_bar.get_mobjects())

        self.play(*loading_bar_animation, rate_func = linear, run_time = self.parameters['duration'])