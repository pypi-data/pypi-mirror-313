from setuptools import setup, find_packages
import os

# 使用 UTF-8 编码读取 README.md
def read_readme():
    try:
        if os.path.exists("README.md"):
            with open("README.md", encoding='utf-8') as f:
                return f.read()
        return ""
    except Exception:
        return ""

setup(
    name="bib-watch",
    version="1.0.2",
    packages=find_packages(),
    install_requires=[
        'bibtexparser',
        'watchdog'
    ],
    entry_points={
        'console_scripts': [
            'bib-watch=bib.bib_watch:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A LaTeX bibliography manager that automatically organizes references",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/bibmanager",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)