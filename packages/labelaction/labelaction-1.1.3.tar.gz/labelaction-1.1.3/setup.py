import codecs
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# you need to change all these
VERSION = '1.1.3'
DESCRIPTION = 'A GUI tool for annotating action in video files. '
setup(
    name="labelaction",
    version=VERSION,
    author="xie jiefeng",
    author_email="p2417822@mpu.edu.mo",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.10',
        'opencv-python>=4.10.0',
        'pandas>=2.2.0',

    ],
    keywords=[ 'Action label', 'Annotation tools','GUI'],
    entry_points={
        "console_scripts": [
            "labelaction=labelaction:main",
        ],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]

)
