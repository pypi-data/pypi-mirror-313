from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="github_username_validator",
    version="0.1.0",
    author="su21",
    author_email="santounyil21041998@gmail.com",
    description="Library untuk validasi username GitHub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imnoob59/github_username_validator",  # Ganti dengan URL repository
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],  # Tambahkan library yang dibutuhkan
    python_requires='>=3.6',
)