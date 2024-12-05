from setuptools import setup, find_packages

setup(
    name="helper_decorators",
    version="0.1.2",
    author="Kavinda Kobbekaduwe",
    author_email="kavindakobbekaduwe@gmail.com",  # Replace with your email
    description="Python decorator functions for regular use.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kavinda-kobbekaduwe/helper_decorators",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
