from setuptools import setup, find_packages

setup(
    name="haplostat",  # Replace with your package name
    version="0.4.0",  # Increment version after adding new features
    description="A package for handling HLA-related tasks with Selenium WebDriver integration",
    long_description=open("README.md").read(),  # Load README for PyPI
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/haplo-package",  # Replace with your repo or website
    packages=find_packages(),  # Automatically find all packages in your project
    install_requires=[
        "flask>=2.0.0",  # Flask for API
        "selenium>=4.0.0",  # Selenium for WebDriver automation
        "bs4>=0.0.1",  # BeautifulSoup for HTML parsing
        "requests>=2.26.0",  # Requests for HTTP handling (optional for downloading WebDriver)
        "webdriver-manager>=3.8.5"  # WebDriver Manager to simplify driver setup
    ],
    python_requires=">=3.6",  # Specify the supported Python version
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,  # Include additional files like WebDriver binaries
    entry_points={
        "console_scripts": [
            "haplo-cli=haplo.main:run_convert_hla",  # CLI entry point (optional)
        ]
    },
    package_data={
        "haplo": [
            "drivers/*",  # Include bundled WebDriver binaries if needed
        ],
    },
)
