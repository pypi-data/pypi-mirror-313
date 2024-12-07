import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-cr-constructs",
    "version": "2.1.647",
    "description": "aws cdk library for custom resource constructs.",
    "license": "Apache-2.0",
    "url": "https://github.com/neilkuan/cdk-cr-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Neil Kuan<guan840912@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/neilkuan/cdk-cr-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cr_constructs",
        "cdk_cr_constructs._jsii"
    ],
    "package_data": {
        "cdk_cr_constructs._jsii": [
            "cdk-cr-constructs@2.1.647.jsii.tgz"
        ],
        "cdk_cr_constructs": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.139.1, <3.0.0",
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
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
