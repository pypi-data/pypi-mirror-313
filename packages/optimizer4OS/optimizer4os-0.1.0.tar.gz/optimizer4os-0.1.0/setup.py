from setuptools import setup, find_packages

setup(
    name="optimizer4OS",                  # Name of your library
    version="0.1.0",                    # Initial version
    author="Zhang Wusan",                 # Your name
    author_email="zhangwusan1@gmail.com",  # Your email
    description="Cross-platform optimizer system cleaner library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zhangwusan/optimizer",  # GitHub repo URL
    packages=find_packages(),           # Automatically discover all packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',            # Minimum Python version
    install_requires=[],                # External dependencies, if any
)