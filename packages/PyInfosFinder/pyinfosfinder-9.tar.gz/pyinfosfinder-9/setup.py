from setuptools import setup, find_packages

setup(
    name="PyInfosFinder",
    version="1",  # This will be updated by the script
    description="A Python package that can get information.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="EuroMH",
    author_email="bypassfdp1501@gmail.com",
    url="https://github.com/EuroMH/PyMalWare",
    packages=find_packages(where="src"),  # Specifies that packages are in the 'src' directory
    package_dir={"": "src"},  # Tells setuptools to look for the packages inside 'src'
    include_package_data=True,  # To include files like LICENSE.txt if needed
    install_requires=[
        "requests",
        "psutil",
        "pycryptodome",
        "pywin32",
        "base64",
        "platform",
        "sqlite3",
        "shutil",
        "datetime",
        "re",
        "os",
        "subprocess",
        "json",
        "tempfile",
        "win32crypt",
        "crypto.Cipher",
        "time",
        "sys"
    ],
    extras_require={
        "dev": ["check-manifest"],
        "test": ["coverage"]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.12",
)
