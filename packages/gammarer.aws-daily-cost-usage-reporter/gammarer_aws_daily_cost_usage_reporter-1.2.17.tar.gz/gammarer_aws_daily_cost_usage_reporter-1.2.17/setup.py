import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "gammarer.aws-daily-cost-usage-reporter",
    "version": "1.2.17",
    "description": "Cost & Usage Reports",
    "license": "Apache-2.0",
    "url": "https://github.com/gammarers/aws-daily-cost-usage-reporter.git",
    "long_description_content_type": "text/markdown",
    "author": "yicr<yicr@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/gammarers/aws-daily-cost-usage-reporter.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "gammarer.aws_daily_cost_usage_reporter",
        "gammarer.aws_daily_cost_usage_reporter._jsii"
    ],
    "package_data": {
        "gammarer.aws_daily_cost_usage_reporter._jsii": [
            "aws-daily-cost-usage-reporter@1.2.17.jsii.tgz"
        ],
        "gammarer.aws_daily_cost_usage_reporter": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.80.0, <3.0.0",
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
