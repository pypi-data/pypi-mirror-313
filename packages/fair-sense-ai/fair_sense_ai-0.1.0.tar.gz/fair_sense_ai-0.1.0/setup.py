from setuptools import setup, find_packages

setup(
    name="fair-sense-ai",  # Replace with your package name
    version="0.1.0",
    author="Shaina",
    author_email="your_email@example.com",
    description="A short description of fair-sense-ai",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    # url="https://github.com/yourusername/fair-sense-ai",  # Update with your repo
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
