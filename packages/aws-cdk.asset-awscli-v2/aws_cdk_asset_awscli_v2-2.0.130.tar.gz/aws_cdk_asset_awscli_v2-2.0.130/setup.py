import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-cdk.asset-awscli-v2",
    "version": "2.0.130",
    "description": "An Asset construct that contains the AWS CLI, for use in Lambda Layers",
    "license": "Apache-2.0",
    "url": "https://github.com/cdklabs/awscdk-asset-awscli#readme",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdklabs/awscdk-asset-awscli.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.asset_awscli_v2",
        "aws_cdk.asset_awscli_v2._jsii"
    ],
    "package_data": {
        "aws_cdk.asset_awscli_v2._jsii": [
            "asset-awscli-v2@2.0.130.jsii.tgz"
        ],
        "aws_cdk.asset_awscli_v2": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.0.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.103.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<5.0.0"
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
