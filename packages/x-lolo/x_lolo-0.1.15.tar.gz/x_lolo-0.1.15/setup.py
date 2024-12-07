from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="x_lolo",
    version="0.1.15",
    author="lolo skiiii",
    author_email="uha22211@gmail.com",
    description="A Python library for direct interaction with Twitter's unofficial API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mohaskii/x_lolo_project",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",  # Pour le scraping
        "Topic :: Internet",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "Natural Language :: English"
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "bs4",
        "brotli",
        "zstandard",
        "PyYAML"
    ],
)