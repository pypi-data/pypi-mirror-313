from setuptools import setup, find_packages

setup(
    name="pygemnts",
    version="89.0.1",
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
    python_requires='>=3.6',
    author="Your Name",
    author_email="your.email@example.com",
    description="Python syntax highlighting library",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://pypi.org/project/pygemnts",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)