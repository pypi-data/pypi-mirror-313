import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="petkit_api",
    version="0.1.6",
    author="Jezza34000",
    author_email="mail@me.org",
    description="Python library for PetKit's API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jezza34000/petkit-api",
    keywords="petkit, eversweet 3 pro, feeder mini, d4, petkit feeder, petkit water fountain, freshelement solo, pura x, pura max, pura air, purobot, eversweet max, pura max 2, yumshare dual hopper",
    packages=setuptools.find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "aiohttp>=3.8.1",
        "tzlocal>=4.2",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={  # Optional
        "Bug Reports": "https://github.com/Jezza34000/petkit-api/issues",
        "Source": "https://github.com/Jezza34000/petkit-api",
    },
)
