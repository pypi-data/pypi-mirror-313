# setup.py
from setuptools import setup, find_packages

setup(
    name="Nasiwak",            # Your package name
    version="0.1.7",             # Initial version
    author="Nasiwak Team",
    author_email="Kushalnasiwak@outlook.com",
    description="A model that contains all the needs of Nasiwak Company Developers",
    packages=find_packages(),    # Automatically discover all packages in the module
    install_requires=[
        "selenium >= 4.26.0",
        "pyautogui >= 0.9.54",
        ],         # Dependencies (add here if your code depends on other packages)
    license="MIT",
)