r'''
# `launchdarkly_audit_log_subscription`

Refer to the Terraform Registry for docs: [`launchdarkly_audit_log_subscription`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription).
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

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class AuditLogSubscription(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.auditLogSubscription.AuditLogSubscription",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription launchdarkly_audit_log_subscription}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        config: typing.Mapping[builtins.str, builtins.str],
        integration_key: builtins.str,
        name: builtins.str,
        on: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        statements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AuditLogSubscriptionStatements", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription launchdarkly_audit_log_subscription} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param config: The set of configuration fields corresponding to the value defined for ``integration_key``. Refer to the ``formVariables`` field in the corresponding ``integrations/<integration_key>/manifest.json`` file in `this repo <https://github.com/launchdarkly/integration-framework/tree/master/integrations>`_ for a full list of fields for the integration you wish to configure. **IMPORTANT**: Please note that Terraform will only accept these in snake case, regardless of the case shown in the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#config AuditLogSubscription#config}
        :param integration_key: The integration key. Supported integration keys are ``chronosphere``, ``cloudtrail``, ``datadog``, ``dynatrace``, ``elastic``, ``grafana``, ``honeycomb``, ``kosli``, ``last9``, ``logdna``, ``msteams``, ``new-relic-apm``, ``signalfx``, ``slack``, and ``splunk``. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#integration_key AuditLogSubscription#integration_key}
        :param name: A human-friendly name for your audit log subscription viewable from within the LaunchDarkly Integrations page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#name AuditLogSubscription#name}
        :param on: Whether or not you want your subscription enabled, i.e. to actively send events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#on AuditLogSubscription#on}
        :param statements: statements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#statements AuditLogSubscription#statements}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#id AuditLogSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#tags AuditLogSubscription#tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__411f1d0cc53fb5844b8519f71316b59e6c298594e900f01df5aa9adb42d72a9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = AuditLogSubscriptionConfig(
            config=config,
            integration_key=integration_key,
            name=name,
            on=on,
            statements=statements,
            id=id,
            tags=tags,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a AuditLogSubscription resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AuditLogSubscription to import.
        :param import_from_id: The id of the existing AuditLogSubscription that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AuditLogSubscription to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e2178d972de561c6e0e19d7a939e5e9ec8becbe13a692471ade66625a0cdd0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putStatements")
    def put_statements(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AuditLogSubscriptionStatements", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b09593dc48451cac7e1de804b7017af1f32c84353b22b5c4c0e47132d112d4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStatements", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="statements")
    def statements(self) -> "AuditLogSubscriptionStatementsList":
        return typing.cast("AuditLogSubscriptionStatementsList", jsii.get(self, "statements"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationKeyInput")
    def integration_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="onInput")
    def on_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onInput"))

    @builtins.property
    @jsii.member(jsii_name="statementsInput")
    def statements_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditLogSubscriptionStatements"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditLogSubscriptionStatements"]]], jsii.get(self, "statementsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "config"))

    @config.setter
    def config(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd93333e753af3e942674e8d35eb2bd562b2c17b91987e17175e5afe70e988de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2d84a7846d6946c2c7e9910b45f406f96501fb19190e96f24154d42eafb0d44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationKey")
    def integration_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationKey"))

    @integration_key.setter
    def integration_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56df65820b16507c6d5b07dc336b9299278931508a997f928c79bb7b2c8eb391)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d44d580c2023e22496c87a2ff72b8b489a25e7b4bb129e87f94d47b15ccf22d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="on")
    def on(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "on"))

    @on.setter
    def on(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8677ea16381901f65d55b725f90b48f7b45956a0f95d13506f39ec151ce8ce39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "on", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ba6d47af38d7ff21f51dabc547973ed76fd65bf7e786ae53a1ca9f9637663f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.auditLogSubscription.AuditLogSubscriptionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "config": "config",
        "integration_key": "integrationKey",
        "name": "name",
        "on": "on",
        "statements": "statements",
        "id": "id",
        "tags": "tags",
    },
)
class AuditLogSubscriptionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        config: typing.Mapping[builtins.str, builtins.str],
        integration_key: builtins.str,
        name: builtins.str,
        on: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        statements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AuditLogSubscriptionStatements", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param config: The set of configuration fields corresponding to the value defined for ``integration_key``. Refer to the ``formVariables`` field in the corresponding ``integrations/<integration_key>/manifest.json`` file in `this repo <https://github.com/launchdarkly/integration-framework/tree/master/integrations>`_ for a full list of fields for the integration you wish to configure. **IMPORTANT**: Please note that Terraform will only accept these in snake case, regardless of the case shown in the manifest. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#config AuditLogSubscription#config}
        :param integration_key: The integration key. Supported integration keys are ``chronosphere``, ``cloudtrail``, ``datadog``, ``dynatrace``, ``elastic``, ``grafana``, ``honeycomb``, ``kosli``, ``last9``, ``logdna``, ``msteams``, ``new-relic-apm``, ``signalfx``, ``slack``, and ``splunk``. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#integration_key AuditLogSubscription#integration_key}
        :param name: A human-friendly name for your audit log subscription viewable from within the LaunchDarkly Integrations page. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#name AuditLogSubscription#name}
        :param on: Whether or not you want your subscription enabled, i.e. to actively send events. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#on AuditLogSubscription#on}
        :param statements: statements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#statements AuditLogSubscription#statements}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#id AuditLogSubscription#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#tags AuditLogSubscription#tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1e41a2cdac9756b56ce790ba595e5e76b13fcfd9f0a7f2d71efe562ae45ed6)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument integration_key", value=integration_key, expected_type=type_hints["integration_key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument on", value=on, expected_type=type_hints["on"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
            "integration_key": integration_key,
            "name": name,
            "on": on,
            "statements": statements,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if id is not None:
            self._values["id"] = id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def config(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The set of configuration fields corresponding to the value defined for ``integration_key``.

        Refer to the ``formVariables`` field in the corresponding ``integrations/<integration_key>/manifest.json`` file in `this repo <https://github.com/launchdarkly/integration-framework/tree/master/integrations>`_ for a full list of fields for the integration you wish to configure. **IMPORTANT**: Please note that Terraform will only accept these in snake case, regardless of the case shown in the manifest.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#config AuditLogSubscription#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def integration_key(self) -> builtins.str:
        '''The integration key.

        Supported integration keys are ``chronosphere``, ``cloudtrail``, ``datadog``, ``dynatrace``, ``elastic``, ``grafana``, ``honeycomb``, ``kosli``, ``last9``, ``logdna``, ``msteams``, ``new-relic-apm``, ``signalfx``, ``slack``, and ``splunk``. A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#integration_key AuditLogSubscription#integration_key}
        '''
        result = self._values.get("integration_key")
        assert result is not None, "Required property 'integration_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A human-friendly name for your audit log subscription viewable from within the LaunchDarkly Integrations page.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#name AuditLogSubscription#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def on(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether or not you want your subscription enabled, i.e. to actively send events.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#on AuditLogSubscription#on}
        '''
        result = self._values.get("on")
        assert result is not None, "Required property 'on' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def statements(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditLogSubscriptionStatements"]]:
        '''statements block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#statements AuditLogSubscription#statements}
        '''
        result = self._values.get("statements")
        assert result is not None, "Required property 'statements' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AuditLogSubscriptionStatements"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#id AuditLogSubscription#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags associated with your resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#tags AuditLogSubscription#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuditLogSubscriptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.auditLogSubscription.AuditLogSubscriptionStatements",
    jsii_struct_bases=[],
    name_mapping={
        "effect": "effect",
        "actions": "actions",
        "not_actions": "notActions",
        "not_resources": "notResources",
        "resources": "resources",
    },
)
class AuditLogSubscriptionStatements:
    def __init__(
        self,
        *,
        effect: builtins.str,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param effect: Either ``allow`` or ``deny``. This argument defines whether the statement allows or denies access to the named resources and actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#effect AuditLogSubscription#effect}
        :param actions: The list of action specifiers defining the actions to which the statement applies. Either ``actions`` or ``not_actions`` must be specified. For a list of available actions read `Actions reference <https://docs.launchdarkly.com/home/account-security/custom-roles/actions#actions-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#actions AuditLogSubscription#actions}
        :param not_actions: The list of action specifiers defining the actions to which the statement does not apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#not_actions AuditLogSubscription#not_actions}
        :param not_resources: The list of resource specifiers defining the resources to which the statement does not apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#not_resources AuditLogSubscription#not_resources}
        :param resources: The list of resource specifiers defining the resources to which the statement applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#resources AuditLogSubscription#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eafab4833c3c1fd2c0d9c87f5e7f4b213057774377a08fc698b07c04d741b68)
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument not_actions", value=not_actions, expected_type=type_hints["not_actions"])
            check_type(argname="argument not_resources", value=not_resources, expected_type=type_hints["not_resources"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "effect": effect,
        }
        if actions is not None:
            self._values["actions"] = actions
        if not_actions is not None:
            self._values["not_actions"] = not_actions
        if not_resources is not None:
            self._values["not_resources"] = not_resources
        if resources is not None:
            self._values["resources"] = resources

    @builtins.property
    def effect(self) -> builtins.str:
        '''Either ``allow`` or ``deny``.

        This argument defines whether the statement allows or denies access to the named resources and actions.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#effect AuditLogSubscription#effect}
        '''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of action specifiers defining the actions to which the statement applies.

        Either ``actions`` or ``not_actions`` must be specified. For a list of available actions read `Actions reference <https://docs.launchdarkly.com/home/account-security/custom-roles/actions#actions-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#actions AuditLogSubscription#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of action specifiers defining the actions to which the statement does not apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#not_actions AuditLogSubscription#not_actions}
        '''
        result = self._values.get("not_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of resource specifiers defining the resources to which the statement does not apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#not_resources AuditLogSubscription#not_resources}
        '''
        result = self._values.get("not_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of resource specifiers defining the resources to which the statement applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/audit_log_subscription#resources AuditLogSubscription#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuditLogSubscriptionStatements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AuditLogSubscriptionStatementsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.auditLogSubscription.AuditLogSubscriptionStatementsList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa849d166c930541bfe6a77a52b6078ca14b7a989c83d9351692dc4b6a8bf32)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AuditLogSubscriptionStatementsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc3cb3e53d2faa60cfe4bdef04110898eb5a0bcbe7727de00eabbddf2d3adf94)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AuditLogSubscriptionStatementsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e69a9705c47d54b626c2a39ea258848bafa6aa5cb5fe13201faeee175f77ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__187ad5bc76ccfd39bdbac50bbf771cf63991c31f846a503ef587176059078646)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc64dc8178e4fe7ebaa1f51ac34965316ec68749d68976f804983f6b9ab36a7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditLogSubscriptionStatements]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditLogSubscriptionStatements]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditLogSubscriptionStatements]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__639b60dc88564b507650def1a760f485e0de3656efd2bbe59f501b8004c1d892)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AuditLogSubscriptionStatementsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.auditLogSubscription.AuditLogSubscriptionStatementsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18177997cb8ff7e5f5ef7bf39e4c4651c9132bbfc9a55cf2219f6f731147e64)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetNotActions")
    def reset_not_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotActions", []))

    @jsii.member(jsii_name="resetNotResources")
    def reset_not_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotResources", []))

    @jsii.member(jsii_name="resetResources")
    def reset_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResources", []))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="effectInput")
    def effect_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectInput"))

    @builtins.property
    @jsii.member(jsii_name="notActionsInput")
    def not_actions_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="notResourcesInput")
    def not_resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "notResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="resourcesInput")
    def resources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @actions.setter
    def actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb9ec3d2a4be67c958c24158c461f584ea6cba17fc0d6d72117a4be6d2b2966d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15c33141045f73a7f7d042d4fe02cefc4e2dd959f41010ef36fa6f07dfac2d72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notActions")
    def not_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notActions"))

    @not_actions.setter
    def not_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6876594a7f9d43e7e929c7da7343d409a02684ba1316402d0af84acb40c8a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notActions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notResources")
    def not_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notResources"))

    @not_resources.setter
    def not_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebf1856cf7e4f58c6236309886e41442ba4c836ebd689d63896f83739e0dfc2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05b0dd5e7298e8daef10ffcc83822e8e6d41fb9529fc4129d6678d7e54d6f39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditLogSubscriptionStatements]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditLogSubscriptionStatements]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditLogSubscriptionStatements]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c091ff6d6dc6aed880d87fba97a924c35dae4f63a1409525b771e6a5354043f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AuditLogSubscription",
    "AuditLogSubscriptionConfig",
    "AuditLogSubscriptionStatements",
    "AuditLogSubscriptionStatementsList",
    "AuditLogSubscriptionStatementsOutputReference",
]

