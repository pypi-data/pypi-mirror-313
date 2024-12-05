import setuptools
import subprocess
import re


with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    process = subprocess.Popen(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    version = output.decode("utf-8").strip()
    version_strict = re.match(r"^\d+\.\d+\.\d+$", version)
    if not version_strict:
        version = re.match(r"(\d+\.\d+\.\d+)-\d+-g\w+$", version).group(1)
except Exception as e:
    version = "0.0.0"

setuptools.setup(
    name="diamond-shovel-api",
    version=version,
    license="AGPL-3.0",
    author="Diamond Shovel Development Team",
    author_email="diamondshovel@cyberspike.top",
    description="A tool for asset scanning and vulnerability discovery, but plugin API part",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.cyberspike.top/tools/diamond_shovel",
    packages=setuptools.find_packages(),
    keywords=["api", "plugin", "diamond_shovel", "security"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ],
    python_requires='>=3.6',
    install_requires=[
        "kink",
        "pymongo",
        "flask",
        "requests",
        "geopy"
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
    ]
)