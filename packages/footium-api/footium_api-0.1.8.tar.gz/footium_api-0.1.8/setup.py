from setuptools import setup, find_packages

setup(
    name="footium_api",
    version="0.1.8",
    author="SohoJoe",
    description="python api for the footium game",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Sohojoe/footium_api",
    packages=find_packages(),
    install_requires=[
        "python-dotenv==1.0.1",
        "pycryptodome==3.20.0",
        "python-box==7.1.1",
        "gql==3.5.0",
        "requests_toolbelt==1.0.0",
        "eth-account==0.13.4",
        "pandas==2.2.2",
        "diskcache==5.6.3",
        "tenacity==9.0.0"
    ],
    extras_require={
        "dev": [
            "pre-commit==3.7.1",
            "black",
            "ruff",
            "codespell",
            "mypy",
            "nbqa",
            "types-requests",
            "pytest",
        ],
        "notebooks": [
            "jupyter", 
            "seaborn", 
        ],
    },
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
