import setuptools
from setuptools import find_packages

setuptools.setup(name='ankerautotrainsdk',
                 version="0.20",
                 description='Python Package Boilerplate',
                 long_description=open('README.md').read().strip(),
                 long_description_content_type="text/markdown",
                 author='taco',
                 author_email='taco.wang@anker-in.com',
                 url='',
                 # py_modules=['sdk'],
                 install_requires=["requests==2.31.0", "pydantic==2.9.2", "Pillow==10.4.0", "moviepy==1.0.3", "pycryptodome==3.21.0"],
                 license='MIT License',
                 zip_safe=False,
                 keywords='',
                 packages=find_packages()
)