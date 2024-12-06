from setuptools import setup, find_packages

setup(
    name='transcribe_zh_en',
    version='1.5',
    packages=find_packages(),  # Automatically find all submodules
    install_requires=[         # List dependencies here
        'ffmpeg-python==0.2.0',
        'paddlespeech==1.4.2',
        'paddlepaddle-gpu==2.5.1',
        'numpy==1.23.5'
    ],
    entry_points={
        'console_scripts': [
            'transcribe_zh_en = transcribe_zh_en.main:main',  # Entry point to the main function
        ],
    },
    author="Mousa Abdulhamid",
    author_email="mousa.abdulhamid97@gmail.com",
    description="A package to transcribe Chinese subtitles and remove audio from videos",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Abdulhamid97Mousa/transcribe_zh_en",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)