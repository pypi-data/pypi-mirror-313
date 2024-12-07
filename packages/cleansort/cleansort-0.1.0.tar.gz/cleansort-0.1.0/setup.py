from setuptools import setup, find_packages

setup(
    name="cleansort",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'pandas>=1.5.0',
        'sqlalchemy>=2.0.0',
        'beautifulsoup4>=4.9.3',
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for cleaning and sorting metadata",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/cleansort",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)