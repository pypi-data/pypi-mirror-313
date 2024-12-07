from setuptools import setup, find_packages

setup(
    name="prompt_evaluator",
    version="0.1.3",
    description="A package to evaluate prompts using OpenAI models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Akshay Ugale",
    author_email="akshay.ugale88@gmail.com",
    url="https://github.com/akshaytheau/prompt_evaluator",
    packages=find_packages(),
    install_requires=["openai"],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
