from yta_multimedia.video.generation.manim.utils.dimensions import ManimDimensions
from yta_multimedia.video.generation.manim.classes.loading_bar.parameter_classes.loading_bar_image import LoadingBarImage
from manim import *
from PIL import Image


class LoadingBarMobject(Mobject):
    def __init__(self, x: int = 0, y: int = -400, width: int = 1400, height: int = 30, unreached_color: ManimColor = GREEN_B, reached_color: ManimColor = GREEN_A):
        """
        The 'x', 'y' and 'width' parameters must be in pixels. Remember that
        we use the scene as a 1920x1080 pixels screen.
        """
        if x == None or x < -960 or x > 960:
            raise Exception('"x" must be an "int" number between [-960, 960]')
        
        if y == None or y < -540 or y > 540:
            raise Exception('"y" must be an "int" number between [-540, 540]')

        if width == None or width <= 0 or width > 1920:
            raise Exception('"width" must be an "int" number between [0, 1920]')
        
        if height == None or height <= 0 or height > 1080:
            raise Exception('"width" must be an "int" number between [0, 1080]')
        
        # TODO: Check colors and raise Exception

        # We transform pixels to manim values and set parameters
        self.initial_x = ManimDimensions.width_to_manim_width(x)
        self.initial_y = ManimDimensions.height_to_manim_height(y)
        self.initial_width = ManimDimensions.width_to_manim_width(width)
        self.initial_height = ManimDimensions.height_to_manim_height(height)
        self.unreached_color = unreached_color
        self.reached_color = reached_color
        self.loading_bar_unreached = None
        self.loading_bar_reached = None
        # mobjects
        self.loading_bar_unreached = None
        self.loading_bar_reached = None
        self.image_mobjects = []

        # Generate the basic loading bar elements (two rectangles)
        self.__reset_bar()

    def __reset_bar(self):
        """
        Moves the bar to the start position. This instantiates the objects
        and moves them to the start position (0%).
        """
        if not self.loading_bar_unreached:
            self.loading_bar_unreached = Rectangle(width = self.initial_width, height = self.initial_height)
            self.loading_bar_unreached.set_fill(self.unreached_color, opacity = 1).set_stroke(self.unreached_color, width = 0).move_to((self.initial_x, self.initial_y, 0))
            
        if not self.loading_bar_reached:
            self.loading_bar_reached = Rectangle(width = ManimDimensions.width_to_manim_width(1), height = self.initial_height)
            self.loading_bar_reached.set_fill(self.reached_color, opacity = 1).set_stroke(self.reached_color, width = 0).move_to((self.loading_bar_unreached.get_x() - (self.loading_bar_unreached.width / 2 + self.loading_bar_reached.width / 2), self.loading_bar_unreached.get_y(), 0))
        else:
            self.loading_bar_reached.stretch_to_fit_width(ManimDimensions.width_to_manim_width(1)).move_to((self.loading_bar_unreached.get_x() - (self.loading_bar_unreached.width / 2 + self.loading_bar_reached.width / 2), self.loading_bar_unreached.get_y(), 0))

    def __calculate_from_percentage_to_percentage(self, start_percentage: int, end_percentage: int):
        """
            Calculates the start width, the end width and the difference between
            both. It will return an object containing 'width_at_start',
            'width_at_end' y 'width_difference'.

            It also returns 'x_at_start' and 'x_at_end' that are the x positions
            for those percentages. These are useful for images.
        """
        width_at_start = start_percentage * 0.01 * self.initial_width
        x_at_start = -self.initial_width / 2 + width_at_start
        width_at_end = end_percentage * 0.01 * self.initial_width
        x_at_end = -self.initial_width / 2 + width_at_end
        width_difference = width_at_end - width_at_start

        if width_at_start == 0:
            # We need to use at least 1 pixel of size
            width_at_start = ManimDimensions.width_to_manim_width(1)

        return {
            'width_at_start': width_at_start,
            'x_at_start': x_at_start,       
            'width_at_end': width_at_end,
            'x_at_end': x_at_end,
            'width_difference': width_difference
        }

    def __move_bar_to_percentage(self, percentage: int):
        # We reset bar to set to the starting position
        self.__reset_bar()

        if percentage == 0:
            return

        calculations = self.__calculate_from_percentage_to_percentage(0, percentage)

        # Move the bar to the new start position according to percentages
        self.loading_bar_reached.stretch_to_fit_width(calculations['width_at_end']).shift(RIGHT * (calculations['width_difference'] / 2))

    def get_mobjects(self):
        """
        Returns all the existing mobjects in this mobject to be able to add
        them to the scene.
        """
        mobjects = [
            self.loading_bar_unreached,
            self.loading_bar_reached
        ]

        if self.image_mobjects and len(self.image_mobjects) > 0:
            mobjects += self.image_mobjects

        return mobjects

    def get_animation(self, images: list[LoadingBarImage] = [], start_percentage: int = 0, end_percentage: int = 100, duration: float = 5):
        """
        Returns the animation to be played in the scene with the 'self.play'
        method. This allows us to execute it outside and to mix this animation
        with others. It is important to provide the exact duration to be able
        to build the correct animation.
        """
        if start_percentage == None or start_percentage < 0 or start_percentage > 100:
            raise Exception('"start_percentage" parameter must be a valid int between [0, 100]')
        
        if end_percentage == None or end_percentage < 0 or end_percentage > 100:
            raise Exception('"start_percentage" parameter must be a valid int between [0, 100]')
        
        if duration == None or duration <= 0 or duration > 120:
            raise Exception('"duration" parameter must be a valid float between (0, 120]')
        
        # TODO: Check if 'images' is provided and valid
        if images == None:
            images = []
        
        # We move the bar to the start percentage position
        self.__move_bar_to_percentage(start_percentage)
        
        # Calculate from start to end
        calculations = self.__calculate_from_percentage_to_percentage(start_percentage, end_percentage)

        self.image_mobjects = []

        animations_group = []
        for image in images:
            # TODO: This is not good, please, handle this in a better way
            image_data = Image.open(image.image_filename).resize((64, 64))

            image_calculations = self.__calculate_from_percentage_to_percentage(image.start_percentage, image.end_percentage)

            image_mobject = ImageMobject(np.array(image_data)).set_z_index(0).move_to((image_calculations['x_at_start'], self.loading_bar_reached.get_y() + image.y, 0))
            self.image_mobjects.append(image_mobject)

            if image.start_percentage != image.end_percentage:
                # We make the animation to move the image to destination
                animations_group.append(image_mobject.animate.shift(RIGHT * (image_calculations['x_at_end'] - image_mobject.get_x())))
            else:
                # We just move static images to their positions without animation
                image_mobject.move_to((image_mobject.get_x(), image_mobject.get_y(), 0))

        # We make the main animation, the bar moving
        animations_group.append(self.loading_bar_reached.animate.stretch_to_fit_width(calculations['width_at_end']).shift(RIGHT * (calculations['width_difference'] / 2)))

        return animations_group