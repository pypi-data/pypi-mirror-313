from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="hex_htmltoimg",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        "html2image",
        "Pillow",
    ],
    author="azharbhat-dev",
    author_email="bazhar691@gmail.com",
    description="A module to generate images from HTML content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/hex_htmltoimg",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)