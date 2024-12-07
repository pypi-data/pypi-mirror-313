r'''
# CDKTF prebuilt bindings for launchdarkly/launchdarkly provider version 2.21.2

This repo builds and publishes the [Terraform launchdarkly provider](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs) bindings for [CDK for Terraform](https://cdk.tf).

## Available Packages

### NPM

The npm package is available at [https://www.npmjs.com/package/@cdktf/provider-launchdarkly](https://www.npmjs.com/package/@cdktf/provider-launchdarkly).

`npm install @cdktf/provider-launchdarkly`

### PyPI

The PyPI package is available at [https://pypi.org/project/cdktf-cdktf-provider-launchdarkly](https://pypi.org/project/cdktf-cdktf-provider-launchdarkly).

`pipenv install cdktf-cdktf-provider-launchdarkly`

### Nuget

The Nuget package is available at [https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Launchdarkly](https://www.nuget.org/packages/HashiCorp.Cdktf.Providers.Launchdarkly).

`dotnet add package HashiCorp.Cdktf.Providers.Launchdarkly`

### Maven

The Maven package is available at [https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-launchdarkly](https://mvnrepository.com/artifact/com.hashicorp/cdktf-provider-launchdarkly).

```
<dependency>
    <groupId>com.hashicorp</groupId>
    <artifactId>cdktf-provider-launchdarkly</artifactId>
    <version>[REPLACE WITH DESIRED VERSION]</version>
</dependency>
```

### Go

The go package is generated into the [`github.com/cdktf/cdktf-provider-launchdarkly-go`](https://github.com/cdktf/cdktf-provider-launchdarkly-go) package.

`go get github.com/cdktf/cdktf-provider-launchdarkly-go/launchdarkly/<version>`

Where `<version>` is the version of the prebuilt provider you would like to use e.g. `v11`. The full module name can be found
within the [go.mod](https://github.com/cdktf/cdktf-provider-launchdarkly-go/blob/main/launchdarkly/go.mod#L1) file.

## Docs

Find auto-generated docs for this provider here:

* [Typescript](./docs/API.typescript.md)
* [Python](./docs/API.python.md)
* [Java](./docs/API.java.md)
* [C#](./docs/API.csharp.md)
* [Go](./docs/API.go.md)

You can also visit a hosted version of the documentation on [constructs.dev](https://constructs.dev/packages/@cdktf/provider-launchdarkly).

## Versioning

This project is explicitly not tracking the Terraform launchdarkly provider version 1:1. In fact, it always tracks `latest` of `~> 2.13` with every release. If there are scenarios where you explicitly have to pin your provider version, you can do so by [generating the provider constructs manually](https://cdk.tf/imports).

These are the upstream dependencies:

* [CDK for Terraform](https://cdk.tf)
* [Terraform launchdarkly provider](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2)
* [Terraform Engine](https://terraform.io)

If there are breaking changes (backward incompatible) in any of the above, the major version of this project will be bumped.

## Features / Issues / Bugs

Please report bugs and issues to the [CDK for Terraform](https://cdk.tf) project:

* [Create bug report](https://cdk.tf/bug)
* [Create feature request](https://cdk.tf/feature)

## Contributing

### Projen

This is mostly based on [Projen](https://github.com/projen/projen), which takes care of generating the entire repository.

### cdktf-provider-project based on Projen

There's a custom [project builder](https://github.com/cdktf/cdktf-provider-project) which encapsulate the common settings for all `cdktf` prebuilt providers.

### Provider Version

The provider version can be adjusted in [./.projenrc.js](./.projenrc.js).

### Repository Management

The repository is managed by [CDKTF Repository Manager](https://github.com/cdktf/cdktf-repository-manager/).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

__all__ = [
    "access_token",
    "audit_log_subscription",
    "custom_role",
    "data_launchdarkly_audit_log_subscription",
    "data_launchdarkly_environment",
    "data_launchdarkly_feature_flag",
    "data_launchdarkly_feature_flag_environment",
    "data_launchdarkly_flag_trigger",
    "data_launchdarkly_metric",
    "data_launchdarkly_project",
    "data_launchdarkly_relay_proxy_configuration",
    "data_launchdarkly_segment",
    "data_launchdarkly_team",
    "data_launchdarkly_team_member",
    "data_launchdarkly_team_members",
    "data_launchdarkly_webhook",
    "destination",
    "environment",
    "feature_flag",
    "feature_flag_environment",
    "flag_trigger",
    "metric",
    "project",
    "provider",
    "relay_proxy_configuration",
    "segment",
    "team",
    "team_member",
    "team_role_mapping",
    "webhook",
]

publication.publish()

# Loading modules to ensure their types are registered with the jsii runtime library
from . import access_token
from . import audit_log_subscription
from . import custom_role
from . import data_launchdarkly_audit_log_subscription
from . import data_launchdarkly_environment
from . import data_launchdarkly_feature_flag
from . import data_launchdarkly_feature_flag_environment
from . import data_launchdarkly_flag_trigger
from . import data_launchdarkly_metric
from . import data_launchdarkly_project
from . import data_launchdarkly_relay_proxy_configuration
from . import data_launchdarkly_segment
from . import data_launchdarkly_team
from . import data_launchdarkly_team_member
from . import data_launchdarkly_team_members
from . import data_launchdarkly_webhook
from . import destination
from . import environment
from . import feature_flag
from . import feature_flag_environment
from . import flag_trigger
from . import metric
from . import project
from . import provider
from . import relay_proxy_configuration
from . import segment
from . import team
from . import team_member
from . import team_role_mapping
from . import webhook
