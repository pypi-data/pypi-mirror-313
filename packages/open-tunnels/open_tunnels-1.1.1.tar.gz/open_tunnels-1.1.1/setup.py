from setuptools import setup, find_packages

setup(
    name="open_tunnels",  # Name of your project
    version="1.1.1",  # Initial version
    author="Sandesh Kumar",
    author_email="connect@sandeshai.in",
    description="A perfect solution for tunnelling hosts to internet",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={ '': ['templates/*'], 
                   },
    python_requires=">=3.10",  # Minimum Python version
    install_requires=open("requirements.txt").readlines(),  # Dependencies
)
