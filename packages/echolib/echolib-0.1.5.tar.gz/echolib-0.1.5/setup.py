from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="echolib",
    version="0.1.5",
    author="Ayoub Achak",
    author_email="ayoub.achak01@example.com",
    description="An AI-driven library for generating content using HuggingFace and LMStudio models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayoubachak/echolib",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
        "transformers",
        "colorlog",
        "pyfiglet",
        "termcolor",
        "openai",
        "appdirs"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
