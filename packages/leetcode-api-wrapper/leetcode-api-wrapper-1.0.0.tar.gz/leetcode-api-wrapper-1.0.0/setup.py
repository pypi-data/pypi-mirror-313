from setuptools import setup, find_packages

setup(
    name="leetcode-api-wrapper",
    version="1.0.0",
    author="Aaditya Mehetre",
    author_email="aadityamehetre@icloud.com",
    description="Python wrapper for Alfa LeetCode API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/harbringe/pyleetcode",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
