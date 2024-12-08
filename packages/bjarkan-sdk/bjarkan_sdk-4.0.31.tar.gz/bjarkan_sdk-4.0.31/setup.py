from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="bjarkan-sdk",
        package_dir={"": "src"},
        packages=find_packages(where="src", exclude=["tests*", "scripts*"]),
        install_requires=[
            "ccxt>=4.1.13",
            "pydantic>=2.5.2",
            "loguru>=0.7.2",
            "python-dotenv>=1.0.0",
            "logtail-python>=0.2.5"
        ],
        extras_require={
            'dev': [
                'build',
                'twine',
                'black',
                'isort',
                'mypy',
                'pytest',
                'pytest-asyncio',
                'pytest-cov'
            ]
        }
    )
