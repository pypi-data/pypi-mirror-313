import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="langcode-turner",
    version="0.1.0",
    author="Feliks Peegel",
    author_email="felikspeegel@outlook.com",
    description="langcode turn, support iso 639-1, iso 639-2, iso 639-3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felikspeegel/langcode_turner",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)
