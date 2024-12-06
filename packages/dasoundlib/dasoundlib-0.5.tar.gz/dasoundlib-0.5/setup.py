from setuptools import setup, find_packages

# Read the contents of README.md
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='dasoundlib',
    version='0.5',
    author='ForNoOne401',
    author_email='fornoone401401@gmail.com',
    description='A package to generate and play sine wave sounds',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ForNoOne401/Soundlib',
    packages=find_packages(include=['Soundlib', 'Soundlib.*']),
    package_data={'Soundlib': ['_soundlib.pyd']},
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
    ],
    python_requires='>=3.6',
)
