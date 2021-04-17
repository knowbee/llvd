from setuptools import setup
from os import path

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, "README.md"), "r") as f:
    readme = f.read()

setup(
    name="llvd",
    version="2.0.8",
    url="https://github.com/knowbee/llvd.git",
    author="Igwaneza Bruce",
    author_email="knowbeeinc@gmail.com",
    description="Linkedin Learning Video Downloader CLI Tool",
    long_description=readme,
    long_description_content_type="text/markdown",
    platforms="any",
    python_requires=">=3.6",
    packages=["llvd"],
    install_requires=[
        "beautifulsoup4==4.9.3",
        "certifi==2020.12.5",
        "chardet==4.0.0",
        "click==7.1.2",
        "idna==2.10",
        "requests==2.25.1",
        "soupsieve==2.1",
        "tqdm==4.55.0",
        "urllib3==1.26.2",
        "click_spinner== 0.1.10"
    ],
    entry_points={
        "console_scripts": ['llvd = llvd:main']
    },
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
