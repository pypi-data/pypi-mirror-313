from setuptools import setup, find_packages

setup(
    name="cisb",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
        "aiohttp>=3.10.5,<4",  # aiohttp with required version
        "aiohappyeyeballs>=2.3.0",  # Sub-dependency for aiohttp
        "aiosignal>=1.1.2",  # Sub-dependency for aiohttp
        "attrs>=17.3.0",  # Dependency for aiohttp
        "frozenlist>=1.1.1",  # Dependency for aiohttp
        "multidict>=4.5,<7.0",  # Dependency for aiohttp
        "yarl>=1.0,<2.0",  # Dependency for aiohttp
        "idna>=2.0",  # Dependency for yarl and requests
        "diskcache>=5.6.3",  # Dependency for caching
        "click>=8.1.7",  # CLI framework dependency
        "requests>=2.32.3,<3",  # HTTP requests library
        "certifi>=2017.4.17",  # Dependency for requests
        "charset-normalizer>=2,<4",  # Dependency for requests
        "urllib3>=1.21.1,<3",  # Dependency for requests
        "python-dateutil>=2.9.0",  # For handling dates
        "six>=1.5",  # Dependency for python-dateutil
        "PyYAML>=6.0.2",  # YAML parsing library
        "setuptools>=75.1.0",  # Needed for package setup
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
    },
    entry_points={
        "console_scripts": [
            "cisb=cisb.cli:cli",
        ],
    },
    description="GitLab Security Compliance CLI",
    long_description="A CLI tool for running GitLab security compliance checks.",
    keywords=["GitLab", "security", "compliance", "CIS benchmarks"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)