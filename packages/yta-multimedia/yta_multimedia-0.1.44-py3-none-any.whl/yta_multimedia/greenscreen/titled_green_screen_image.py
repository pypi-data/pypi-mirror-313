# TODO: Remove this when new greenscreen system has been
# completely implemented and this file doesn't make sense
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.color.converter import ColorConverter
from PIL import Image, ImageDraw, ImageFont
from random import choice as random_choice
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip
from moviepy.video.fx import MaskColor

import os


# TODO: This has to be refactored to be dynamically built
# and to obtain the files from Google Drive, that must be
# also registered in somewhere to include details like the
# size, the number of green screens and their positions, 
# etc.
#
# We will need to refactor it again to handle different
# texts (not only one) and more elements that could be
# applied while whe develop the app an this greenscreen
# functionality.
class TitledGreenScreenImage:
    """
    Green screen of custom size that is placed over a background image of 1920x1080. It
    can include a text that is placed in the bottom side of the green screen.
    """
    __TOUSE_ABSOLUTE_PATH = os.getenv('TOUSE_ABSOLUTE_PATH')
    __GREEN_SCREENS_FOLDER = __TOUSE_ABSOLUTE_PATH + 'green_screens/'
    # TODO: This is no more a local folder, they are files that we must
    # download from Google Drive
    __BACKGROUNDS_1920x1080_FOLDER = __GREEN_SCREENS_FOLDER + 'backgrounds/1920x1080/'
    __GREEN_SCREEN_RGB_COLOR = (0, 249, 12)
    # TODO: Move this to .env
    __FONTS_PATH = 'C:/USERS/DANIA/APPDATA/LOCAL/MICROSOFT/WINDOWS/FONTS/'

    def __init__(self, title, width = 1344, height = 756):
        if width <= 0 or width > 1920 or height <= 0 or height > 1080:
            # TODO: Handle this exception
            print('Green screen size error, setting to default (1344x756).')
            width = 1344
            height = 756

        # TODO: We must now download the file and use it
        self.background_filename = self.__BACKGROUNDS_1920x1080_FOLDER + random_choice(os.listdir(self.__BACKGROUNDS_1920x1080_FOLDER))
        self.title = title
        self.width = width
        self.height = height

        self.x = int((Image.open(self.background_filename).width - self.width) / 2)
        self.y = int((Image.open(self.background_filename).height - self.height) / 2)

    def save(self, output_filename):
        # We use a random 1920x1080 background image
        # We insert the green_screen in the base_image
        base = Image.open(self.background_filename)
        green_screen = Image.open(self.__generate_green_screen())

        # Dynamically get x,y start to put the green screen in the base image center
        base.paste(green_screen, (self.x, self.y))

        PADDING = 15

        if self.title:
            draw = ImageDraw.Draw(base)   
            font = ImageFont.truetype(self.__FONTS_PATH + 'ROBOTO-MEDIUM.TTF', 60, encoding = 'unic')
            w, h = draw.textsize(self.title, font = font)
            position = ((1920 / 2) - (w / 2), 1080 - ((1080 - self.height) / 2) - (h / 2 + PADDING))
            left, top, right, bottom = draw.textbbox(position, self.title, font = font)
            draw.rectangle((left - PADDING * 2, top - PADDING, right + PADDING * 2, bottom + PADDING), fill = 'black')
            draw.text(position, self.title, font = font, fill = 'white')
        
        base.save(output_filename, quality = 100)

    def __generate_green_screen(self):
        """
        Generates a green screen rectangle of the provided 'width' and 'height' that has a rectangle
        black border.
        """
        shape = [(10, 10), (self.width - 10, self.height - 10)] 
        
        img = Image.new("RGB", (self.width, self.height)) 
        draw = ImageDraw.Draw(img)   
        r, g, b = self.__GREEN_SCREEN_RGB_COLOR
        draw.rectangle(shape, fill = ColorConverter.rgb_to_hex(r, g, b) , outline = 'black')

        filename = create_temp_filename('tmp_gs_shape.png')
        img.save(filename)

        return filename
    
    def insert_video(self, video_filename, output_filename):
        tmp_filename = create_temp_filename('tmp_gs.png')
        self.save(tmp_filename)

        clip = VideoFileClip(video_filename)
        green_screen_clip = ImageClip(tmp_filename, duration = clip.duration).with_effects([MaskColor(color = self.rgb_color, threshold = 100, stiffness = 5)])

        width = self.drx - self.ulx
        clip = clip.resized(width = width).with_position((self.ulx, self.uly))

        final_clip = CompositeVideoClip([clip, green_screen_clip], size = green_screen_clip.size)

        final_clip.write_videofile(output_filename, fps = clip.fps)

    def insert_image(self, image_filename, output_filename):
        # I do the trick with moviepy that is working for videos...
        tmp_filename = create_temp_filename('tmp_gs.png')
        self.save(tmp_filename)

        width = self.drx - self.ulx

        clip = ImageClip(image_filename, duration = 1 / 60).resized(width = width).with_position((self.ulx, self.uly))
        green_screen_clip = ImageClip(tmp_filename, duration = clip.duration).with_effects([MaskColor(color = self.rgb_color, threshold = 100, stiffness = 5)])

        final_clip = CompositeVideoClip([clip, green_screen_clip], size = green_screen_clip.size)
        final_clip.save_frame(output_filename, t = 0)

        # https://medium.com/@gowtham180502/how-can-we-replace-the-green-screen-background-using-python-4947f1575b1f
        """
        # https://www.geeksforgeeks.org/replace-green-screen-using-opencv-python/
        # TODO: Please, implement with this below, but by now (above)
        image = cv2.imread(self.__filename) 
        frame = cv2.imread(output_filename)
    
        width = self.drx - self.ulx
        height = self.dry - self.uly
        frame = resize_image(resize_image, width, height)

        u_green = np.array([104, 153, 70]) 
        l_green = np.array([30, 30, 0]) 
    
        mask = cv2.inRange(frame, l_green, u_green) 
        res = cv2.bitwise_and(frame, frame, mask = mask) 
    
        f = frame - res 
        f = np.where(f == 0, image, f) 
    
        cv2.imshow("video", frame) 
        cv2.imshow("mask", f) 
        """
    
