from setuptools import find_packages, setup


APP = ["src/checkbook_helper/__main__.py"]
OPTIONS = {
    "argv_emulation": True,
    "packages": ["checkbook_helper"],
}

setup(
    name="checkbook-helper",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages("src"),
    app=APP,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
