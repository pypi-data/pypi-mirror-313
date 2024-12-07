from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="GPTRouter",
    version="0.4.2",
    description="A Python package for working with GPTRouter APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email="sirjanpreet@writesonic.com",
    packages=["gpt_router"],
    install_requires=["httpx>=0.23.3", "pydantic>=1.10.13", "pyhumps>=3.8.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
