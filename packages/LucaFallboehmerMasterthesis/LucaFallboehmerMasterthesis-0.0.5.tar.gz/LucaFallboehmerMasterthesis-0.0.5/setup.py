import setuptools
import os
import pathlib
import re
import ast


# Function to read the value of a __magic__ variable from the __init__.py file
def read_from_init(name, base_dir):
    field_re = re.compile(r"__{}__\s+=\s+(.*)".format(re.escape(name)))
    path = os.path.join(base_dir, "__init__.py")
    line = field_re.search(pathlib.Path(path).read_text()).group(1)
    return ast.literal_eval(line)


# Base directory of the package
BASEDIR = os.path.dirname(os.path.realpath(__file__))

# Package configuration
setuptools.setup(
    name="LucaFallboehmerMasterthesis",
    author="Luca Fallböhmer",
    url="https://github.com/lucafally/masterthesis",
    author_email="luca.fallboehmer@tum.de",
    version=read_from_init("version", os.path.join(BASEDIR, "masterthesis")),
    description=read_from_init("description", os.path.join(BASEDIR, "masterthesis")),
    packages=setuptools.find_packages(
        where=".", exclude=["masterthesis.notebooks", "masterthesis.__pycache__"]
    ),
    python_requires=">=3.9",
    # install_requires=[
    #     "h5py==3.7.0",
    #     "iminuit==2.26.0",
    #     "matplotlib==3.6.0",
    #     "numpy==1.23.3",
    #     "pandas==1.5.0",
    #     "scipy==1.9.1",
    #     "seaborn==0.13.2",
    #     # "torch==2.4.0.dev20240523",
    #     "torch==2.3.1",
    #     "tqdm==4.65.0",
    # ],
    include_package_data=True,
    zip_safe=False,
)
