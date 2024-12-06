from yta_multimedia.video.generation.manim.constants import MANDATORY_CONFIG_PARAMETER
from yta_multimedia.video.generation.manim.utils.config import ManimConfig
from yta_general_utils.file.filename import get_file_extension, get_file_filename_without_extension
from yta_general_utils.file.handler import FileHandler
from yta_general_utils.programming.path import get_code_abspath, get_project_abspath, get_code_filename
from manim.cli.render.commands import render as manim_render
from manim import config, ThreeDScene
from threading import Thread


# TODO: This is exactly as BaseManimAnimation but using 'ThreeDScene'
# so please, review if we can make the behaviour common or what
class BaseThreeDManimAnimation(ThreeDScene):
    """
    General class so that our own classes can inherit it 
    and work correctly.
    """
    required_parameters = {}
    parameters = {}

    def parameter_is_mandatory(self, parameter, required_parameters):
        """
        Returns true if the provided 'parameter' is mandatory, based on
        'required_parameters' definition.
        """
        if parameter in required_parameters and required_parameters[parameter] == MANDATORY_CONFIG_PARAMETER:
            return True
        
        return False

    def __set_mandatory_config(self):
        """
        This method set some configuration parameters we need to build perfect
        animation videos.
        """
        # Disables caching to avoid error when cache is overload
        config.disable_caching = True
        config.max_files_cached = 9999
        # This makes the video background transparent to fit well over the main video
        self.camera.background_opacity = 0.0
    
    def setup(self):
        """
        This method is called when manim is trying to use it to
        render the scene animation. It is called the first, to
        instantiate it and before the 'construct' method that
        is the one that will render.
        """
        self.__set_mandatory_config()
        self.parameters = ManimConfig.read()

        return self.parameters
    
    def construct(self):
        """
        This method is called by manim when executed by shell and
        will call the scene animation render method to be processed
        and generated.
        """
        self.setup()

    def animate(self):
        pass

    def generate(self, parameters, renderer = 'cairo', output_filename: str = 'base_three_d_manim_animation.mov'):
        """
        Generates the animation video file using the provided
        'parameters' and stores it locally as 'output_filename'
        """
        if not output_filename:
            raise Exception('No "output_filename" provided.')

        # We write parameters in file to be able to read them
        ManimConfig.write(parameters)

        # Variables we need to make it work
        FPS = str(60)
        CLASS_MANIM_CONTAINER_ABSPATH = get_code_abspath(self.__class__)
        CLASS_FILENAME_WITHOUT_EXTENSION = get_file_filename_without_extension(get_code_filename(self.__class__))
        CLASS_NAME = self.__class__.__name__
        
        output_filename_extension = get_file_extension(output_filename)

        if not renderer or renderer not in ['cairo', 'opengl']:
            renderer = 'cairo'

        # These args are in 'manim.cli.render.commands.py' injected
        # as '@output_options', '@render_options', etc.
        args = {
            # I never used this 'format' before
            '--format': True,
            output_filename_extension.replace('.', ''): True, # Valid values are: [png|gif|mp4|webm|mov]
            # Qualities are here: manim\constants.py > QUALITIES
            '--quality': True,
            'h': True,
            '--fps': True,
            FPS: True,
            '--transparent': True,
            '--renderer': True,
            # The 'cairo' default option has been working good always
            renderer: True, # 'opengl' or 'cairo', 'cairo' is default
            # The '--output_file' changes the created file name, not the path
            CLASS_MANIM_CONTAINER_ABSPATH: True,
            CLASS_NAME: True
        }

        # TODO: Do more Exception checkings (such as '.smtg')
        if output_filename_extension != '.mov':
            del args['--transparent']

        # We need to execute this as a thread because the program ends when
        # finished if not a thread
        render_thread = Thread(target = manim_render, args = [args])
        render_thread.start()
        render_thread.join()
            
        CREATED_FILE_ABSPATH = get_project_abspath() + 'media/videos/' + CLASS_FILENAME_WITHOUT_EXTENSION + '/1080p' + FPS + '/' + CLASS_NAME + output_filename_extension

        FileHandler.rename_file(CREATED_FILE_ABSPATH, output_filename)

        return output_filename