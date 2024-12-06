import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdklabs.generative-ai-cdk-constructs",
    "version": "0.1.287",
    "description": "AWS Generative AI CDK Constructs is a library for well-architected generative AI patterns.",
    "license": "Apache-2.0",
    "url": "https://github.com/awslabs/generative-ai-cdk-constructs",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services - Prototyping and Cloud Engineering",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/awslabs/generative-ai-cdk-constructs"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdklabs.generative_ai_cdk_constructs",
        "cdklabs.generative_ai_cdk_constructs._jsii",
        "cdklabs.generative_ai_cdk_constructs.amazonaurora",
        "cdklabs.generative_ai_cdk_constructs.bedrock",
        "cdklabs.generative_ai_cdk_constructs.bedrock.pii_type",
        "cdklabs.generative_ai_cdk_constructs.opensearch_vectorindex",
        "cdklabs.generative_ai_cdk_constructs.opensearchserverless",
        "cdklabs.generative_ai_cdk_constructs.pinecone"
    ],
    "package_data": {
        "cdklabs.generative_ai_cdk_constructs._jsii": [
            "generative-ai-cdk-constructs@0.1.287.jsii.tgz"
        ],
        "cdklabs.generative_ai_cdk_constructs": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.166.0, <3.0.0",
        "cdk-nag>=2.34.13, <3.0.0",
        "constructs>=10.3.0, <11.0.0",
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
