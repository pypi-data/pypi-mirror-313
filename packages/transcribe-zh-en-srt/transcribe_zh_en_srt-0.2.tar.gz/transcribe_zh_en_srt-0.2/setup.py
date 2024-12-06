from setuptools import setup, find_packages

setup(
    name='transcribe_zh_en_srt',
    version='0.2',
    packages=find_packages(),  # Automatically find all submodules
    install_requires=[         # List dependencies here
   
    'numpy==1.24.4',
    'torch==2.4.1',
    'triton==3.0.0',
    'python-dotenv',                  
    'demucs==4.0.1',
    'omegaconf==2.3.0',
    'openunmix==1.2.1',
    'requests==2.32.3',
    'retrying==1.3.4',
    'six==1.16.0',
    'submitit==1.5.2',
    'sympy==1.13.3',
    'wheel==0.45.1'
  
                      ],
    entry_points={
        'console_scripts': [
            'transcribe_zh_en_srt = transcribe_zh_en_srt.main:main',  # Entry point to the main function
        ],
    },
    author="Mousa Abdulhamid",
    author_email="mousa.abdulhamid97@gmail.com",
    description="A package to process audio and generate translation from input language to target language. this package return srt format files containing english accurated translation from Chinese language to English language.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Abdulhamid97Mousa/transcribe_zh_en_srt",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
