from setuptools import setup, find_packages

setup(
    name="sanskrit-dictionary-scraper",
    version="1.0.1",
    author="Jagruti Airao",
    author_email="jagrutiairao04@gmail.com",
    description="A package to scrape Sanskrit dictionary data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/jagruti0403/sanskrit-dictionary-scraper",  # Update with your repository link
    packages=find_packages(),
    install_requires=[
        "selenium",
        "beautifulsoup4",
        "webdriver-manager"
    ],
    entry_points={
        "console_scripts": [
            "sanskrit-dictionary-scraper = sanskrit_scraper.scraper:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
