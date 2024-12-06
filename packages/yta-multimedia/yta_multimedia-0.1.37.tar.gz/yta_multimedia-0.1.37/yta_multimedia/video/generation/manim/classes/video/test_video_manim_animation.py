"""
Some tests I made with Manim (3D, as it is the most difficult):
- ImageMobject + Cairo works, but positioning gets crazy.
- ImageMobject + Opengl fails
- OpenGLImageMobject + Opengl works perfectly.
- VideoMobject (ImageMobject) + Cairo works, but positioning gets crazy.
- VideoMobject (ImageMobject) + Opengl fails
- VideoMobject (OpenGLImageMobject) + Opengl only shows the first frame, but positioning is perfect.
- Didn't test anything else
"""
from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.video.generation.manim.classes.base_three_d_manim_animation import BaseThreeDManimAnimation
from yta_multimedia.video.generation.manim.classes.video.mobjects.video_mobject import VideoMobject
from yta_multimedia.video.generation.manim.classes.video.mobjects.video_opengl_mobject import VideoOpenGLMobject
from yta_multimedia.video.generation.manim.classes.image.opengl_image_mobject import OpenGLImageMobject
from manim import *


class TestVideoMobjectIn2DManimAnimation(BaseManimAnimation):
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid. The 
        'text' parameter is limited to 30 characters.
        """
        # Check and validate all parameters
        parameters = {}

        # Generate the animation when parameters are valid
        super().generate(parameters, renderer = 'cairo', output_filename = output_filename)

        return output_filename
    
    def animate(self):
        video1 = VideoMobject(
            filename = 'prueba.mp4',
        ).scale_to_fit_width(5)
        self.add(video1)
        self.wait(0.25)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.wait(0.25)

class TestVideoOpenGLMobjectIn2DManimAnimation(BaseManimAnimation):
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid. The 
        'text' parameter is limited to 30 characters.
        """
        # Check and validate all parameters
        parameters = {}

        # Generate the animation when parameters are valid
        super().generate(parameters, renderer = 'opengl', output_filename = output_filename)

        return output_filename
    
    def animate(self):
        video1 = VideoOpenGLMobject(
            filename = 'prueba.mp4',
        ).scale_to_fit_width(5)
        self.add(video1)
        self.wait(0.25)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.wait(0.25)

class TestVideoMobjectIn3DManimAnimation(BaseThreeDManimAnimation):
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid. The 
        'text' parameter is limited to 30 characters.
        """
        # Check and validate all parameters
        parameters = {}

        # Generate the animation when parameters are valid
        super().generate(parameters, renderer = 'cairo', output_filename = output_filename)

        return output_filename
    
    def animate(self):
        video1 = VideoMobject(
            filename = 'prueba.mp4',
        ).scale_to_fit_width(5)
        self.add(video1)
        self.wait(0.25)
        self.begin_ambient_camera_rotation(rate = 0.15)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        self.wait(0.25)

class TestVideoOpenGLMobjectIn3DManimAnimation(BaseThreeDManimAnimation):
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid. The 
        'text' parameter is limited to 30 characters.
        """
        # Check and validate all parameters
        parameters = {}

        # Generate the animation when parameters are valid
        super().generate(parameters, renderer = 'opengl', output_filename = output_filename)

        return output_filename
    
    def animate(self):
        video1 = VideoOpenGLMobject(
            filename = 'prueba.mp4',
        ).scale_to_fit_width(5)
        self.add(video1)
        self.wait(0.25)
        self.begin_ambient_camera_rotation(rate = 0.15)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.play(video1.animate.shift(2 * DOWN), run_time = 0.5)
        self.play(video1.animate.shift(1 * UP), run_time = 0.25)
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, zoom=1, run_time=1.5)
        self.wait(0.25)

