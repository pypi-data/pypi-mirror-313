import setuptools
from setuptools import find_packages

setuptools.setup(
    name="ankerautotrainsdk",
    version="0.25",
    description="Python Package Boilerplate",
    long_description=open("README.md").read().strip(),
    long_description_content_type="text/markdown",
    author="taco",
    python_requires=">=3.6",
    author_email="taco.wang@anker-in.com",
    url="",
    # py_modules=['sdk'],
    install_requires=[
        "requests==2.31.0",
        "pydantic==1.0",
        "Pillow==10.4.0",
        "moviepy==1.0.3",
        "pycryptodome==3.21.0",
    ],
    license="MIT License",
    zip_safe=False,
    keywords="",
    packages=find_packages(),
)
