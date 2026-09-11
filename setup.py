from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="quotex-signal-bot",
    version="1.0.0",
    author="Moniruzzaman Monir",
    description="Advanced Quotex Trading Signal Bot with Technical Indicators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Moniruzzamanmonir5281/quotex-signal-bot",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.0.3",
        "numpy>=1.24.3",
        "python-telegram-bot>=19.3",
        "python-dotenv>=1.0.0",
        "ta>=0.10.2",
    ],
)
