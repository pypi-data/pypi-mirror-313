from setuptools import setup, find_packages

setup(
    name="ddq_tkinter",
    version="0.2.4",
    packages=find_packages(),
    install_requires=[
        "tkcalendar",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A collection of custom tkinter widgets",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ddq_tkinter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 