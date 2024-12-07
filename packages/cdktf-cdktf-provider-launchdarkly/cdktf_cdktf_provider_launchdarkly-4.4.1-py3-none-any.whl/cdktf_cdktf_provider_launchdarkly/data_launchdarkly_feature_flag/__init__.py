r'''
# `data_launchdarkly_feature_flag`

Refer to the Terraform Registry for docs: [`data_launchdarkly_feature_flag`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag).
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


class DataLaunchdarklyFeatureFlag(
    _cdktf_9a9027ec.TerraformDataSource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlag",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag launchdarkly_feature_flag}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        key: builtins.str,
        project_key: builtins.str,
        id: typing.Optional[builtins.str] = None,
        maintainer_id: typing.Optional[builtins.str] = None,
        maintainer_team_key: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag launchdarkly_feature_flag} Data Source.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param key: The unique feature flag key that references the flag in your application code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#key DataLaunchdarklyFeatureFlag#key}
        :param project_key: The feature flag's project key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#project_key DataLaunchdarklyFeatureFlag#project_key}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#id DataLaunchdarklyFeatureFlag#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintainer_id: The feature flag maintainer's 24 character alphanumeric team member ID. ``maintainer_team_key`` cannot be set if ``maintainer_id`` is set. If neither is set, it will automatically be or stay set to the member ID associated with the API key used by your LaunchDarkly Terraform provider or the most recently-set maintainer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#maintainer_id DataLaunchdarklyFeatureFlag#maintainer_id}
        :param maintainer_team_key: The key of the associated team that maintains this feature flag. ``maintainer_id`` cannot be set if ``maintainer_team_key`` is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#maintainer_team_key DataLaunchdarklyFeatureFlag#maintainer_team_key}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd472e721a5b9a57959ca895c010f4b6019c5f43972008821693a4d274aaeece)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DataLaunchdarklyFeatureFlagConfig(
            key=key,
            project_key=project_key,
            id=id,
            maintainer_id=maintainer_id,
            maintainer_team_key=maintainer_team_key,
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
        '''Generates CDKTF code for importing a DataLaunchdarklyFeatureFlag resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DataLaunchdarklyFeatureFlag to import.
        :param import_from_id: The id of the existing DataLaunchdarklyFeatureFlag that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DataLaunchdarklyFeatureFlag to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf79ead42c7cfc000b3592742ddc7ed149b6ee1e6db9a469423a7abd9df1a410)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMaintainerId")
    def reset_maintainer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainerId", []))

    @jsii.member(jsii_name="resetMaintainerTeamKey")
    def reset_maintainer_team_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaintainerTeamKey", []))

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
    @jsii.member(jsii_name="archived")
    def archived(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "archived"))

    @builtins.property
    @jsii.member(jsii_name="clientSideAvailability")
    def client_side_availability(
        self,
    ) -> "DataLaunchdarklyFeatureFlagClientSideAvailabilityList":
        return typing.cast("DataLaunchdarklyFeatureFlagClientSideAvailabilityList", jsii.get(self, "clientSideAvailability"))

    @builtins.property
    @jsii.member(jsii_name="customProperties")
    def custom_properties(self) -> "DataLaunchdarklyFeatureFlagCustomPropertiesList":
        return typing.cast("DataLaunchdarklyFeatureFlagCustomPropertiesList", jsii.get(self, "customProperties"))

    @builtins.property
    @jsii.member(jsii_name="defaults")
    def defaults(self) -> "DataLaunchdarklyFeatureFlagDefaultsList":
        return typing.cast("DataLaunchdarklyFeatureFlagDefaultsList", jsii.get(self, "defaults"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="includeInSnippet")
    def include_in_snippet(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "includeInSnippet"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="temporary")
    def temporary(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "temporary"))

    @builtins.property
    @jsii.member(jsii_name="variations")
    def variations(self) -> "DataLaunchdarklyFeatureFlagVariationsList":
        return typing.cast("DataLaunchdarklyFeatureFlagVariationsList", jsii.get(self, "variations"))

    @builtins.property
    @jsii.member(jsii_name="variationType")
    def variation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "variationType"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="maintainerIdInput")
    def maintainer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintainerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="maintainerTeamKeyInput")
    def maintainer_team_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maintainerTeamKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKeyInput")
    def project_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__924dbdf38cdc09f17e9e8347f0a0ef366f131f948e660717efa2bd62ef799800)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cc12e391a65cd83ee10c8d78497680f349817421afb19d7fc384f4b157e585f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainerId")
    def maintainer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainerId"))

    @maintainer_id.setter
    def maintainer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19b9ddcee6cb01369187d676924559d2b292f77098b2dc5d3f81283e38df2171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainerId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maintainerTeamKey")
    def maintainer_team_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maintainerTeamKey"))

    @maintainer_team_key.setter
    def maintainer_team_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786cf6063c9631520f01dd14d551767616cb7f77045de73ff1816bc457ca7d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maintainerTeamKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e96ec2f4ae0b9508de4e49a49f32e4eccca74c259049f586c19e0fd157cf2d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagClientSideAvailability",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagClientSideAvailability:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagClientSideAvailability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagClientSideAvailabilityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagClientSideAvailabilityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__975133d018be7809edeae14b9305654186c1876ca4598ffc15d2e2c13ea964c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagClientSideAvailabilityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea9a4b471034231558f9fcb699ebc74f9f78b0c70096dced6328fd0bbbb54f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagClientSideAvailabilityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20a530c531c28358b9cac6aa9cd44295fa2d45a52fdb9417e9eb197e4d2bb606)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9963d100a16375908b7295edf7791352bc3432f8b6b2fcd53edc722be3e0bcef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__25b03fd70a711789cf7eda3298922840c9deaa602792eb3e37db5899dfc21bb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagClientSideAvailabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagClientSideAvailabilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__90e41c9eba9c71b7f2b1664972aebce9c17396f28a26a74bc198f0c7e7961abf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="usingEnvironmentId")
    def using_environment_id(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "usingEnvironmentId"))

    @builtins.property
    @jsii.member(jsii_name="usingMobileKey")
    def using_mobile_key(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "usingMobileKey"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFeatureFlagClientSideAvailability]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagClientSideAvailability], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagClientSideAvailability],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c281996774b3f3a0f956e380b0b50175d6168097ea9b8992ea0c72cbd5e17f99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "key": "key",
        "project_key": "projectKey",
        "id": "id",
        "maintainer_id": "maintainerId",
        "maintainer_team_key": "maintainerTeamKey",
    },
)
class DataLaunchdarklyFeatureFlagConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        key: builtins.str,
        project_key: builtins.str,
        id: typing.Optional[builtins.str] = None,
        maintainer_id: typing.Optional[builtins.str] = None,
        maintainer_team_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param key: The unique feature flag key that references the flag in your application code. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#key DataLaunchdarklyFeatureFlag#key}
        :param project_key: The feature flag's project key. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#project_key DataLaunchdarklyFeatureFlag#project_key}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#id DataLaunchdarklyFeatureFlag#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param maintainer_id: The feature flag maintainer's 24 character alphanumeric team member ID. ``maintainer_team_key`` cannot be set if ``maintainer_id`` is set. If neither is set, it will automatically be or stay set to the member ID associated with the API key used by your LaunchDarkly Terraform provider or the most recently-set maintainer. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#maintainer_id DataLaunchdarklyFeatureFlag#maintainer_id}
        :param maintainer_team_key: The key of the associated team that maintains this feature flag. ``maintainer_id`` cannot be set if ``maintainer_team_key`` is set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#maintainer_team_key DataLaunchdarklyFeatureFlag#maintainer_team_key}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__530b455bc63811ba078aa401a86b5e682619333c87f8c2405c03d404a47fc2b1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument maintainer_id", value=maintainer_id, expected_type=type_hints["maintainer_id"])
            check_type(argname="argument maintainer_team_key", value=maintainer_team_key, expected_type=type_hints["maintainer_team_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "project_key": project_key,
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
        if maintainer_id is not None:
            self._values["maintainer_id"] = maintainer_id
        if maintainer_team_key is not None:
            self._values["maintainer_team_key"] = maintainer_team_key

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
    def key(self) -> builtins.str:
        '''The unique feature flag key that references the flag in your application code.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#key DataLaunchdarklyFeatureFlag#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_key(self) -> builtins.str:
        '''The feature flag's project key.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#project_key DataLaunchdarklyFeatureFlag#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#id DataLaunchdarklyFeatureFlag#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintainer_id(self) -> typing.Optional[builtins.str]:
        '''The feature flag maintainer's 24 character alphanumeric team member ID.

        ``maintainer_team_key`` cannot be set if ``maintainer_id`` is set. If neither is set, it will automatically be or stay set to the member ID associated with the API key used by your LaunchDarkly Terraform provider or the most recently-set maintainer.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#maintainer_id DataLaunchdarklyFeatureFlag#maintainer_id}
        '''
        result = self._values.get("maintainer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def maintainer_team_key(self) -> typing.Optional[builtins.str]:
        '''The key of the associated team that maintains this feature flag. ``maintainer_id`` cannot be set if ``maintainer_team_key`` is set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/data-sources/feature_flag#maintainer_team_key DataLaunchdarklyFeatureFlag#maintainer_team_key}
        '''
        result = self._values.get("maintainer_team_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagCustomProperties",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagCustomProperties:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagCustomProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagCustomPropertiesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagCustomPropertiesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37d9e3d855361eb73f76a4cf7fbe37871b35b0e3f99af550d163bae4fedd1591)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagCustomPropertiesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6342947c6e4b752fccdb9e170a2ad01e3163929985e614f0b05ac2f3e29de685)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagCustomPropertiesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c51ef13148777ed040bbc1e3522cf6157f6a449394947c241a65515c0338e1ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dc341b84ee91b77d47f8f59a670334773273cc52073e8c5dde3af7d0f10f892)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3ec76e67bef3453ce8d03911d7e54674490346bf53b4eab65b17f542e638d995)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagCustomPropertiesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagCustomPropertiesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fbcf4926d2d2fdac970fce616a67bcc9b53e9a04a399a9f75e2b5e1333b23d4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DataLaunchdarklyFeatureFlagCustomProperties]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagCustomProperties], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagCustomProperties],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01dea3c0fa740a05d6daebffe5cf1986fdf83fb5f76eecf374e6aa8aad9756eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagDefaults",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagDefaults:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagDefaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagDefaultsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagDefaultsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3111cc9c1e3070d1acf64e38af037fa3aaf3e648e40c8bc4fc804e9532ca3445)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagDefaultsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff2a8cf4284d0c51d4f4f59c999ca2e5611e13cc57c13c117751955f19d3cfe0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagDefaultsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381e556391e4eea18f44958fff2aacf8a248efcea2b1f9c9c266524f89a0044f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea31d5a3c16da11e2bd0e62024e1f56a2c39b1b20cf03f8edeeb0e7b0ae26d59)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56c1453958c7b282432dd25291ec36d9bce054469374ed32ea49fbf54f964196)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagDefaultsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagDefaultsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d49b42c746fd470acfdb58ae7a64c4e8c09464b4fb7fa424f1cefaef46c9a88)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="offVariation")
    def off_variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "offVariation"))

    @builtins.property
    @jsii.member(jsii_name="onVariation")
    def on_variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "onVariation"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataLaunchdarklyFeatureFlagDefaults]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagDefaults], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagDefaults],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d86aeb0da8c32f5975540fb2cc53a95193f16466d80c2f41fff30d6053d086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagVariations",
    jsii_struct_bases=[],
    name_mapping={},
)
class DataLaunchdarklyFeatureFlagVariations:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataLaunchdarklyFeatureFlagVariations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataLaunchdarklyFeatureFlagVariationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagVariationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__92596fb8728630148130a9d08f4f17ba79ba7b4421e1d32d782025df85163a1a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DataLaunchdarklyFeatureFlagVariationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889e56cfbd59731d24ede6485775108f7711c88b1dda557f4d31dcd4da337154)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DataLaunchdarklyFeatureFlagVariationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c0cf505f9bdf36d2091c714907310495b0e511dcdddf84fb7a6dff0c39c3c29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d564fdfc5f104e111ca8a372baea0e68d61fd89b5667a42f48772d37794c5c63)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff5d5e4cefe27987142946b7c1ce8df19a03a2a9e1dd7a7efc4fce9da202b71f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DataLaunchdarklyFeatureFlagVariationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.dataLaunchdarklyFeatureFlag.DataLaunchdarklyFeatureFlagVariationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b06762144ec08ca1fb103b2520151a3238cfa3da8996020183d2665f11784973)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DataLaunchdarklyFeatureFlagVariations]:
        return typing.cast(typing.Optional[DataLaunchdarklyFeatureFlagVariations], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DataLaunchdarklyFeatureFlagVariations],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf6482783beedd0f43355a159c69f139326290ea09ddc93de514bcc2d55af2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DataLaunchdarklyFeatureFlag",
    "DataLaunchdarklyFeatureFlagClientSideAvailability",
    "DataLaunchdarklyFeatureFlagClientSideAvailabilityList",
    "DataLaunchdarklyFeatureFlagClientSideAvailabilityOutputReference",
    "DataLaunchdarklyFeatureFlagConfig",
    "DataLaunchdarklyFeatureFlagCustomProperties",
    "DataLaunchdarklyFeatureFlagCustomPropertiesList",
    "DataLaunchdarklyFeatureFlagCustomPropertiesOutputReference",
    "DataLaunchdarklyFeatureFlagDefaults",
    "DataLaunchdarklyFeatureFlagDefaultsList",
    "DataLaunchdarklyFeatureFlagDefaultsOutputReference",
    "DataLaunchdarklyFeatureFlagVariations",
    "DataLaunchdarklyFeatureFlagVariationsList",
    "DataLaunchdarklyFeatureFlagVariationsOutputReference",
]

