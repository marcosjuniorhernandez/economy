from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    longDescription = fh.read()

setup(
    name="oikos",
    version="0.3.1",
    author="Marcos Junior Hernández-Moreno",
    author_email="iam.marcoshernandez@gmail.com",
    description="Biblioteca para modelos económicos en Python.",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    url="https://github.com/marcosjuniorhernandez/economy",
    
    project_urls={
        "Documentation": "https://oikos.readthedocs.io/en/latest/",
        "Source": "https://github.com/marcosjuniorhernandez/economy",
    },
    
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "License :: OSI Approved :: MIT License",
    ],

    keywords=[
        "economics",
        "macroeconomics",
        "economic-modeling",
        "symbolic-math",
        "economic-theory",
        "education",
    ],

    install_requires=[
        "numpy",
        "sympy",
        "scipy",
        "latex2sympy2",
        "ipython",
        "matplotlib",
        "rich"
    ],
    
    python_requires=">=3.8"
)