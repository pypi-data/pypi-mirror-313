import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "pharindoko.cdk-internal-gateway",
    "version": "1.4.26",
    "description": "CDK construct to create to create internal serverless applications.",
    "license": "Apache-2.0",
    "url": "https://github.com/pharindoko/cdk-internal-gateway.git",
    "long_description_content_type": "text/markdown",
    "author": "Florian Fuß",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/pharindoko/cdk-internal-gateway.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "pharindoko.cdk_internal_gateway",
        "pharindoko.cdk_internal_gateway._jsii"
    ],
    "package_data": {
        "pharindoko.cdk_internal_gateway._jsii": [
            "cdk-internal-gateway@1.4.26.jsii.tgz"
        ],
        "pharindoko.cdk_internal_gateway": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.78.0, <3.0.0",
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
