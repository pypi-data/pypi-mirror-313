from setuptools import setup, find_packages

setup(
    name="messaging-py-sdk",
    version="2.1.2",
    description="A Python SDK for managing messages and contacts, with webhook integration.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Amirul Islam",
    author_email="amirulislamalmamun@gmail.com",
    url="https://github.com/shiningflash/messaging-sdk",
    project_urls={
        "Documentation": "https://github.com/shiningflash/messaging-sdk/blob/main/README.md",
        "Source Code": "https://github.com/shiningflash",
        "Issue Tracker": "https://github.com/shiningflash/messaging-sdk/issues",
    },
    packages=find_packages(where="src"),  # Discover packages under "src"
    package_dir={"": "src"},             # Specify that all packages live under "src"
    include_package_data=True,           # Include non-Python files specified in MANIFEST.in
    install_requires=[
        "requests",
        "python-dotenv",
        "pytest",
        "pytest-mock",
        "flake8",
        "black",
        "mypy",
        "pydantic",
        "pytest-cov",
        "fastapi",
        "uvicorn",
        "pytest-asyncio",
        "httpx",
        "pydantic-settings",
    ],
    extras_require={
        "dev": [
            "flake8",
            "black",
            "mypy",
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
            "pytest-mock",
        ],
    },
    entry_points={
        "console_scripts": [],
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="messaging sdk python api contacts",
    license="Apache",
    python_requires=">=3.8",
    zip_safe=False,
)
