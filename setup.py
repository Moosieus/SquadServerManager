from setuptools import setup

setup(
    name='SquadServerManager',
    version='0.1',
    description='A program that manages Squad server instances.',
    url='https://github.com/Moosieus/SquadServerManager',
    author='Moosieus',
    license='WTFPL',
    install_requires=[
        'discord.py',
        'steam',
        'aiorcon',
        'psutil',
        'fuzzywuzzy[speedup]',
        'apscheduler'
    ]
)
