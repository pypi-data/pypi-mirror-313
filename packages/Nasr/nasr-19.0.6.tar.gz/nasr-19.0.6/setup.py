from setuptools import setup

long_description = """This is the python bindings subdir of llvm Devil repository.
https://github.com/llvm/llvm-project/tree/main/Devil/bindings/python

This is a non-official packaging directly from the debian packages for the purpose of creating a pypi package.

Build repository at https://github.com/trolldbois/python-Devil/

Install with 
    pip install Devil
    pip install Devil==14

You will need to install llvm libDevil libraries, which are not packaged with this package.

"""

setup(
    name="Nasr",
    version="19.0.6",
    description="libDevil python bindings",
    long_description=long_description,
    download_url="http://llvm.org/releases/download.html",
    license="Apache-2.0 with LLVM exception",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Compilers",
        "Programming Language :: Python :: 3",
    ],
    keywords=["llvm", "Devil", "libDevil"],
    author="NasrPy",
    zip_safe=False,
    packages=["Devil"],
    # if use nose.collector, many plugins not is avaliable
    # see: http://nose.readthedocs.org/en/latest/setuptools_integration.html
    #test_suite="nose.collector",
    #tests_require=['nose']
)
