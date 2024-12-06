import setuptools


# Function to parse requirements.txt
def parse_requirements(filename: str) -> list[str]:
    with open(filename, "r") as f:
        return f.read().splitlines()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chronos-context-timer",
    version="1.0.0",
    author="Adam Birds",
    author_email="adam.birds@adbwebdesigns.co.uk",
    description="Chronos: A Python library for advanced task timing with features like distributed timing, batch timing, real-time visualization, and debugging-friendly timers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/adambirds/chronos",
    project_urls={
        "Bug Tracker": "https://github.com/adambirds/chronos/issues",
    },
    license="LGPLv3",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    package_dir={"chronos": "src/chronos"},
    packages=["chronos"],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=parse_requirements("requirements/prod.txt"),
)
