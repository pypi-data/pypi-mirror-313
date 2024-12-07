# Youtube Autónomo Multimedia Utils Module

This module has been created to handle audio, images and video resources.

This project needs the next environment variables:
- [Audio] GIPHY_API_KEY
- [Audio.Music] MUSIXMATCH_API_KEY



## Audio Module
### Installation
<p>
Use the command 'pip install yta_voice_module'. Once installed, download this file (https://myshell-public-repo-hosting.s3.amazonaws.com/checkpoints_1226.zip) and place the content (folders 'base_speakers' and 'converter') inside this library, in the relative path 'yta_voice_module/resources/openvoice/checkpoints_v2' (you must create those folders). This is needed to use the 'imitate' open_voice functionality, that uses those models to run. Remember to find your library in your python user data. (!This readme will be improved in future versions).
</p>

<p>⚠ There are some libraries that need special installation as they are not public through _pip install_ command.</p>

==> MeloTTS <===
<p>
This library is not published in pypi, so we need to use the "pip install git+https://github.com/myshell-ai/MeloTTS.git" command to install it from the official repo. Also, use the "python -m unidic download" command to install any missing dictionary.

Here you have the official guide for any trouble (https://github.com/myshell-ai/OpenVoice/blob/main/docs/USAGE.md#quick-use).
</p>

==> OpenVoice <==
<p>
TODO: ¿Quizás probar "pip install git+https://github.com/myshell-ai/OpenVoice.git"? Como MeloTSS
This library is not published in pypi, so we need to handle it manually. First, we need to clone the official project with the "git clone https://github.com/myshell-ai/OpenVoice.git" command. Once downloaded, you install it by using the "pip install ./OpenVoice" command. Once installed, we need to manually change a line in the "se_extractor.py" file to let the model instantiation line use only the first argument (there are 3, but we cannot work with cuda nor float16). Please, read this official guide if any trouble (https://github.com/Alienpups/OpenVoice/blob/main/docs/USAGE_WINDOWS.md), and for downloading the "checkpoints_v2" we need to work. Place them in the project. If you have any trouble with languages, use the "python -m unidic download" command.

This library is for voice cloning and uses the MeloTTS library described in the previous step.
</p>

### Notes
- Nothing

## Image Module
### Installation