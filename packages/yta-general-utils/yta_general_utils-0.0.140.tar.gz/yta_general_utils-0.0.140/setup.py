from setuptools import setup, find_packages


VERSION = '0.0.140'
DESCRIPTION = 'Youtube Autónomo general utils are here.'
LONG_DESCRIPTION = 'These are the general utils we need in the Youtube Autónomo project to work in a better way.'

setup(
        name = "yta_general_utils", 
        version = VERSION,
        author = "Daniel Alcalá",
        author_email = "<danielalcalavalera@gmail.com>",
        description = DESCRIPTION,
        long_description = LONG_DESCRIPTION,
        packages = find_packages(),
        install_requires = [
            'moviepy',
            'pillow',
            'backgroundremover',
            'scikit-image',
            'opencv-python',
            'numpy',
            'pyttsx3',
            'gtts',
            'pydub',
            'torch',
            'torchaudio',
            'deepfilternet'
        ],
        
        keywords = [
            'youtube autonomo general utils'
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