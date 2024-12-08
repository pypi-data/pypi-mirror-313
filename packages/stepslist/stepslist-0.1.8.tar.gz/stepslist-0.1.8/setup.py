from setuptools import setup, find_packages

setup(
    name='stepslist',
    version='0.1.8',
    packages=find_packages(),
    entry_points={
        'markdown.extensions': [
            'stepslist = stepslist.stepslist:makeExtension',
        ],
    },
    author='Chris van Liere',
    author_email='c.vnliere@gmail.com',
    description='A MkDocs extension to convert <steps> tags into ordered lists.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/a3bagged/stepslist-extension',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)