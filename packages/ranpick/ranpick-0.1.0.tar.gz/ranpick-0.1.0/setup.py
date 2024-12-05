import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ranpick",
    version="0.1.0",
    author="rainy58",
    author_email="yhg4908@kakao.com",
    description="A high-entropy random number generation library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yhg4908/ranpick.py",
    project_urls={
        "Bug Tracker": "https://github.com/yhg4908/ranpick.py/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)