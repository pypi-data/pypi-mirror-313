import setuptools

try:
    from pip.req import parse_requirements
except ImportError:  # pip >= 10.0.0
    from pip._internal.req import parse_requirements

# TODO: mm - twine benutzen https://pypi.org/project/twine/
#
# Kurzanleitung
#    https://medium.com/@joel.barmettler/how-to-upload-your-python-package-to-pypi-65edc5fe9c56


parsed_reqs = parse_requirements('requirements.txt', session='hack')
installed_reqs = [str(ir.requirement) for ir in parsed_reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='processcube_sdk',
    version=setuptools.sic('5.0.3-alpha.1'),
    author="5Minds IT-Solutions GmbH & Co. KG",
    author_email="processcube@5minds.de",
    description="Some tools and defaults to program for the ProcessCube.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="sdk processcube bpmm external-tasks process-management etw",
    url="https://github.com/5minds/processcube_sdk.py",
    packages=setuptools.find_packages(),
    install_requires=installed_reqs,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
