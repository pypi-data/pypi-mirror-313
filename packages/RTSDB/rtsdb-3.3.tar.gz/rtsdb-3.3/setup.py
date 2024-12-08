from setuptools import setup, find_packages

setup(
    name='RTSDB',
    version='3.3',
    packages=find_packages(),
    description='Create yourself a simple database with this package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='RandomTimeTV',
    author_email='dergepanzerte1@gmail.com',
    license='MIT with required credit to the author.',
    url='https://github.com/RandomTimeLP/RTS_DataBase/',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='database',
    install_requires=["extradecorators","extrautilities","aiohttp"],
)