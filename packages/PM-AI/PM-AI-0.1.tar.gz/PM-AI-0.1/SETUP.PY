from setuptools import setup,find_packages       #Works on python 3.11.7

setup(
    name='PM-AI',
    version='0.1',
    author='Prajurjya Mohapatra',
    author_email='mrperfectprajurjya@gmail.com',
    description='This is speech to text package created by the author',
),

packages = find_packages(),

install_requirements = [
    'random',
]