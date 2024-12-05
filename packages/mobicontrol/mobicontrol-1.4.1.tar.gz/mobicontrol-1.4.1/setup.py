from setuptools import setup

setup(
    name="mobicontrol",
    version="1.4.1",
    packages=["mobicontrol", "mobicontrol.cli", "mobicontrol.client"],
    include_package_data=True,
    install_requires=["Click", "requests", "PyYAML"],
    entry_points={"console_scripts": ["mc = mobicontrol.cli:mobicontrol"]},
)
