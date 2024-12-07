from setuptools import *

rst = open(".\\README.rst", mode='r', encoding = 'UTF-8').read()

setup(
    name = "pdf_docx_pic",
    version = "4.1.0.20241207",
    packages = find_packages(),
    python_requires = ">=3.10, <=3.12",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8.1",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: Chinese (Simplified)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Typing :: Typed",
    ],
    install_requires = [
        "ttkbootstrap>=1.10, <1.11",
        "pdf2docx>=0.5.5, <0.6",
        "docx2pdf>=0.1.7, <0.2",
        "PyMuPDF>=1.24.1, <1.26",
        "Pillow>=10, <12",
    ],
    long_description = rst
)
