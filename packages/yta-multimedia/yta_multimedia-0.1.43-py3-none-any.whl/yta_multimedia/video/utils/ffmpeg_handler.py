"""
Nice help: https://www.bannerbear.com/blog/how-to-use-ffmpeg-in-python-with-examples/
Official doc: https://www.ffmpeg.org/ffmpeg-resampler.html
More help: https://kkroening.github.io/ffmpeg-python/
Nice guide: https://img.ly/blog/ultimate-guide-to-ffmpeg/
Available flags: https://gist.github.com/tayvano/6e2d456a9897f55025e25035478a3a50

Interesting usage: https://stackoverflow.com/a/20325676
Maybe avoid writting on disk?: https://github.com/kkroening/ffmpeg-python/issues/500#issuecomment-792281072
"""
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.audio.parser import AudioParser
from yta_general_utils.temp import create_temp_filename
from yta_general_utils.image.parser import ImageParser
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.file.writer import FileWriter
from typing import Union
from subprocess import run


class FfmpegAudioCodec(Enum):
    """
    TODO: Fill this

    Should be used in the **-c:a {codec}** flag.
    """
    AAC = 'aac'
    """
    Default encoder.
    """
    AC3 = 'ac3'
    """
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ac3-and-ac3_005ffixed
    """
    AC3_FIXED = 'ac3_fixed'
    """
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ac3-and-ac3_005ffixed
    """
    FLAC = 'flac'
    """
    FLAC (Free Lossless Audio Codec) Encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-flac-2
    """
    OPUS = 'opus'
    """
    This is a native FFmpeg encoder for the Opus format. Currently, it’s
    in development and only implements the CELT part of the codec. Its
    quality is usually worse and at best is equal to the libopus encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-opus
    """
    LIBFDK_AAC = 'libfdk_aac'
    """
    libfdk-aac AAC (Advanced Audio Coding) encoder wrapper. The libfdk-aac
    library is based on the Fraunhofer FDK AAC code from the Android project.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libfdk_005faac
    """
    LIBLC3 = 'liblc3'
    """
    liblc3 LC3 (Low Complexity Communication Codec) encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-liblc3
    """
    LIBMP3LAME = 'libmp3lame'
    """
    LAME (Lame Ain’t an MP3 Encoder) MP3 encoder wrapper.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libmp3lame-1
    """
    LIBOPENCORE_AMRNB = 'libopencore_amrnb'
    """
    OpenCORE Adaptive Multi-Rate Narrowband encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libopencore_002damrnb-1ss
    """
    LIBOPUS = 'libopus'
    """
    libopus Opus Interactive Audio Codec encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libopus-1
    """
    LIBSHINE = 'libshine'
    """
    Shine Fixed-Point MP3 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libshine-1
    """
    LIBTWOLAME = 'libtwolame'
    """
    TwoLAME MP2 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libtwolame
    """
    LIBVO_AMRWBENC = 'libvo-amrwbenc'
    """
    VisualOn Adaptive Multi-Rate Wideband encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libvo_002damrwbenc
    """
    LIBVORBIS = 'libvorbis'
    """
    libvorbis encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libvorbis
    """
    MJPEG = 'mjpeg'
    """
    Motion JPEG encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-mjpeg
    """
    WAVPACK = 'wavpack'
    """
    WavPack lossless audio encoder.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-wavpack
    """

class FfmpegVideoCodec(Enum):
    """
    These are the video codecs available as Enums. The amount of codecs
    available depends on the ffmpeg built version.
    
    Should be used in the **-c:v {codec}** flag.
    """
    A64_MULTI = 'a64_multi'
    """
    A64 / Commodore 64 multicolor charset encoder. a64_multi5 is extended with 5th color (colram).

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-a64_005fmulti_002c-a64_005fmulti5
    """
    A64_MULTI5 = 'a64_multi5'
    """
    A64 / Commodore 64 multicolor charset encoder. a64_multi5 is extended with 5th color (colram).

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-a64_005fmulti_002c-a64_005fmulti5
    """
    CINEPAK = 'Cinepak'
    """
    Cinepak aka CVID encoder. Compatible with Windows 3.1 and vintage MacOS.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Cinepak
    """
    GIF = 'GIF'
    """
    GIF image/animation encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Cinepak
    """
    HAP = 'Hap'
    """
    Vidvox Hap video encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-Hap
    """
    JPEG2000 = 'jpeg2000'
    """
    The native jpeg 2000 encoder is lossy by default

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-jpeg2000
    """
    LIBRAV1E = 'librav1e'
    """
    rav1e AV1 encoder wrapper.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-librav1e
    """
    LIBAOM_AV1 = 'libaom-av1'
    """
    libaom AV1 encoder wrapper.
    
    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libaom_002dav1
    """
    # TODO: Continue with this (https://www.ffmpeg.org/ffmpeg-codecs.html#toc-libsvtav1)
    QTRLE = 'qtrle'
    """
    TODO: Find information about this video codec.

    More info: ???
    """
    PRORES = 'prores'
    """
    Apple ProRes encoder.

    More info: https://www.ffmpeg.org/ffmpeg-codecs.html#toc-ProRes
    """

