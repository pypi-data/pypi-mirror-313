from yta_multimedia.video.generation.rrss.discord.classes.discord_conversation_character import DiscordConversationCharacter
from yta_multimedia.image.generation.rrss.discord.discord_message_image_generator import DiscordMessageImageGenerator
from yta_multimedia.video.generation.rrss.discord.constants import DISCORD_MESSAGE_RECEIVED_AUDIO_FILENAME, DISCORD_MESSAGE_RECEIVED_AUDIO_GOOGLE_DRIVE_URL
from yta_multimedia.video.generation.rrss.discord.enums import DiscordConversationMessageMode
from yta_multimedia.resources import Resource
from yta_general_utils.image.converter import ImageConverter
from moviepy import AudioFileClip, ColorClip, CompositeVideoClip, ImageClip


class DiscordConversationMessage:
    character = None
    text = None
    duration = None

    def __init__(self, character: DiscordConversationCharacter, text: str, duration: float = None, mode: DiscordConversationMessageMode = DiscordConversationMessageMode.NORMAL, image_url: str = None, sound = None, effect = None):
        # TODO: Ignore 'sound' and 'effect' by now. Implement later
        if not character:
            raise Exception('No "character" provided.')
        
        # TODO: Check that character is 'DiscordConversationCharacter' type

        if not text:
            raise Exception('No "text" provided.')
        
        # TODO: Check if 'mode' is 'DiscordConversationMessageMode' type
        if not mode:
            mode = DiscordConversationMessageMode.NORMAL

        # TODO: Check if 'image_url' and that is valid image url

        # TODO: Check if 'sound' that is valid

        # TODO: Check if 'effect' that is valid

        if not duration:
            # No fixed duration so we calculate it (default: SLOW mode)
            character_duration = 0.10
            self.duration = 0.6
            if mode == DiscordConversationMessageMode.NORMAL:
                self.duration = 0.45
                character_duration = 0.08
            elif mode == DiscordConversationMessageMode.FAST:
                self.duration = 0.3
                character_duration = 0.06

            if len(text) > 8:
                # Long messages need longer duration
                self.duration = character_duration * len(text)
        else:
            self.duration = duration

        self.character = character
        self.text = text
        # TODO: Handle 'image_url'
        # TODO: Handle 'effect'
        self.discord_message_image_generator = DiscordMessageImageGenerator()

    def generate_clip(self):
        """
        Generates a clip with the discord message received audio, the
        specific 'sound' if provided, with the discord message in the
        center of the video.

        This method returns a moviepy CompositeVideoClip.
        """
        audioclip = AudioFileClip(Resource.get(DISCORD_MESSAGE_RECEIVED_AUDIO_GOOGLE_DRIVE_URL, DISCORD_MESSAGE_RECEIVED_AUDIO_FILENAME))
        # TODO: Handle 'self.sound' and use CompositeAudioClip

        image = self.discord_message_image_generator.generate(self.character.username, self.character.avatar_url, self.text)
        # Original image is too wide, we shorten it by the half 
        # TODO: We could do a x3 and limit the amount of chars in text
        image = image.crop((0, 0, image.width / 2, image.height))
        image = image.resize((image.width * 2, image.height * 2))
        # Open it with Image.open(image)

        # TODO: Make this duration dynamic
        clip = CompositeVideoClip([
            # Black background to make the Image fit
            ColorClip((1920, 1080), (0, 0, 0), duration = self.duration),
            # We set it in the center of the video
            ImageClip(ImageConverter.pil_image_to_numpy(image), duration = self.duration).with_position((1920 / 2 - image.width / 2, 1080 / 2 - image.height / 2))
        ])

        if audioclip.duration > clip.duration:
            audioclip.with_subclip(0, clip.duration)

        clip = clip.with_audio(audioclip).with_fps(60)

        return clip