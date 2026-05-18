from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="unifi_access",
    version="0.1.0",
    author="Travis Tucker",
    author_email="",
    description="A Python client for the UniFi Access API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/travis-tucker/unifi_access",
    project_urls={
        "Bug Tracker": "https://github.com/travis-tucker/unifi_access/issues",
        "Documentation": "https://github.com/travis-tucker/unifi_access",
        "Source Code": "https://github.com/travis-tucker/unifi_access",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Home Automation",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "httpx>=0.23.0",
        "python-dotenv>=1.0.0",
    ],
    python_requires=">=3.8",
    keywords="unifi access ubiquiti api client home-automation",
    license="MIT",
)