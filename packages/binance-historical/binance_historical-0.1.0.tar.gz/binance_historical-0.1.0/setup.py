import platform
from setuptools import setup, find_packages

extras_require = {
    "windows": ["winloop"], 
    "non_windows": ["uvloop"],
}

if platform.system() == "Windows":
    event_loop_requirements = extras_require["windows"]
else:
    event_loop_requirements = extras_require["non_windows"]

setup(
    name="binance_historical",
    version="0.1.0",
    description="A package for interacting with Binance historical data",
    author="Tapanhaz",
    url="https://github.com/Tapanhaz/binance_historical",
    packages=["binance_historical"],
    package_dir={"": "."},
    install_requires=[
        "aiohttp",
        "tqdm",
        "polars",
        "aiolimiter",
        "pandas",
        "pyarrow",
        "python-dateutil",
    ] + event_loop_requirements, 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
