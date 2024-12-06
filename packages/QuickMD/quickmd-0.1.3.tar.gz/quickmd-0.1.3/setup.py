from setuptools import setup, find_packages

setup(
    name="QuickMD",
    version="0.1.3",
    description="Command Line Tool that quickly generates markdown files from your docstrings",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Jared T Ponting",
    author_email="jaredtponting@gmail.com",
    url="https://github.com/JaredTPonting/QuickMD",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "qmd=QuickMD.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">3.6"
)