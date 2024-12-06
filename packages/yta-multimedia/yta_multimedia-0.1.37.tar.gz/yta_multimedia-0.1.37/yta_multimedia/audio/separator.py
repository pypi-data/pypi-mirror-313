from yta_general_utils.file.filename import get_file_filename_without_extension
from subprocess import run


class AudioSeparator:
    """
    Class to simplify and encapsulate the functionality related to
    extracting vocals, instruments and more from a single audio.
    """
    def separate_audio_file_into_vocals_and_instruments(audio_filename: str, output_dirname: str):
        """
        This method will get 'audio_filename' audio file and will split
        it into 2 different files stored in 'output_dirname' directory.
        These 2 files will be 'vocals.wav' and 'accompaniment.wav' that
        are the vocals and the instrumental part, respectively, and 
        will be generated in a folder inside the 'output_dirname' 
        provided that is the 'audio_filename' file name without the
        extension, and will be returned by the function.

        If 'example.wav' provided as 'audio_filename' and 'test' as 
        'output_dirname', this method will create 
        'test/example/vocals.wav' and 'test/example/accompaniment.wav'
        audio files.
        """
        # This is using Spleeter, check this (https://github.com/deezer/spleeter/wiki/2.-Getting-started)
        #
        # This method needs a pre-trained model (that is downloaded from the repo)
        # for each type (2stems, 4stems or 5stems). These are downloaded by default
        # in 'pretrained_models' folder (project root) of the project in which code
        # is being executed
        #
        # You can also do 'spleeter:4stems' and 'spleeter:5stems'
        # 2stems ->   vocals.wav, accompaniment.wav
        # 4stems ->   vocals.wav, drums.wav, bass.wav, piano.wav
        # 5stems ->   vocals.wav, drums.wav, bass.wav, piano.wav and other.wav
        #
        # By now this method is only working for the '2stems' format so it will
        # generate 'vocals.wav' and 'accompaniment.wav' in the provided 
        # 'output_dirname'. We could personalize this in the future.
        
        # TODO: We should accept any type of audio and, if needed, we
        # write it to a local file to be read by the spleeter command
        if not audio_filename:
            return None
        
        # TODO: Make this dynamic (by using temporary values)
        if not output_dirname:
            return None
        
        command_str = 'spleeter separate -p spleeter:2stems -o ' + output_dirname + ' ' + audio_filename

        try:
            run(command_str)
        except:
            return False

        if not output_dirname.endswith('/'):
            output_dirname += '/'

        generated_output_folder = output_dirname + get_file_filename_without_extension(audio_filename)
        
        return generated_output_folder

        # TODO: Please, make it work with python code, this below is not working
        """
        from spleeter.audio.adapter import AudioAdapter
        from spleeter.separator import Separator

        separator = Separator('spleeter:2stems')
        # With this below we read file as numpy array (waveform parameter)
        #from scipy.io.wavfile import read
        #audiowave = read(audio_filename)
        audio_adapter = AudioAdapter.default()
        separator.separate_to_file(audio_descriptor = audio_filename, destination = output_dirname, audio_adapter = audio_adapter)
        separator.join()
        """