publication.publish()

def _typecheckingstub__cd472e721a5b9a57959ca895c010f4b6019c5f43972008821693a4d274aaeece(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    key: builtins.str,
    project_key: builtins.str,
    id: typing.Optional[builtins.str] = None,
    maintainer_id: typing.Optional[builtins.str] = None,
    maintainer_team_key: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__cf79ead42c7cfc000b3592742ddc7ed149b6ee1e6db9a469423a7abd9df1a410(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924dbdf38cdc09f17e9e8347f0a0ef366f131f948e660717efa2bd62ef799800(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cc12e391a65cd83ee10c8d78497680f349817421afb19d7fc384f4b157e585f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19b9ddcee6cb01369187d676924559d2b292f77098b2dc5d3f81283e38df2171(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786cf6063c9631520f01dd14d551767616cb7f77045de73ff1816bc457ca7d03(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e96ec2f4ae0b9508de4e49a49f32e4eccca74c259049f586c19e0fd157cf2d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975133d018be7809edeae14b9305654186c1876ca4598ffc15d2e2c13ea964c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea9a4b471034231558f9fcb699ebc74f9f78b0c70096dced6328fd0bbbb54f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a530c531c28358b9cac6aa9cd44295fa2d45a52fdb9417e9eb197e4d2bb606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9963d100a16375908b7295edf7791352bc3432f8b6b2fcd53edc722be3e0bcef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b03fd70a711789cf7eda3298922840c9deaa602792eb3e37db5899dfc21bb3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e41c9eba9c71b7f2b1664972aebce9c17396f28a26a74bc198f0c7e7961abf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c281996774b3f3a0f956e380b0b50175d6168097ea9b8992ea0c72cbd5e17f99(
    value: typing.Optional[DataLaunchdarklyFeatureFlagClientSideAvailability],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__530b455bc63811ba078aa401a86b5e682619333c87f8c2405c03d404a47fc2b1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    key: builtins.str,
    project_key: builtins.str,
    id: typing.Optional[builtins.str] = None,
    maintainer_id: typing.Optional[builtins.str] = None,
    maintainer_team_key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d9e3d855361eb73f76a4cf7fbe37871b35b0e3f99af550d163bae4fedd1591(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6342947c6e4b752fccdb9e170a2ad01e3163929985e614f0b05ac2f3e29de685(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c51ef13148777ed040bbc1e3522cf6157f6a449394947c241a65515c0338e1ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dc341b84ee91b77d47f8f59a670334773273cc52073e8c5dde3af7d0f10f892(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ec76e67bef3453ce8d03911d7e54674490346bf53b4eab65b17f542e638d995(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fbcf4926d2d2fdac970fce616a67bcc9b53e9a04a399a9f75e2b5e1333b23d4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01dea3c0fa740a05d6daebffe5cf1986fdf83fb5f76eecf374e6aa8aad9756eb(
    value: typing.Optional[DataLaunchdarklyFeatureFlagCustomProperties],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3111cc9c1e3070d1acf64e38af037fa3aaf3e648e40c8bc4fc804e9532ca3445(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff2a8cf4284d0c51d4f4f59c999ca2e5611e13cc57c13c117751955f19d3cfe0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381e556391e4eea18f44958fff2aacf8a248efcea2b1f9c9c266524f89a0044f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea31d5a3c16da11e2bd0e62024e1f56a2c39b1b20cf03f8edeeb0e7b0ae26d59(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c1453958c7b282432dd25291ec36d9bce054469374ed32ea49fbf54f964196(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d49b42c746fd470acfdb58ae7a64c4e8c09464b4fb7fa424f1cefaef46c9a88(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d86aeb0da8c32f5975540fb2cc53a95193f16466d80c2f41fff30d6053d086(
    value: typing.Optional[DataLaunchdarklyFeatureFlagDefaults],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92596fb8728630148130a9d08f4f17ba79ba7b4421e1d32d782025df85163a1a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889e56cfbd59731d24ede6485775108f7711c88b1dda557f4d31dcd4da337154(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c0cf505f9bdf36d2091c714907310495b0e511dcdddf84fb7a6dff0c39c3c29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d564fdfc5f104e111ca8a372baea0e68d61fd89b5667a42f48772d37794c5c63(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5d5e4cefe27987142946b7c1ce8df19a03a2a9e1dd7a7efc4fce9da202b71f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06762144ec08ca1fb103b2520151a3238cfa3da8996020183d2665f11784973(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf6482783beedd0f43355a159c69f139326290ea09ddc93de514bcc2d55af2d(
    value: typing.Optional[DataLaunchdarklyFeatureFlagVariations],
) -> None:
    """Type checking stubs"""
    pass
