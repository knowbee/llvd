from setuptools import setup, find_packages
from os import path
import llvd

current_dir = path.abspath(path.dirname(__file__))

with open(path.join(current_dir, "README.md"), "r", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="llvd",
    version=llvd.__version__,
    url="https://github.com/knowbee/llvd.git",
    author="Igwaneza Bruce",
    author_email="knowbeeinc@gmail.com",
    description="Linkedin Learning Video Downloader CLI Tool",
    long_description=readme,
    long_description_content_type="text/markdown",
    platforms="any",
    python_requires=">=3.6",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "beautifulsoup4==4.11.1",
        "certifi==2022.12.7",
        "chardet==5.1.0",
        "click==8.1.3",
        "idna==3.4",
        "requests==2.28.1",
        "soupsieve==2.3.2",
        "tqdm==4.64.1",
        "urllib3==1.26.13",
        "click_spinner==0.1.10"
    ],
    entry_points={"console_scripts": ["llvd = llvd.cli:main"]},
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
