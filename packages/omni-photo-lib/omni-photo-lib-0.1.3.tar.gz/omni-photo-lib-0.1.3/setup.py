from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="omni-photo-lib",  # Unique package name
    version="0.1.3",  # Start with a low version
    description="A library for generating images",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Markdown for PyPI
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "requests",
        "together",
        "celery",
    ],
    author="Adhithyan",
    author_email="adhithyan@omnineura.ai",
    url="",  
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
