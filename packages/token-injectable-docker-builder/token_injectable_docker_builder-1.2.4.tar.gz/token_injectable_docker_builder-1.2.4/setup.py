import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "token-injectable-docker-builder",
    "version": "1.2.4",
    "description": "The TokenInjectableDockerBuilder is a flexible AWS CDK construct that enables the usage of AWS CDK tokens in the building, pushing, and deployment of Docker images to Amazon Elastic Container Registry (ECR). It leverages AWS CodeBuild and Lambda custom resources.",
    "license": "MIT",
    "url": "https://github.com/AlexTech314/TokenInjectableDockerBuilder.git",
    "long_description_content_type": "text/markdown",
    "author": "AlexTech314<alest314@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/AlexTech314/TokenInjectableDockerBuilder.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "token_injectable_docker_builder",
        "token_injectable_docker_builder._jsii"
    ],
    "package_data": {
        "token_injectable_docker_builder._jsii": [
            "token-injectable-docker-builder@1.2.4.jsii.tgz"
        ],
        "token_injectable_docker_builder": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.166.0, <3.0.0",
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