class FfmpegVideoFormat(Enum):
    """
    Enum list to simplify the way we choose a video format for
    the ffmpeg command. This should be used with the FfmpegFlag
    '-f' flag that forces that video format.

    Should be used in the **-f {format}** flag.
    """
    CONCAT = 'concat'
    """
    The format will be the concatenation.
    """
    AVI = 'avi'
    """
    Avi format.

    # TODO: Explain more
    """
    PNG = 'png'
    """
    # TODO: Look for mor information about this vcodec
    # TODO: I don't know if this one is actually an FfmpegVideoFormat
    # or if I need to create another Enum class. This option us used
    # in the '-vcodec' option, and the other ones are used in the
    # 'c:v' option.
    """
    # TODO: Keep going

class FfmpegFilter(Enum):
    """
    Enum list to simplify the way we use a filter for the
    ffmpeg command.

    Should be used in the **-filter {filter}** flag.
    """
    THUMBNAIL = 'thumbnail'
    """
    Chooses the most representative frame of the video to be used
    as a thumbnail.
    """

class FfmpegPixelFormat(Enum):
    """
    Enum list to simplify the way we use a pixel format for
    the ffmpeg command.

    Should be used in the **-pix_fmt {format}** flag.
    """
    YUV420p = 'yuv420p'
    """
    This is de default value. TODO: Look for more information about it
    """
    RGB24 = 'rgb24'
    """
    TODO: Look for more information about this pixel format.
    """
    ARGB = 'argb'
    """
    TODO: Look for more information about this pixel format
    """
    YUVA444P10LE = 'yuva444p10le'
    """
    TODO: Look for more information about this pixel format
    """

