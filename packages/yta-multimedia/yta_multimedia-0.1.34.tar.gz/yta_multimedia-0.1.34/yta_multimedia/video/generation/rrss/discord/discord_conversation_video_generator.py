from yta_multimedia.video.generation.rrss.discord.classes.discord_conversation_message import DiscordConversationMessage
from moviepy import concatenate_videoclips
from typing import Union


class DiscordConversationVideoGenerator:
    def __init__(self):
        pass

    def generate_clip(self, messages: list[DiscordConversationMessage], output_filename: Union[str, None] = None):
        """
        Generates a video clip with the provided messages. This method
        will return the clip and also write it locally if 'output_filename'
        is provided.
        """
        if not messages:
            raise Exception('No "messages" provided.')
        
        clips = []
        for index, message in enumerate(messages):
            # If previous clip is from the same author, concat the 'text'
            if len(clips) > 0:
                previous_message = messages[index - 1]
                if previous_message.character == message.character:
                    message.text = previous_message.text + '\\n' + message.text

            clips.append(message.generate_clip())

        clip = concatenate_videoclips(clips).with_fps(60)

        if output_filename:
            clip.write_videofile(output_filename)

        return clip