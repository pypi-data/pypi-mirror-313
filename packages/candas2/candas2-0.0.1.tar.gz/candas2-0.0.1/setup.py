from setuptools import setup, find_packages

setup(
    name="candas2",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[],
    author="Dr-Br0t",
    author_email="dr.br00tz@gmail.com",
    description="This is a project inspired on the original Candas library by https://gist.github.com/JulianWgs, a blf file can be handle in a faster way using python data science classical libraries.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Dr-Br0t/Candas2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    license="GNU Affero General Public License v3"
)
