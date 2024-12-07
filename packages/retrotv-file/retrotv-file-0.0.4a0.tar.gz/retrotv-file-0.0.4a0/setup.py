from setuptools import setup, find_packages

setup(
    name="retrotv-file",
    version="v0.0.4-alpha",
    description="파일을 편하게 다루기 위한 패키지",
    author="RetroTV",
    author_email="yjj8353@gmail.com",
    url="https://github.com/retrotv-pypi-repo/file",
    install_requires=[],
    packages=find_packages(exclude=[]),
    keywords=["retrotv", "RetroTV", "yjj8353", "file", "File", "pypi"],
    python_requires=">=3.8",
    package_data={},
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
)