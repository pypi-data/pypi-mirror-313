from setuptools import setup, find_packages

setup(
    name="bruce-models",
    version="0.0.1",
    description="This is a library which defines data-models for the Nextspace API and provides functions for communicating with the endpoints.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Matvey Lavrinovich",
    author_email="matveylavrinovich@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests>=2.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers"
    ],
    python_requires=">=3.6",
)
