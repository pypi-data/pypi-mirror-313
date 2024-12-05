from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.7'
DESCRIPTION = 'eazyml image explain api'
LONG_DESCRIPTION = 'eazyml image explain api with linux and windows compatibility'

# Setting up
setup(
    name="eazyml-xai-image",
    version=VERSION,
    author="Eazyml",
    author_email="admin@ipsoftlabs.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_dir={"eazyml_xai_image":"./eazyml_xai_image"},
    package_data={'' : ['*.py', '*.so', '*.dylib', '*.pyd']},
    install_requires=['tensorflow',
                      'segmentation-models==1.0.1',
                      'lime',
                      ],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
