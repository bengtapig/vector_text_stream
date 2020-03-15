import os, sys
from setuptools import setup, find_packages

def read_requirements():
    """Parse requirements from requirements.txt."""
    reqs_path = os.path.join('.', 'requirements.txt')
    with open(reqs_path, 'r') as f:
        requirements = [line.rstrip() for line in f]
    return requirements

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vector_text_stream',
    version='0.0.1',
    description='Package for showing texts on the screen of Vector with sliding animation',
    long_description=long_description,
    author='Ryo Sakagami',
    author_email='sakagamiry@gmail.com',
    install_requires=read_requirements(),
    url='https://github.com/ryosakagami/vector_text_stream',
    license='MIT License',
    packages=find_packages(),
    package_data={'vector_text_stream': ['fonts/JF-Dot-jiskan24.ttf', 'fonts/LICENSE', 'fonts/README.md']},
    include_package_data=True
)