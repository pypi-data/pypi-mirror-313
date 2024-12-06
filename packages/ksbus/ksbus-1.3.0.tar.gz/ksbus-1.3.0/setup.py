from setuptools import find_packages, setup

VERSION = '1.3.0'
DESCRIPTION = 'Ksbus client for https://github.com/kamalshkeir/ksbus'
LONG_DESCRIPTION = 'Ksbus client for https://github.com/kamalshkeir/ksbus'

# Setting up
setup(
    name="ksbus",
    version=VERSION,
    author="Ksbus (Kamal Shkeir)",
    author_email="<kamalshkeir@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['asyncio', 'websockets'],
    keywords=['eventbus', 'bus', 'ksbus', 'korm', 'pubsub', 'websockets','ws'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)