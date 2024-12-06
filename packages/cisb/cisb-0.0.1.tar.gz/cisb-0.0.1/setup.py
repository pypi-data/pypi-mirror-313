from setuptools import setup, find_packages

setup(
    name="cisb",
    version="0.0.1",
    packages=find_packages(),  # Automatically find relevant packages
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "asyncio",
        "diskcache",
    ],
    entry_points="""
        [console_scripts]
        cisb=cisb.cli:cli
    """,
)
