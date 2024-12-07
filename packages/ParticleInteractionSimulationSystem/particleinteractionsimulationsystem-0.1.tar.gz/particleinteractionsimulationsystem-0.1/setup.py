from setuptools import setup, find_packages

setup(
    name='ParticleInteractionSimulationSystem',
    version='0.1',
    packages=find_packages(),
    description='A Lightweight Pygame Particle System',
    author='SirBilby',
    license='MIT',
    install_requires=[
        'pygame'
    ],
)