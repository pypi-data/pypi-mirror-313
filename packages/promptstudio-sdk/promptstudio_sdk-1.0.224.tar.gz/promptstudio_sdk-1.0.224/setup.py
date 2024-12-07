from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="promptstudio_sdk",
    version="1.0.224",
    author="PromptStudio",
    author_email="support@promptstudio.dev",
    description="A Python SDK for PromptStudio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/promptstudio-dev/promptstudio-sdk-python",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0",
        "openai>=1.0.0",
        "google-generativeai>=0.3.0",
        "fastapi",
    ],
)
