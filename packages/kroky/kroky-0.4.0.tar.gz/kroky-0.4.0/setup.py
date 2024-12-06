from setuptools import setup, find_packages

setup(
    name="kroky",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    description="A Python wrapper for interacting with the Kroky meal service website.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Jon Pečar Anželak",
    author_email="your.email@example.com",
    url="https://github.com/Jonontop/kroky-library",  # Change this to your actual URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
