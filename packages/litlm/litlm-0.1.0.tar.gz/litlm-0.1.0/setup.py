from setuptools import setup

setup(
    name="litlm",
    version="0.1.0",
    description="Minimalist litellm wrapper for simpler requests and better openrouter support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Damien Sileo",
    url="https://github.com/sileod/litlm",
    py_modules=["litlm"],
    install_requires=[
        "litellm",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
)
