from setuptools import setup, find_packages

setup(
    name="oj-bz.sh",  # Replace with your package name
    version="0.1.0",
    description="binary pacages for lambda ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="oj-bz",
    author_email="osherbg@gmail.com",
    url="https://github.com/eldiabloj/osher-aws-project-int.git",  # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Replace with your minimum Python version

)