class TestImageOpenGLMobjectIn3DManimAnimation(BaseThreeDManimAnimation):
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, filename: str, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid. The 
        'text' parameter is limited to 30 characters.
        """
        # Check and validate all parameters
        parameters = {
            'filename': filename
        }

        # Generate the animation when parameters are valid
        super().generate(parameters, renderer = 'opengl', output_filename = output_filename)

        return output_filename
    
    def animate(self):
        image = OpenGLImageMobject.init(self.parameters['filename']).scale_to_fit_width(5)
        self.add(image)
        image.shift(10 * UP)
        self.play(image.animate.shift(10 * DOWN), run_time = 0.25)
        self.move_camera(phi = 30 * DEGREES, frame_center = image, run_time = 0.25)
        self.move_camera(phi = -60 * DEGREES, frame_center = image, run_time = 0.50)
        self.move_camera(phi = 30 * DEGREES, frame_center = image, run_time = 0.25)
        self.wait(0.25)

class TestOpenGLImageMobjectIn3DManimAnimation(BaseThreeDManimAnimation):
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.animate()

    def generate(self, output_filename: str = 'output.mov'):
        """
        Checks and validates the provided parameters and generates
        the manim animation if those parameters are valid. The 
        'text' parameter is limited to 30 characters.
        """
        # Check and validate all parameters
        parameters = {}

        # Generate the animation when parameters are valid
        super().generate(parameters, renderer = 'opengl', output_filename = output_filename)

        return output_filename
    
    def animate(self):
        from yta_multimedia.image.generation.reviews.tripadvisor.tripadvisor_image_generator import TripadvisorImageGenerator
        from yta_multimedia.video.generation.manim.constants import SCENE_HEIGHT

        # This makes an image navigating in 3D scenario and being rendered
        # with alpha transparency (if it nos working, go to 'opengl_renderer.py'
        # and change the line 596 replacing 1.0 by 0.0)
        self.camera.background_color = [0, 0, 0, 0]
        image = OpenGLImageMobject.init(
            filename_or_array = np.asarray(TripadvisorImageGenerator.generate_review()),
        ).scale_to_fit_width(5)
        image.move_to((0, SCENE_HEIGHT + image.height / 2, 0))
        self.add(image)
        #self.move_camera(phi = 75 * DEGREES, theta = 30 * DEGREES, run_time = 0.0000001)
        self.set_camera_orientation(phi = 75 * DEGREES, theta = 30 * DEGREES)
        self.play(image.animate.move_to((0, -SCENE_HEIGHT - image.height / 2, 0)), run_time = 5, rate_func = linear)
        print('Animation finished')
        print(self.camera.background_opacity)

    def animate_two(self):
        from yta_multimedia.video.frames.video_frame_extractor import VideoFrameExtractor
        from yta_multimedia.video.generation.manim.constants import SCENE_WIDTH, HALF_SCENE_HEIGHT
        from moviepy import VideoFileClip

        # This below is for trying to render a video but the internal
        # counter is not working properly
        image = OpenGLImageMobject.init(
            filename_or_array = VideoFrameExtractor.get_frame_by_number('prueba.mp4', 0)
        ).scale_to_fit_width(SCENE_WIDTH)
        self.add(image)
        #self.begin_ambient_camera_rotation()
        self.wait(0.25)
        self.wait(0.25)
        self.move_camera(phi = 45 * DEGREES, added_anims = [image.animate.move_to((0, HALF_SCENE_HEIGHT, -HALF_SCENE_HEIGHT))], run_time = 1, rate_func = linear)
        videoclip = VideoFileClip('prueba.mp4')
        #previous_image = image
        print(videoclip.fps * videoclip.duration)
        print((int) (videoclip.fps * videoclip.duration))
        videoclip = videoclip.with_subclip(0, 1)
        for i in range((int) (videoclip.fps * videoclip.duration)):
            if i == 0:
                i += 1
                print(self.mobjects)
                other_image = OpenGLImageMobject.init(
                    filename_or_array = VideoFrameExtractor.get_frame_by_number('prueba.mp4', i),
                ).scale_to_fit_width(SCENE_WIDTH).move_to(self.mobjects[0])
                print(self.mobjects[0].__class__)
                print(self.mobjects[1].__class__)
                print(self.mobjects)
                self.add(other_image)
                print(self.mobjects)
                self.play(Transform(self.mobjects[0], self.mobjects[len(self.mobjects) - 1]), run_time = 1 / 60)
                print(self.mobjects)
                self.remove(self.mobjects[0])
                image = other_image
                #self.add(other_image)
                #previous_image = other_image
                #self.wait(1 / 60)
                print(self.mobjects)
            else:
                print(self.mobjects)
                other_image = OpenGLImageMobject.init(
                    filename_or_array = VideoFrameExtractor.get_frame_by_number('prueba.mp4', i),
                ).scale_to_fit_width(SCENE_WIDTH).move_to(self.mobjects[len(self.mobjects) - 1])
                print(self.mobjects[0].__class__)
                print(self.mobjects[1].__class__)
                print(self.mobjects)
                self.add(other_image)
                print(self.mobjects)
                self.play(Transform(self.mobjects[len(self.mobjects) - 2], self.mobjects[len(self.mobjects) - 1]), run_time = 1 / 60)
                print(self.mobjects)
                self.remove(self.mobjects[len(self.mobjects) - 2])
                image = other_image
                #self.add(other_image)
                #previous_image = other_image
                #self.wait(1 / 60)
                print(self.mobjects)
        #self.play(Uncreate(image), run_time = 0.5, rate_func = linear)
        #image.animate.move_to((0, 0, HALF_SCENE_HEIGHT))
        self.wait(0.25)
        #self.stop_ambient_camera_rotation()