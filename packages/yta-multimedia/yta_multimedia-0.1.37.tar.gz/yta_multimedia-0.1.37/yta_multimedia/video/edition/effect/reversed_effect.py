from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.parser import VideoParser
from moviepy.video.fx import TimeMirror
from moviepy import Clip


class ReversedEffect(Effect):
    """
    This method creates a new one but in reversa, also
    with the sound reversed.
    """
    def apply(self, video: Clip) -> Clip:
        # TODO: This is not working properly yet
        #PythonValidator.validate_method_params(BlinkEffect.apply, locals(), ['video'])
        video = VideoParser.to_moviepy(video)

        return TimeMirror().apply(video)
    
    # TODO: Here below is the old method that I will keep 
    # a couple of commits before I confirm it is working
    # @classmethod
    # def apply(cls, video: Union[str, VideoFileClip, VideoClip, CompositeVideoClip, ImageClip, ColorClip]):
    #     """
    #     Applies the effect to the provided 'video'.
    #     """
    #     video = VideoEffect.parse_moviepy_video(video)

    #     reversed_frames_array = VideoFrameExtractor.get_all_frames(video)[::-1]

    #     # TODO: Try to do this audio processing in memory
    #     AUDIO_FILE = create_temp_filename('tmp_audio.mp3')
    #     REVERSED_AUDIO_FILE = create_temp_filename('tmp_reversed_audio.mp3')
    #     video.audio.write_audiofile(AUDIO_FILE, fps = 44100)
    #     AudioSegment.from_mp3(AUDIO_FILE).reverse().export(REVERSED_AUDIO_FILE)
    #     reversed_audio = AudioFileClip(REVERSED_AUDIO_FILE)

    #     return ImageSequenceClip(reversed_frames_array, fps = video.fps).with_audio(reversed_audio)