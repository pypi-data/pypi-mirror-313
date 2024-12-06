import os
import shutil

import setuptools
from setuptools.command.sdist import sdist
from wheel.bdist_wheel import bdist_wheel

with open("README.md", "r") as fh:
    long_description = fh.read()


def clean_folders():
    print("Removing temporary folders.")

    TMP_FOLDERS = ["dakiya.egg-info"]
    for folder in TMP_FOLDERS:
        if os.path.exists(folder):
            shutil.rmtree(folder)


class SdistCommand(sdist):
    """Custom build command."""

    def run(self):
        sdist.run(self)
        clean_folders()


class BdistWheelCommand(bdist_wheel):
    """Custom build command."""

    def run(self):
        bdist_wheel.run(self)
        clean_folders()


setuptools.setup(
    name="dakiya",
    version="1.1",
    author="Shamail Tayyab",
    author_email="tayyab.shamail@gmail.com",
    description="Relay Communcation via Nitro's Communication Hub",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    # url="https://github.com/username/password_extractor_by_name_using_py-passbolt.",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    cmdclass={"sdist": SdistCommand, "bdist_wheel": BdistWheelCommand},
)
