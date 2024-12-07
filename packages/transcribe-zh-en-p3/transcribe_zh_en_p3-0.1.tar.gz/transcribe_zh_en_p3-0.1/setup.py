from setuptools import setup, find_packages

setup(
    name='transcribe_zh_en_p3',
    version='0.1',
    packages=find_packages(),  # Automatically find all submodules
    install_requires=[         # List dependencies here
    'torch==2.4.1',
    'python-dotenv',                  
    'requests==2.32.3',
    'submitit==1.5.2',
    'wheel==0.45.1',
    'numpy==1.23.5',
    'pysrt==1.1.2',
    'pydub==0.25.1',
    ],
    entry_points={
        'console_scripts': [
            'transcribe_zh_en_p3 = transcribe_zh_en_p3.main:main',  # Entry point to the main function
        ],
    },
    author="Abdulhamid Mousa",
    author_email="mousa.abdulhamid97@gmail.com",
    description="A package to process video and generate video from input language to target language.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Abdulhamid97Mousa/transcribe_zh_en_p3",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)


