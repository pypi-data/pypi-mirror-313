from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [
        line.strip() for line in fh if line.strip() and not line.startswith("#")
    ]


setup(
    name="CodeAss",
    version="0.13.2",
    author="HullaBulla",
    author_email="hullabulla666@gmail.com",
    description="Code Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=[],
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.10",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points="""
        [console_scripts]
        ca=codeassistant.main:cli
    """,
)
