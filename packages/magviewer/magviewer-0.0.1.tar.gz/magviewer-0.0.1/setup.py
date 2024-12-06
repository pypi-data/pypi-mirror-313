from importlib.metadata import entry_points

from setuptools import find_packages, setup

setup(
    name = "magviewer",
    version = "0.0.1",
    keywords = ("pip", "VASP", "noncolinear MAGMOM"),
    description = "ncl-MAGMOM viewer",
    long_description = "visulize the noncolinear magnetic moment for VASP",
    license = "MIT Licence",
    url = "https://gumijiong.github.io/",
    author = "GumiJiong",
    author_email = "Gaomouxu@outlook.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["numpy", "matplotlib", "scipy"],
    scripts = [],
    entry_points = {
        "console_scripts": [
            "mv-opt = MagViewer.viewer:view_opt",
            "mv-ecurve = MagViewer.viewer:view_Ecurve",
        ],
    },
)