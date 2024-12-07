from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup (
    name='obstacles',
    version='2.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'obstacles-game = Obstacles:obstacles_game'
        ]
    },
    description='This is a simple arcade-style game where you have to miss the obstacles',
    long_description=description,
    long_description_content_type='text/markdown'
)