class FfmpegFlag:
    """
    Class to simplify the way we push flags into the ffmpeg command.
    """
    overwrite: str = '-y'
    """
    Overwrite the output file if existing.

    Notation: **-y**
    """

    @classmethod
    def force_format(cls, format: FfmpegVideoFormat):
        """
        Force the output format to be the provided 'format'.

        Notation: **-f {format}**
        """
        format = FfmpegVideoFormat.to_enum(format).value

        return f'-f {format}'
    
    @classmethod
    def safe_routes(cls, value: int):
        """
        To enable or disable unsafe paths.

        Notation: **-safe {value}**
        """
        # TODO: Check that 'value' is a number between -1 and 1

        return f'-safe {str(value)}'
    
    @classmethod
    def input(cls, input: str):
        """
        To set the input (or inputs) we want.

        Notation: **-i {input}**
        """
        # TODO: I don't know how to check this or format it from 'input' param

        return f'-i {input}'
    
    @classmethod
    def audio_codec(cls, codec: Union[FfmpegAudioCodec, str]):
        """
        Sets the general audio codec.

        Notation: **-c:a {codec}**
        """
        # We cannot control the big amount of audio codecs that
        # are available so we allow any string as parameter
        try:
            codec = FfmpegAudioCodec.to_enum(codec).value
        except:
            pass

        return f'-c:a {codec}'
    
    @classmethod
    def video_codec(cls, codec: Union[FfmpegVideoCodec, str]):
        """
        Sets the general video codec.

        Notation: **-c:v {codec}**
        """
        # We cannot control the big amount of video codecs that
        # are available so we allow any string as parameter
        try:
            codec = FfmpegVideoCodec.to_enum(codec).value
        except:
            pass

        return f'-c:v {codec}'

    @classmethod
    def v_codec(cls, codec: Union[FfmpegVideoCodec, str]):
        """
        Sets the video codec.

        TODO: I don't know exactly the difference between '-c:v {codec}'
        and the '-vcodec' generated in this method. I keep this method
        until I actually find the difference. I don't even know if the
        video codecs I can provide as values are the same as in the other
        method.

        Notation: **-vcodec {codec}**
        """
        # We cannot control the big amount of video codecs that
        # are available so we allow any string as parameter
        try:
            codec = FfmpegVideoCodec.to_enum(codec).value
        except:
            pass

        return f'-vcodec {codec}'

    @classmethod
    def codec(cls, codec: Union[FfmpegVideoCodec, FfmpegAudioCodec, str]):
        """
        Sets the general codec with '-c {codec}'.

        -c copy indica que se deben copiar los flujos de audio y video sin recodificación, lo que hace que la operación sea rápida y sin pérdida de calidad. TODO: Turn this 'copy' to AudioCodec and VideoCodec (?)

        Notation: **-c {codec}**
        """
        # We cannot control the big amount of video codecs that
        # are available so we allow any string as parameter

        # TODO: Validate provided 'codec'
        # TODO: This method has a variation, it can be '-c:a' or '-c:v'
        if not isinstance(codec, (FfmpegVideoCodec, FfmpegAudioCodec)):
            try:
                codec = FfmpegVideoCodec.to_enum(codec)
            except:
                pass

        if not isinstance(codec, (FfmpegVideoCodec, FfmpegAudioCodec)):
            try:
                codec = FfmpegAudioCodec.to_enum(codec)
            except:
                pass

        if isinstance(codec, (FfmpegVideoCodec, FfmpegAudioCodec)):
            codec = codec.value

        return f'-c {codec}'
    
    @classmethod
    def map(cls, map: str):
        """
        Set input stream mapping.
        -map [-]input_file_id[:stream_specifier][,sync_file_id[:stream_s set input stream mapping

        # TODO: Improve this

        Notation: **-map {map}**
        """
        return f'-map {map}'
    
    @classmethod
    def filter(cls, filter: FfmpegFilter):
        """
        Sets the expected filter to be used.

        Notation: **-filter {filter}**
        """
        filter = FfmpegFilter.to_enum(filter).value

        return f'-filter {filter}'
    
    @classmethod
    def frame_rate(cls, frame_rate: int):
        """
        Sets the frame rate (Hz value, fraction or abbreviation)

        Notation: **-r {frame_rate}**
        """
        # TODO: Validate 'frame_rate'

        return f'-r {str(frame_rate)}'
    
    @classmethod
    def pixel_format(cls, format: FfmpegPixelFormat):
        """
        Sets the pixel format.

        Notation: **-pix_fmt {format}**
        """
        format = FfmpegPixelFormat.to_enum(format).value

        return f'-pix_fmt {format}'


