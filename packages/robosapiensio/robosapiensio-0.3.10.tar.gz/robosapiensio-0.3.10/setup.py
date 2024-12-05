#**************************************************************************
# * Copyright (C) 2023-present Bert Van Acker (B.MKR) <bva.bmkr@gmail.com>
# * 
# * This file is part of the hybridIO project.
# * 
# * HybridIO can not be copied and/or distributed without the express
# * permission of Bert Van Acker
# *************************************************************************

import platform
from setuptools import setup, find_packages

from rpio import (
    __author__,
    __description__,
    __email__,
    __license__,
    __title__,
    __version__,
    __url__
)

#--- insert platform dependent setup ---
setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=open("README.md").read(),
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=__license__,
    #install_requires=__install_requires__,
    python_requires=">=3.10",
    packages=find_packages(include=["rpio", "rpio.*"]),
    package_data={'rpio': ['transformations/templates/*.template']},  # directory which contains the jinja templates
    include_package_data=True,
    install_requires = [
        line.strip() for line in open('requirements.txt')],
    entry_points={
        "console_scripts": [
            "rpio = rpio.__main__:main",
            "hio = rpio.__main__:main",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    keywords=[
        "Robotics",
        "Trustworthiness",
        "self-adaptive",
        "Model-based",
    ],
)