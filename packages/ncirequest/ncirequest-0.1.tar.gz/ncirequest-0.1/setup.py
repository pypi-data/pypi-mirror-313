from setuptools import setup, find_packages

setup(
    name="ncirequest",
    version="0.1",
    description="A package for handling web scraping with retries, user-agent rotation, and proxy support",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "cloudscraper",
        "selenium",
        "webdriver-manager",
        "seleniumbase",
        "beautifulsoup4",
        "tenacity",
        "playwright",
        "fake-useragent"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
