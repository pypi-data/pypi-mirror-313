import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws-data-landing-zone",
    "version": "0.0.40",
    "description": "AWS CDK Data Landing Zone construct",
    "license": "Apache-2.0",
    "url": "https://github.com/DataChefHQ/aws-data-landing-zone.git",
    "long_description_content_type": "text/markdown",
    "author": "DataChefHQ<hi@datachef.co>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/DataChefHQ/aws-data-landing-zone.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_data_landing_zone",
        "aws_data_landing_zone._jsii"
    ],
    "package_data": {
        "aws_data_landing_zone._jsii": [
            "aws-data-landing-zone@0.0.40.jsii.tgz"
        ],
        "aws_data_landing_zone": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.133.0, <3.0.0",
        "cdk_express_pipeline>=1.0.2, <2.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.104.0, <2.0.0",
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
