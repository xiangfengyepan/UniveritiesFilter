from setuptools import setup, find_packages

setup(
    name="UniversitiesFilter",  # Name of the package
    version="0.1.0",  # Initial release version
    author="Xiang Feng Ye Pan",
    description="Filter of the degrees in catalunya",
    long_description=open("README.md").read(),  # Detailed description (usually README.md)
    long_description_content_type="text/markdown",  # Type of the long description (Markdown)
    url="https://github.com/xiangfengyepan/UniversitiesFilter",  # URL of the project repository
    packages=find_packages(),  # Automatically discover packages in the current directory
    classifiers=[
        "Programming Language :: Python :: 3",  # Python version support
        "License :: OSI Approved :: MIT License",  # License type
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version required
    install_requires=[
        # List your dependencies here
        "requests",
        "numpy",
    ],
    entry_points={
        'console_scripts': [
            'your_command=your_module:main_function',  # Command-line interface entry
        ],
    },
)
