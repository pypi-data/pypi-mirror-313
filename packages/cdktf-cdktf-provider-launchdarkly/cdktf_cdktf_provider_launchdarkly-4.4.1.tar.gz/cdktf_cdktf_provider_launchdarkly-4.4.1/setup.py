import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktf-cdktf-provider-launchdarkly",
    "version": "4.4.1",
    "description": "Prebuilt launchdarkly Provider for Terraform CDK (cdktf)",
    "license": "MPL-2.0",
    "url": "https://github.com/cdktf/cdktf-provider-launchdarkly.git",
    "long_description_content_type": "text/markdown",
    "author": "HashiCorp",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdktf/cdktf-provider-launchdarkly.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktf_cdktf_provider_launchdarkly",
        "cdktf_cdktf_provider_launchdarkly._jsii",
        "cdktf_cdktf_provider_launchdarkly.access_token",
        "cdktf_cdktf_provider_launchdarkly.audit_log_subscription",
        "cdktf_cdktf_provider_launchdarkly.custom_role",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_audit_log_subscription",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_environment",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_feature_flag",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_feature_flag_environment",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_flag_trigger",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_metric",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_project",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_relay_proxy_configuration",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_segment",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_team",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_team_member",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_team_members",
        "cdktf_cdktf_provider_launchdarkly.data_launchdarkly_webhook",
        "cdktf_cdktf_provider_launchdarkly.destination",
        "cdktf_cdktf_provider_launchdarkly.environment",
        "cdktf_cdktf_provider_launchdarkly.feature_flag",
        "cdktf_cdktf_provider_launchdarkly.feature_flag_environment",
        "cdktf_cdktf_provider_launchdarkly.flag_trigger",
        "cdktf_cdktf_provider_launchdarkly.metric",
        "cdktf_cdktf_provider_launchdarkly.project",
        "cdktf_cdktf_provider_launchdarkly.provider",
        "cdktf_cdktf_provider_launchdarkly.relay_proxy_configuration",
        "cdktf_cdktf_provider_launchdarkly.segment",
        "cdktf_cdktf_provider_launchdarkly.team",
        "cdktf_cdktf_provider_launchdarkly.team_member",
        "cdktf_cdktf_provider_launchdarkly.team_role_mapping",
        "cdktf_cdktf_provider_launchdarkly.webhook"
    ],
    "package_data": {
        "cdktf_cdktf_provider_launchdarkly._jsii": [
            "provider-launchdarkly@4.4.1.jsii.tgz"
        ],
        "cdktf_cdktf_provider_launchdarkly": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "cdktf>=0.20.0, <0.21.0",
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
