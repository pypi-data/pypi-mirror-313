from setuptools import setup
#run with python3 setup.py sdist bdist_wheel

with open("./README.md") as f:
    description = f.read()

with open("./requirements.txt", encoding="utf-16") as f:
    requirements = f.readlines()

setup(
    name = "fitting_toolkit",
    version = "1.0.1",
    package_dir={"": "src"},
    packages=[""],
    long_description=description,
    long_description_content_type="text/markdown",
    install_requires = requirements,
    project_urls = {
        "Documentation": "https://github.com/davidkowalk/fitting_toolkit/blob/development/docs/manual.md",
        "Source": "https://github.com/davidkowalk/fitting_toolkit/",
        "Tracker": "https://github.com/davidkowalk/fitting_toolkit/issues"
    },
    license="MIT",
    description="Easy and Flexible Curve Fitting",
    maintainer_email="david.kowalk@gmail.com",
    url="https://github.com/davidkowalk/fitting_toolkit/"
)