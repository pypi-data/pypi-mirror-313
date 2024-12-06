import os
from setuptools import setup, find_packages


VERSION = '0.0.17'
DESCRIPTION = 'eazyml cf api'
LONG_DESCRIPTION = 'eazyml cf api'

# Setting up
setup(
    name="eazyml-cf",
    version=VERSION,
    author="Eazyml",
    author_email="admin@ipsoftlabs.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    package_dir={"eazyml_cf":"./eazyml_cf"},
    package_data={'' : ['*.py', '*.so', '*.dylib', '*.pyd']},
    install_requires=['pandas',
                      'matplotlib',
                      'openpyxl',
                      'scikit-learn',
                      'scipy'
                      ],
    keywords=['python'],
    python_requires=">=3.8",
    url="https://eazyml.com/",
    project_urls={
        "Documentation": "https://eazyml.com/docs",
        "Homepage": "https://eazyml.com/"
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        # "Development Status :: 5 - Production/Stable",
        "License :: Other/Proprietary License",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
