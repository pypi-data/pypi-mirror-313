from setuptools import setup, find_packages

setup(
    name="latex_converter_itmo_223215",
    version="0.0.1a",
    description="Latex converter for ITMO",
    author="<Maxim Vukolov>",
    author_email="<example@gmail.com>",
    url="https://github.com/example",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "hw": ["picture.png"]
    }
)
