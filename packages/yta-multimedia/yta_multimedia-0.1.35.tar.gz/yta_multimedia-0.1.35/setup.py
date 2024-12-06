from setuptools import setup, find_packages


VERSION = '0.1.35'
DESCRIPTION = 'Youtube Autónomo Multimedia Module is here.'
LONG_DESCRIPTION = 'These are all the multimedia utils we need in the Youtube Autónomo project to work in a better way. This module includes audio, image and video generation and editing utilities.'

setup(
        name = "yta_multimedia", 
        version = VERSION,
        author = "Daniel Alcalá",
        author_email = "<danielalcalavalera@gmail.com>",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        packages = find_packages(),
        install_requires = [
            # Audio module
            'pyttsx3',
            'gtts',
            'pydub',
            'pedalboard',
            'spleeter',
            'bezier',
            # Image module
            'pillow',
            # Video module
            #'moviepy',
            # This below breaks everything as there is a problem with the
            # 'click' library and I have to manually reinstall 'manim' any
            # time I install 'yta_multimedia' by pip.
            #'manim' 
        ],
        
        keywords = [
            'youtube autonomo multimedia utils module'
        ],
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)