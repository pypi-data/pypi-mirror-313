from yta_multimedia.video.generation.manim.classes.base_manim_animation import BaseManimAnimation
from yta_multimedia.resources import Resource
from yta_general_utils.text.transformer import remove_accents
from manim import *


class MagazineTextIsWrittenManimAnimation(BaseManimAnimation):
    """
    Makes an animation in which the provided 'text' appears
    with special magazine characters through an animation
    as if they were written. It is only one row of text 
    limited to 30 characters.
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

        if super().parameter_is_mandatory('text', self.required_parameters) and not text:
            raise Exception('Field "text" is mandatory. Aborting manim creation...')
        
        if len(text) > 30:
            raise Exception('Field "text" has a maximum of 30 characters.')
        
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
        """
        This code will generate the manim animation and belongs to the
        Scene manim object.
        """
        DISTANCE_BETWEEN_LETTERS = 0.30

        text = remove_accents(self.parameters['text'])

        elements = []
        # TODO: Make the text fit attending to how long it is
        for char in text:
            elements_len = len(elements)
            new_letter = self.__get(char)

            if elements_len > 0:
                new_letter.move_to(elements[elements_len - 1]).shift(RIGHT * DISTANCE_BETWEEN_LETTERS)

            elements.append(new_letter)

        all_mobjects = Group(*elements)
        all_mobjects.move_to((0, 0, 0)) # We place all elements in the center

        # We need to make the animation fit the 
        self.wait(1 / 60)

        # If we have a 'duration' of 3 seconds that means 180 FPS.
        # We will be using (1 / 60) before and after the loop so
        # we substract it. We will make one animation per each 
        # mobject, so thats how this work dynamically
        EACH_LETTER_WAITING_TIME = self.parameters['duration'] * 60 / len(all_mobjects) - (2 / 60)
        for mobject in all_mobjects:
            self.add(mobject)
            self.wait(EACH_LETTER_WAITING_TIME / 60)

        self.wait(1 / 60)

        # TODO: If this doesn't work we just set our own animation duration and thats all
        # TODO: We need to make the static alternativa in which the text is just added
        # TODO: This is the Animation, what about creating a big Mobject (?)

    # TODO: This below is repeated in the other magazine scene
    def __get(self, letter: str = 'a'):
        if not letter:
            return None
        
        letter = letter[0:1].lower()
        mobject_group = None

        if letter == 'a':
            mobject_group = self.__get_letter(letter, WHITE, 'https://drive.google.com/file/d/1p_NrqZEf3lhQl_lB_PMwgI4FNIbVkSs-/view?usp=sharing', 0.2, 0)
        elif letter == 'b':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1KO0WsYNcocowFeG7Uql_71dn4tlEyUEJ/view?usp=sharing', 0.2, 0)
        elif letter == 'c':
            mobject_group = self.__get_letter(letter, WHITE, 'https://drive.google.com/file/d/1pFC5l3C0JylftXsDajI2hYJwgFgHFHeX/view?usp=sharing', 0.2, 0)
        elif letter == 'd':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1f7MPrRmczO-oaQYG5tdadg0-q7X8Avm9/view?usp=sharing', 0.2, 0)
        elif letter == 'e':
            mobject_group = self.__get_letter(letter, '#325e2e', 'https://drive.google.com/file/d/1JLb2dPK5AdGqk3MdF1KzKwQnisU1fYwf/view?usp=sharing', 0.2, 0)
        elif letter == 'f':
            mobject_group = self.__get_letter(letter, WHITE, 'https://drive.google.com/file/d/1QA2u8ppuZ9nWFlbfyOBDP3sZ0GRRAcRD/view?usp=sharing', 0.2, 0)
        elif letter == 'g':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1-3PlY9N-X83gyYQWX-M-t0R_gUkp8TMp/view?usp=sharing', 0.2, 0)
        elif letter == 'h':
            mobject_group = self.__get_letter(letter, WHITE, 'https://drive.google.com/file/d/1_e5SzuadQUzMia_KhiLa2p9qntxg-kIC/view?usp=sharing', 0.2, 0)
        elif letter == 'i':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1pWGKVyDGyXcLX2Xwg8pxAV0FHSchB9_J/view?usp=sharing', 0.2, 0)
        elif letter == 'j':
            mobject_group = self.__get_letter(letter, WHITE, 'https://drive.google.com/file/d/17fLo90TghQIRsrLvIm7gRIwKjJkcNgun/view?usp=sharing', 0.2, 0)
        elif letter == 'k':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1yoLkzH1o8vZ4RjVCDWza6WCWvZ8y5MxN/view?usp=sharing', 0.2, 0)
        elif letter == 'l':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1cZAncrpB0j8FD64opEzQdyeCtQVJbajU/view?usp=sharing', 0.2, 0)
        elif letter == 'm':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1XQ02p-veaiSWLyx2PozCfK2QhflDCnpu/view?usp=sharing', 0.2, 0)
        elif letter == 'n':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1gp-9ZLAVVPeOO5uitF6zVOJqeK6443R8/view?usp=sharing', 0.2, 0)
        # TODO: Make 'ñ'
        elif letter == 'o':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/13H8nmkH9UiTn7vG57WgpC0v5S_UNATPM/view?usp=sharing', 0.2, 0)
        elif letter == 'p':
            mobject_group = self.__get_letter(letter, WHITE, 'https://drive.google.com/file/d/1YNSFeSAujWWFuwrqU_A-iw_Xk-l2vXvU/view?usp=sharing', 0.2, 0)
        elif letter == 'q':
            mobject_group = self.__get_letter(letter, WHITE, 'https://drive.google.com/file/d/1k4MuXPS9M2H4Z3BCnCf64yXcBwf6QEKO/view?usp=sharing', 0.2, 0)
        elif letter == 'r':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1nM_jNdzGGV60Z8fAjJp-Q43RXCmwsqh0/view?usp=sharing', 0.2, 0)
        elif letter == 's':
            mobject_group = self.__get_letter(letter, WHITE, 'https://drive.google.com/file/d/1bJC8IAMsHOdqeVxdPBhuV3_KYIE0DZSZ/view?usp=sharing', 0.2, 0)
        elif letter == 't':
            mobject_group = self.__get_letter(letter, WHITE, 'https://drive.google.com/file/d/1H4t4iS_yrsAqg7QEdAhxwDOOahBh54dl/view?usp=sharing', 0.2, 0)
        elif letter == 'u':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1M_uMgx9CBkwM0tKTMH_YiyGRiYPIxbXa/view?usp=sharing', 0.2, 0)
        elif letter == 'v':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/12SGuNyNdF03ua2Ro7GIoAf7ETUB0jDWl/view?usp=sharing', 0.2, 0)
        elif letter == 'w':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1aDQ0vhhrnh-BzVgtnTv9HOFSm7cgxycc/view?usp=sharing', 0.2, 0)
        elif letter == 'x':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1wjCkyibwEYz3G19XZiO9viGkNhFRgY0M/view?usp=sharing', 0.2, 0)
        elif letter == 'y':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1aIEu0EP8a-tDHY6aGvAnFGtGyFBn9M7D/view?usp=sharing', 0.2, 0)
        elif letter == 'z':
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1k7EryiaWPX8HRlnB7tJtEL1eI85z7KD_/view?usp=sharing', 0.2, 0)
        # Special ones
        elif letter == '¿': # Background is the same as '?'
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1cGm0r4cdDi4b4ZSS_VxH3yJdyJ5sGB6Q/view?usp=sharing', 0.2, 0)
        elif letter == '?': # Background is the same as '¿'
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1cGm0r4cdDi4b4ZSS_VxH3yJdyJ5sGB6Q/view?usp=sharing', 0.2, 0)
        elif letter == '¡': # Background is the same as '!'
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1J4aL2yf1V_lCjbxzgXE1HyoXoyBRVXwx/view?usp=sharing', 0.2, 0)
        elif letter == '!': # Backgroudn is the same '¡'
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1J4aL2yf1V_lCjbxzgXE1HyoXoyBRVXwx/view?usp=sharing', 0.2, 0)
        # General ones (those who I don't specify manually)
        # elif letter == ' ':
        #     mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1fLol_Fe_AiQ6ZDY8pWW6yBXSFg9PnTb_/view?usp=sharing', 0.2, 0)
        else:   # Any other sign, even the space
            mobject_group = self.__get_letter(letter, BLACK, 'https://drive.google.com/file/d/1fLol_Fe_AiQ6ZDY8pWW6yBXSFg9PnTb_/view?usp=sharing', 0.2, 0)

        return mobject_group

    def __get_letter(self, letter: str = 'a', color: ManimColor = WHITE, google_drive_url: str = None, background_scale: float = 0.2, background_shift: float = 0):
        """
        Generates the default Mobject Group for our own characters
        """
        if not letter:
            return None

        if not google_drive_url:
            return None

        letter = letter[0:1]

        if letter == ' ':
            return Group(Text('a', font_size = 48, color = color).set_opacity(0))
        
        letter_background_filename = letter
        if letter == '¿':
            letter_background_filename = 'open_question_mark'
        elif letter == '?':
            letter_background_filename = 'close_question_mark'
        elif letter == '¡':
            letter_background_filename = 'open_exclamation_mark'
        elif letter == '!':
            letter_background_filename = 'close_exclamation_mark'

        TMP_FILENAME = Resource.get(google_drive_url, 'resources/manim/magazine_letters/' + letter_background_filename + '.svg')
        letter_background = SVGMobject(TMP_FILENAME).scale(0.2).shift(UP * background_shift)
        letter_text = Text(letter, font_size = 32, color = color)
        letter_group = Group(letter_background, letter_text)
        
        return letter_group