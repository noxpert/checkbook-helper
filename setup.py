from setuptools import find_packages, setup


APP = ["src/checkbook_helper/__main__.py"]
OPTIONS = {
    "argv_emulation": True,
    "packages": ["checkbook_helper"],
    "includes": [
        "tkinter",
        "tkinter.ttk",
        "tkinter.font",
        "tkinter.messagebox",
    ],
    "plist": {
        "CFBundleName": "checkbook-helper",
        "CFBundleDisplayName": "checkbook-helper",
        "CFBundleIdentifier": "com.matthew.checkbook-helper",
        "CFBundleShortVersionString": "0.1.0",
        "CFBundleVersion": "0.1.0",
    },
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
