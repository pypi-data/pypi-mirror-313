import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="PyPNM",
    version="1.12.1.2",
    author="Ilya Razmanov",
    author_email="ilyarazmanov@gmail.com",
    description="Reading and writing PPM and PGM image files, including 16 bits per channel.",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Dnyarri/PyPNM",
    packages=['pypnm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Topic :: File Formats"
    ],
    python_requires='>=3.10',
)
