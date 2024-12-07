r'''
# `data_launchdarkly_feature_flag_environment`

Refer to the Terraform Registry for docs: [`data_launchdarkly_feature_flag_environment`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment).
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


class DataLaunchdarklyFeatureFlagEnvironment(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment launchdarkly_feature_flag_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        env_key: builtins.str,
        flag_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment launchdarkly_feature_flag_environment} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param env_key: The environment key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#env_key DataLaunchdarklyFeatureFlagEnvironment#env_key}
        :param flag_id: The feature flag's unique ``id`` in the format ``project_key/flag_key``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#flag_id DataLaunchdarklyFeatureFlagEnvironment#flag_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#id DataLaunchdarklyFeatureFlagEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90c7201088cc682989cfe4a66f317bf8c78a4e980658850fce9ac9a9e35331b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLaunchdarklyFeatureFlagEnvironmentConfig(
            env_key=env_key,
            flag_id=flag_id,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a DataLaunchdarklyFeatureFlagEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataLaunchdarklyFeatureFlagEnvironment to import.
        :param import_from_id: The id of the existing DataLaunchdarklyFeatureFlagEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataLaunchdarklyFeatureFlagEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbdece8673f98de26c21b45f8218ee2d6ccc672cdae393049585cfb49b3c54f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="contextTargets")
    def context_targets(
        self,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList", jsii.get(self, "contextTargets"))

    @builtins.property
    @jsii.member(jsii_name="fallthrough")
    def fallthrough(self) -> "DataLaunchdarklyFeatureFlagEnvironmentFallthroughList":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentFallthroughList", jsii.get(self, "fallthrough"))

    @builtins.property
    @jsii.member(jsii_name="offVariation")
    def off_variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "offVariation"))

    @builtins.property
    @jsii.member(jsii_name="on")
    def on(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "on"))

    @builtins.property
    @jsii.member(jsii_name="prerequisites")
    def prerequisites(
        self,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList", jsii.get(self, "prerequisites"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "DataLaunchdarklyFeatureFlagEnvironmentRulesList":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> "DataLaunchdarklyFeatureFlagEnvironmentTargetsList":
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentTargetsList", jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="trackEvents")
    def track_events(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "trackEvents"))

    @builtins.property
    @jsii.member(jsii_name="envKeyInput")
    def env_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="flagIdInput")
    def flag_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flagIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="envKey")
    def env_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envKey"))

    @env_key.setter
    def env_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48052dd6c7a023dcecce6585b80141ef2bf75e8bbea9ae6bb4c77a27c682b8c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flagId")
    def flag_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flagId"))

    @flag_id.setter
    def flag_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126d671c6f1e79cde7b6e0da7da9d97f229102e9d719fd234c6359ff50734169)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flagId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37431ffbfa1344495d2467f4e57cfddc0fd29de83f198523798d359debefb4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "env_key": "envKey",
        "flag_id": "flagId",
        "id": "id",
    },
)
class DataLaunchdarklyFeatureFlagEnvironmentConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        env_key: builtins.str,
        flag_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param env_key: The environment key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#env_key DataLaunchdarklyFeatureFlagEnvironment#env_key}
        :param flag_id: The feature flag's unique ``id`` in the format ``project_key/flag_key``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#flag_id DataLaunchdarklyFeatureFlagEnvironment#flag_id}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#id DataLaunchdarklyFeatureFlagEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3887b8a55bec50ce0052798f0dc17b208c0f50312a4ba4a1a14d0afb5a2ac31c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument env_key", value=env_key, expected_type=type_hints["env_key"])
            check_type(argname="argument flag_id", value=flag_id, expected_type=type_hints["flag_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env_key": env_key,
            "flag_id": flag_id,
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
    def env_key(self) -> builtins.str:
        '''The environment key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#env_key DataLaunchdarklyFeatureFlagEnvironment#env_key}
        '''
        result = self._values.get("env_key")
        assert result is not None, "Required property 'env_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flag_id(self) -> builtins.str:
        '''The feature flag's unique ``id`` in the format ``project_key/flag_key``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#flag_id DataLaunchdarklyFeatureFlagEnvironment#flag_id}
        '''
        result = self._values.get("flag_id")
        assert result is not None, "Required property 'flag_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag_environment#id DataLaunchdarklyFeatureFlagEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentContextTargets",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagEnvironmentContextTargets:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentContextTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4c861f85a336823e80a111eef51d967f3dc260ee12f6ceb139a6774c1b67bb9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d96e15de5a7e338cffd5f55069f05f939e9be8c9746a3ec2ca49ccc24974be04)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d31c4c8d97cde5aedd817fe5dbae1d13d56b76121dedb2872471f292e9967c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d6652b7937d676f69b4c17dbb1ee6f3bc0828e41428e2aaa246f2de48a90340)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43c7771d66b8cbbd7375b2c3309eb3201d96df03b6b2eed59e62f1b9594bab9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce5546370a9059518904401e231c12a1170cc38c130f333f53bdfc1420c0cace)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentContextTargets]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentContextTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentContextTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc8b87db97e573193c6c5d83a5210998f1a0779cef76678e95d50d43e5e9273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentFallthrough",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagEnvironmentFallthrough:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentFallthrough(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentFallthroughList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentFallthroughList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6a8990dfe5ac730aaa5ea42e63394bba7e64260e33f8e0b085d48c46acc1574)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1f15cdfcfa78cbddbe61a6bff7b1071d13e01ccb9c4373766b706a2d68db28)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7681d354e0843b743e9a051ab4a286b2e2ccbcb21a9db54c478ef38b6874c8f0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78a48fbd841e45d3a151303bf5b687f857683829745846e56d550279e3fcd46e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca9c2fce8b78be08c8b9274ed545bea8236e0de28892b292e9b2876d040da95f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a4f0fbb1b5671a2a896f5d94f94956c2c9a5bd6014dec31f958f1c75cf881d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="bucketBy")
    def bucket_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketBy"))

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @builtins.property
    @jsii.member(jsii_name="rolloutWeights")
    def rollout_weights(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "rolloutWeights"))

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentFallthrough]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentFallthrough], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentFallthrough],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87fb75d33b68925215bf849cd7f727caf53de05a1f20217892c8b94bd23e53ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentPrerequisites",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagEnvironmentPrerequisites:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentPrerequisites(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__924162720c08538d0a2a4f14a62324b405effc3c81735ad9cea5fb82bf5c0805)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6c31e50dd4fdb761d0e5490128dad96dfe468ffe6a6d5d4ccf8a6abe9257f41)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e93255de41cebe537b062c1b0a2372a4e349c879121f3b1bec1e3386b2d16a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__abc85e480215ef6bcda306cccd212af9ff3e33b322cf085b265acf1ddbf2ecbb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e7cfc261603b766e25969552c5d75ceabc86da32aee6921783c4667eefe83ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1f4843b547c4d95531c1f74c9b671eae102eb6ca7e0f6442399fb15882fb3d3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="flagKey")
    def flag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flagKey"))

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28139a67eeb753d3f28f90b45aec635af3eeef8a7c05cc76b1f2f37c6031eec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRules",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagEnvironmentRules:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesClauses",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagEnvironmentRulesClauses:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentRulesClauses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d77d4ea8da9059368daf4cba66cf1e1eac50e7759f7d2476b901988f5827a317)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f56f48f0390df4691fd02dc191b08847f9ccb4a2a8a092d68057ee5637115a13)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d050aa412d0f4bd721f8b5c5648117e5094e5a1a627b8519b1944f9904fae9eb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__779226076cba08212cce2c9167e237ef25068487bf21107382d298298e0e0858)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16c183342773b034d5f74c173910e26f3f7f3c18316909c226cc2661cff781b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__848108790c477e871c079f6d89d95b98f539c810e26dbec170b6c15842d8bf11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "negate"))

    @builtins.property
    @jsii.member(jsii_name="op")
    def op(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "op"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029bca670f80ae9e248a5717fa20e40ef161e132cb41eb9f84ec95d9200c9a16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagEnvironmentRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a13bd484e01f5c8cc11cfc327ec5c7de3953233568cfee096a88972662169e3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37c6feccf14873f0fe814689f37e8806c6b854af4795d019a04520889c49e3c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__690c441fd37e756e7b7e851912643e27cfc96766883d725f5150a01ed165106c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ece46b7986a13cdb4fbe87777a2dc631d54f0bcc14f041d24dfd1149e33eed79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfd89e88c0ba9f9f1a4f1b1a866dbea199118796b580894a63f9f23729491423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53ef788ed59cec2a828bf22949d89eb8caa2c51d399f5823838affebb2045b6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="bucketBy")
    def bucket_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketBy"))

    @builtins.property
    @jsii.member(jsii_name="clauses")
    def clauses(self) -> DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList:
        return typing.cast(DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList, jsii.get(self, "clauses"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="rolloutWeights")
    def rollout_weights(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "rolloutWeights"))

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentRules]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40a846e7e502ae738a10a6d7d2c5c218428d37d0404a08f5104374f088d1597)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentTargets",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagEnvironmentTargets:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagEnvironmentTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagEnvironmentTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e12d96e69c7e28805563915acec711644a2652c00d293a0a6cbbaf6f96988f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5384d99e6711f0a32b3e6900d6217aa69a29cce4b9fad93bd28faf8880bc6bde)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80c751e7e65653992eed5501fdafb8c6b916c6632c0c0a7e353dea31a2886855)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a64387f46224e1668fb086319ce8aaf7a675ed58e16f5a5d1df25ca898b1f71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed4896044257875b27c4d9d992cd34b9dd8a210f02ca0a32f38ab80265837b25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlagEnvironment.DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5016e2702df0d87756c5095f55d98c02bb93e52dc2b0558fc6400e0fad2af40f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentTargets]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentTargets], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentTargets],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23e8c92abd94efcff6462039bef5951a5a26d3a7c43f3b20db38becaeba8559c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataLaunchdarklyFeatureFlagEnvironment",
    "DataLaunchdarklyFeatureFlagEnvironmentConfig",
    "DataLaunchdarklyFeatureFlagEnvironmentContextTargets",
    "DataLaunchdarklyFeatureFlagEnvironmentContextTargetsList",
    "DataLaunchdarklyFeatureFlagEnvironmentContextTargetsOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentFallthrough",
    "DataLaunchdarklyFeatureFlagEnvironmentFallthroughList",
    "DataLaunchdarklyFeatureFlagEnvironmentFallthroughOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentPrerequisites",
    "DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesList",
    "DataLaunchdarklyFeatureFlagEnvironmentPrerequisitesOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentRules",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesClauses",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesClausesList",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesClausesOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesList",
    "DataLaunchdarklyFeatureFlagEnvironmentRulesOutputReference",
    "DataLaunchdarklyFeatureFlagEnvironmentTargets",
    "DataLaunchdarklyFeatureFlagEnvironmentTargetsList",
    "DataLaunchdarklyFeatureFlagEnvironmentTargetsOutputReference",
]

publication.publish()

def _typecheckingstub__90c7201088cc682989cfe4a66f317bf8c78a4e980658850fce9ac9a9e35331b6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    env_key: builtins.str,
    flag_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__bcbdece8673f98de26c21b45f8218ee2d6ccc672cdae393049585cfb49b3c54f(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48052dd6c7a023dcecce6585b80141ef2bf75e8bbea9ae6bb4c77a27c682b8c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126d671c6f1e79cde7b6e0da7da9d97f229102e9d719fd234c6359ff50734169(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37431ffbfa1344495d2467f4e57cfddc0fd29de83f198523798d359debefb4dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3887b8a55bec50ce0052798f0dc17b208c0f50312a4ba4a1a14d0afb5a2ac31c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    env_key: builtins.str,
    flag_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c861f85a336823e80a111eef51d967f3dc260ee12f6ceb139a6774c1b67bb9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d96e15de5a7e338cffd5f55069f05f939e9be8c9746a3ec2ca49ccc24974be04(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d31c4c8d97cde5aedd817fe5dbae1d13d56b76121dedb2872471f292e9967c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6652b7937d676f69b4c17dbb1ee6f3bc0828e41428e2aaa246f2de48a90340(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c7771d66b8cbbd7375b2c3309eb3201d96df03b6b2eed59e62f1b9594bab9f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce5546370a9059518904401e231c12a1170cc38c130f333f53bdfc1420c0cace(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc8b87db97e573193c6c5d83a5210998f1a0779cef76678e95d50d43e5e9273(
    value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentContextTargets],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6a8990dfe5ac730aaa5ea42e63394bba7e64260e33f8e0b085d48c46acc1574(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1f15cdfcfa78cbddbe61a6bff7b1071d13e01ccb9c4373766b706a2d68db28(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7681d354e0843b743e9a051ab4a286b2e2ccbcb21a9db54c478ef38b6874c8f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a48fbd841e45d3a151303bf5b687f857683829745846e56d550279e3fcd46e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9c2fce8b78be08c8b9274ed545bea8236e0de28892b292e9b2876d040da95f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a4f0fbb1b5671a2a896f5d94f94956c2c9a5bd6014dec31f958f1c75cf881d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87fb75d33b68925215bf849cd7f727caf53de05a1f20217892c8b94bd23e53ee(
    value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentFallthrough],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924162720c08538d0a2a4f14a62324b405effc3c81735ad9cea5fb82bf5c0805(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c31e50dd4fdb761d0e5490128dad96dfe468ffe6a6d5d4ccf8a6abe9257f41(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e93255de41cebe537b062c1b0a2372a4e349c879121f3b1bec1e3386b2d16a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc85e480215ef6bcda306cccd212af9ff3e33b322cf085b265acf1ddbf2ecbb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7cfc261603b766e25969552c5d75ceabc86da32aee6921783c4667eefe83ac(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f4843b547c4d95531c1f74c9b671eae102eb6ca7e0f6442399fb15882fb3d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28139a67eeb753d3f28f90b45aec635af3eeef8a7c05cc76b1f2f37c6031eec0(
    value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentPrerequisites],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77d4ea8da9059368daf4cba66cf1e1eac50e7759f7d2476b901988f5827a317(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f56f48f0390df4691fd02dc191b08847f9ccb4a2a8a092d68057ee5637115a13(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d050aa412d0f4bd721f8b5c5648117e5094e5a1a627b8519b1944f9904fae9eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779226076cba08212cce2c9167e237ef25068487bf21107382d298298e0e0858(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c183342773b034d5f74c173910e26f3f7f3c18316909c226cc2661cff781b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__848108790c477e871c079f6d89d95b98f539c810e26dbec170b6c15842d8bf11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029bca670f80ae9e248a5717fa20e40ef161e132cb41eb9f84ec95d9200c9a16(
    value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentRulesClauses],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13bd484e01f5c8cc11cfc327ec5c7de3953233568cfee096a88972662169e3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37c6feccf14873f0fe814689f37e8806c6b854af4795d019a04520889c49e3c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__690c441fd37e756e7b7e851912643e27cfc96766883d725f5150a01ed165106c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece46b7986a13cdb4fbe87777a2dc631d54f0bcc14f041d24dfd1149e33eed79(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd89e88c0ba9f9f1a4f1b1a866dbea199118796b580894a63f9f23729491423(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ef788ed59cec2a828bf22949d89eb8caa2c51d399f5823838affebb2045b6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40a846e7e502ae738a10a6d7d2c5c218428d37d0404a08f5104374f088d1597(
    value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e12d96e69c7e28805563915acec711644a2652c00d293a0a6cbbaf6f96988f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5384d99e6711f0a32b3e6900d6217aa69a29cce4b9fad93bd28faf8880bc6bde(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80c751e7e65653992eed5501fdafb8c6b916c6632c0c0a7e353dea31a2886855(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a64387f46224e1668fb086319ce8aaf7a675ed58e16f5a5d1df25ca898b1f71(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4896044257875b27c4d9d992cd34b9dd8a210f02ca0a32f38ab80265837b25(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5016e2702df0d87756c5095f55d98c02bb93e52dc2b0558fc6400e0fad2af40f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23e8c92abd94efcff6462039bef5951a5a26d3a7c43f3b20db38becaeba8559c(
    value: typing.Optional[DataLaunchdarklyFeatureFlagEnvironmentTargets],
) -> None:
    """Type checking stubs"""
    pass
