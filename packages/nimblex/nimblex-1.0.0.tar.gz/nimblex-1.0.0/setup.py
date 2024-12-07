from setuptools import setup, find_packages

setup(
    name="nimblex",  # Updated package name
    version="1.0.0",  # Increment for new versions
    description="nimblex: A CLI tool to explore and extract project structures.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pezhvak98/Nimblex",  # Your project's GitHub repo URL
    author="Pezhvak",
    author_email="m.8562.m@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords="CLI, project-structure, code-exploration",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "rich",
        "termcolor",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "nimblex=nimblex.cli:main",
        ],
    },
    python_requires=">=3.7",
    project_urls={
        "Bug Reports": "https://github.com/pezhvak98/Nimblex/issues",
        "Source": "https://github.com/pezhvak98/Nimblex",
    },
)
