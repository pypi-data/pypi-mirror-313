import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "scotthsieh_projen_statemachine",
    "version": "2.0.580",
    "description": "An example construct for deploying to npm, PyPi, Maven, and Nuget with Amazon API Gateway and AWS Step Functions.",
    "license": "Apache-2.0",
    "url": "https://github.com/HsiehShuJeng/projen-simple.git",
    "long_description_content_type": "text/markdown",
    "author": "Shu-Jeng Hsieh",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/HsiehShuJeng/projen-simple.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "scotthsieh_projen_statemachine",
        "scotthsieh_projen_statemachine._jsii"
    ],
    "package_data": {
        "scotthsieh_projen_statemachine._jsii": [
            "projen-statemachine-example@2.0.580.jsii.tgz"
        ],
        "scotthsieh_projen_statemachine": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.27.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.105.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<4.3.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