class FfmpegHandler:
    """
    Class to simplify and encapsulate ffmpeg functionality.
    """
    @classmethod
    def _validate_video_filename(cls, video_filename: str):
        # TODO: Validate and raise Exception if invalid
        pass

    @classmethod
    def write_concat_file(cls, filenames: str):
        """
        Writes the files to concat in a temporary text file with
        the required format and returns that file filename. This
        is required to use different files as input.
        """
        text = ''
        for filename in filenames:
            text += f"file '{filename}'\n"

        # TODO: Maybe this below is interesting for the 'yta_general_utils.file.writer'
        # open('concat.txt', 'w').writelines([('file %s\n' % input_path) for input_path in input_paths])
        filename = create_temp_filename('concat_ffmpeg.txt')
        FileWriter.write_file(text, filename)

        return filename

    @classmethod
    def run_command(cls, args: list[str]):
        """
        Runs an ffmpeg provided with the provided 'args' as a subprocess.
        """
        # TODO: Clean args (?)
        # Remove 'None' args, our logic allow that to make it easier
        args = [arg for arg in args if arg is not None]

        # TODO: Validate args

        run(f"ffmpeg {' '.join(args)}")

    # TODO: Check this one below
    @classmethod
    def get_audio_from_video_deprecated(cls, video_filename: str, codec: FfmpegAudioCodec = None, output_filename: str = None):
        """
        Exports the audio of the provided video to a local file named
        'output_filename' if provided or as a temporary file.

        # TODO: This has not been tested yet.

        This methods returns a tuple with the audio as a moviepy audio 
        in the first place and the filename of the file generated in
        the second place.
        """
        cls._validate_video_filename(video_filename)
        
        if not output_filename:
            output_filename = create_temp_filename('temp_audio.mp3')
        # TODO: Validate 'output_filename' is a valid audio filename

        if codec:
            codec = FfmpegAudioCodec.to_enum(codec)

        cls.run_command([
            FfmpegFlag.input(video_filename),
            FfmpegFlag.audio_codec(codec) if codec else None,
            output_filename
        ])

        return AudioParser.to_audiofileclip(output_filename), output_filename
    
    @classmethod
    def get_audio_from_video(cls, video_filename: str, output_filename: str = None):
        """
        Exports the audio of the provided video to a local file named
        'output_filename' if provided or as a temporary file.

        This methods returns a tuple with the audio as a moviepy audio 
        in the first place and the filename of the file generated in
        the second place.
        """
        cls._validate_video_filename(video_filename)
        
        if not output_filename:
            output_filename = create_temp_filename('temp_audio.mp3')

        # TODO: Verify valid output_filename extension

        cls.run_command([
            FfmpegFlag.input(video_filename),
            FfmpegFlag.map('0:1'),
            output_filename
        ])

        return AudioParser.to_audiofileclip(output_filename), output_filename

    @classmethod
    def get_best_thumbnail(cls, video_filename: str, output_filename: str = None):
        """
        Gets the best thumbnail of the provided 'video_filename'.

        This methods returns a tuple with the thumbnail as a pillow 
        image in the first place and the filename of the file generated
        in the second place.
        """
        cls._validate_video_filename(video_filename)

        if not output_filename:
            output_filename = create_temp_filename('temp_thumbnail.png')
        # TODO: Verify valid extension

        cls.run_command([
            FfmpegFlag.input(video_filename),
            FfmpegFlag.filter(FfmpegFilter.THUMBNAIL),
            output_filename
        ])

        return ImageParser.to_pillow(output_filename), output_filename
    
    @classmethod
    def concatenate_videos(cls, video_filenames: str, output_filename: str = None):
        """
        Concatenates the provided 'video_filenames' in the order in
        which they are provided.

        This methods returns a tuple with the new video as a moviepy
        video in the first place and the filename of the file generated
        in the second place.
        """
        for video_filename in video_filenames:
            cls._validate_video_filename(video_filename)

        # TODO: Use new output handler
        if not output_filename:
            output_filename = create_temp_filename('concatenated_video.mp4')

        concat_filename = cls.write_concat_file(video_filenames)

        cls.run_command([
            FfmpegFlag.overwrite,
            FfmpegFlag.force_format(FfmpegVideoFormat.CONCAT),
            FfmpegFlag.safe_routes(0),
            FfmpegFlag.input(concat_filename),
            FfmpegFlag.codec('copy'),
            output_filename
        ])

        return VideoParser.to_moviepy(output_filename), output_filename
    
    @classmethod
    def concatenate_images(cls, image_filenames: str, frame_rate = 60, pixel_format: FfmpegPixelFormat = FfmpegPixelFormat.YUV420p, output_filename: str = None):
        """
        Concatenates the provided 'image_filenames' in the order in
        which they are provided.

        This methods returns a tuple with the new video as a moviepy
        video in the first place and the filename of the file generated
        in the second place.
        """
        for image_filename in image_filenames:
            cls._validate_video_filename(image_filename)

        if not output_filename:
            output_filename = create_temp_filename('concatenated_video.mp4')

        concat_filename = cls.write_concat_file(image_filenames)

        # TODO: Should we check the pixel format or give freedom (?)
        # pixel_format = FfmpegPixelFormat.to_enum(pixel_format)

        cls.run_command([
            FfmpegFlag.force_format(FfmpegVideoFormat.CONCAT),
            FfmpegFlag.safe_routes(0),
            FfmpegFlag.overwrite,
            FfmpegFlag.frame_rate(frame_rate),
            FfmpegFlag.input(concat_filename),
            FfmpegFlag.video_codec(FfmpegVideoCodec.QTRLE),
            FfmpegFlag.pixel_format(pixel_format), # I used 'argb' in the past
            output_filename
        ])

        return VideoParser.to_moviepy(output_filename), output_filename
    
    # TODO: Create a 'set_audio_in_video' method to replace the
    # yta_multimedia\video\audio.py > set_audio_in_video_ffmpeg

    # TODO: Keep going

    # https://www.reddit.com/r/ffmpeg/comments/ks8zfs/comment/gieu7x6/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # https://stackoverflow.com/questions/38368105/ffmpeg-custom-sequence-input-images/51618079#51618079
    # https://stackoverflow.com/a/66014158