publication.publish()

def _typecheckingstub__411f1d0cc53fb5844b8519f71316b59e6c298594e900f01df5aa9adb42d72a9a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    config: typing.Mapping[builtins.str, builtins.str],
    integration_key: builtins.str,
    name: builtins.str,
    on: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    statements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AuditLogSubscriptionStatements, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e2178d972de561c6e0e19d7a939e5e9ec8becbe13a692471ade66625a0cdd0(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b09593dc48451cac7e1de804b7017af1f32c84353b22b5c4c0e47132d112d4dc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AuditLogSubscriptionStatements, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd93333e753af3e942674e8d35eb2bd562b2c17b91987e17175e5afe70e988de(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2d84a7846d6946c2c7e9910b45f406f96501fb19190e96f24154d42eafb0d44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56df65820b16507c6d5b07dc336b9299278931508a997f928c79bb7b2c8eb391(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d44d580c2023e22496c87a2ff72b8b489a25e7b4bb129e87f94d47b15ccf22d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8677ea16381901f65d55b725f90b48f7b45956a0f95d13506f39ec151ce8ce39(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ba6d47af38d7ff21f51dabc547973ed76fd65bf7e786ae53a1ca9f9637663f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1e41a2cdac9756b56ce790ba595e5e76b13fcfd9f0a7f2d71efe562ae45ed6(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    config: typing.Mapping[builtins.str, builtins.str],
    integration_key: builtins.str,
    name: builtins.str,
    on: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    statements: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AuditLogSubscriptionStatements, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eafab4833c3c1fd2c0d9c87f5e7f4b213057774377a08fc698b07c04d741b68(
    *,
    effect: builtins.str,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa849d166c930541bfe6a77a52b6078ca14b7a989c83d9351692dc4b6a8bf32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc3cb3e53d2faa60cfe4bdef04110898eb5a0bcbe7727de00eabbddf2d3adf94(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e69a9705c47d54b626c2a39ea258848bafa6aa5cb5fe13201faeee175f77ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__187ad5bc76ccfd39bdbac50bbf771cf63991c31f846a503ef587176059078646(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc64dc8178e4fe7ebaa1f51ac34965316ec68749d68976f804983f6b9ab36a7b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__639b60dc88564b507650def1a760f485e0de3656efd2bbe59f501b8004c1d892(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AuditLogSubscriptionStatements]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18177997cb8ff7e5f5ef7bf39e4c4651c9132bbfc9a55cf2219f6f731147e64(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9ec3d2a4be67c958c24158c461f584ea6cba17fc0d6d72117a4be6d2b2966d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15c33141045f73a7f7d042d4fe02cefc4e2dd959f41010ef36fa6f07dfac2d72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6876594a7f9d43e7e929c7da7343d409a02684ba1316402d0af84acb40c8a4a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf1856cf7e4f58c6236309886e41442ba4c836ebd689d63896f83739e0dfc2a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05b0dd5e7298e8daef10ffcc83822e8e6d41fb9529fc4129d6678d7e54d6f39(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c091ff6d6dc6aed880d87fba97a924c35dae4f63a1409525b771e6a5354043f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AuditLogSubscriptionStatements]],
) -> None:
    """Type checking stubs"""
    pass
