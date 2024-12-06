import os
import re
import setuptools

scriptFolder = os.path.dirname(os.path.realpath(__file__))
os.chdir(scriptFolder)

# Find version info from module (without importing the module):
with open("src/BotniumPlus/__init__.py", "r", encoding="utf-8") as fileObj:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fileObj.read(), re.MULTILINE
    ).group(1)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="botnium-plus",
    version=version,
    author="QCYQ",
    author_email="devadmin@botnium.com",
    description="Python toolkits for RPA projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    test_suite='tests',
    install_requires=['pythonnet','typing_extensions'],
    include_package_data = True,
    url="https://www.botnium.com",
    project_urls={
        "Documentation": "https://www.botnium.com"
    },
    classifiers=[
        'Environment :: Win32 (MS Windows)',
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={
        '':['lib\*.dll','lib\lib\*.dll','lib\lib\*.sys','*.config','*.xml', '.locator\*.cnstore', '.locator\*\*.jpg']
    }
)