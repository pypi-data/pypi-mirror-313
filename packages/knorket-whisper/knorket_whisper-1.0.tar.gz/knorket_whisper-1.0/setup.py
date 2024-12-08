import os

import pkg_resources
from setuptools import setup, find_packages

setup(
    name="knorket-whisper",
    py_modules=["knorket-whisper"],
    version="1.0",
    description="Speech Recognition plus diarization",
    readme="README.md",
    python_requires=">=3.7",
    author="ockhamlabs",
    author_email="hello@ockhamlabs.ai",
    url="https://github.com/yinruiqing/knorket-whisper",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    
    entry_points={
        'console_scripts': ['knorket-whisper=knorket_whisper.cli.transcribe:cli'],
    },
    include_package_data=True,
    extras_require={'dev': ['pytest']},
)
