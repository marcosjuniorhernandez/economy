from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    longDescription = fh.read()

setup(
    name="oikos",
    version="0.1.0",
    author="Marcos Jr.",
    author_email="iam.marcoshernandez@gmail.com",
    description="Library for modeling and graphing economic models in Python.",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://github.com/marcosjuniorhernandez/economy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License"
    ],
    install_requires=["numpy", "matplotlib"],
    python_requires=">=3.8"
)