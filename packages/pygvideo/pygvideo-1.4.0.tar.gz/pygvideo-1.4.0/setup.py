from setuptools import find_packages, setup

with open('requirements.txt') as req:
    install_requirements = req.read().splitlines()

with open('README.md') as README:
    readme = README.read()

setup(
    name = 'pygvideo',
    version = '1.4.0',
    description = 'pygvideo, video for pygame. Using moviepy video module to read and organize videos.',
    url = 'https://github.com/azzammuhyala/pygvideo.git',
    author = 'azzammuhyala',
    author_email = 'azzammuhyala@gmail.com',
    license = 'MIT',
    python_requires = '>=3.10',
    long_description_content_type = 'text/markdown',
    long_description = readme,
    packages = find_packages(),
    include_package_data = True,
    install_requires = install_requirements,
    keywords = [
        'pygvideo', 'pygamevid', 'pyvidplayer', 'pygame vid', 'pygame video', 'video player', 'vid player',
        'pygame player', 'python pygame video', 'pgvideo', 'pgvid', 'video', 'player', 'pygame video player'
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Multimedia :: Sound/Audio :: Analysis',
        'Topic :: Multimedia :: Video',
        'Topic :: Multimedia :: Video :: Capture',
        'Topic :: Multimedia :: Video :: Conversion'
    ]
)