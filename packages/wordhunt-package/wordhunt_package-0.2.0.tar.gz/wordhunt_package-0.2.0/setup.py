from setuptools import setup, find_packages

setup(
    name="wordhunt_package",
    version="0.2.0",
    author="Jeffrey Kim",
    author_email="jkjeffrey7@gmail.com",
    description="Type \"wordhunt\" and enter your Wordhunt board to get all possible words in Wordhunt!",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jeffreykim/wordhunt-bot",
    packages=find_packages(),
    package_data={
        'wordhunt_package': ['data/english.json'],  # Include all .json files in the 'data' folder
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "wordhunt=wordhunt_package.solver:run",
        ],
    },
)