r'''
# `launchdarkly_project`

Refer to the Terraform Registry for docs: [`launchdarkly_project`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project).
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


class Project(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.project.Project",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project launchdarkly_project}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        environments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectEnvironments", typing.Dict[builtins.str, typing.Any]]]],
        key: builtins.str,
        name: builtins.str,
        default_client_side_availability: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectDefaultClientSideAvailability", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_in_snippet: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project launchdarkly_project} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param environments: environments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#environments Project#environments}
        :param key: The project's unique key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#key Project#key}
        :param name: The project's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#name Project#name}
        :param default_client_side_availability: default_client_side_availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#default_client_side_availability Project#default_client_side_availability}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#id Project#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_in_snippet: Whether feature flags created under the project should be available to client-side SDKs by default. Please migrate to ``default_client_side_availability`` to maintain future compatibility. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#include_in_snippet Project#include_in_snippet}
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#tags Project#tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93863e3fb3fd83ae81a5fa249223e918b8c59e37a83bd136051efa59baf1c23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ProjectConfig(
            environments=environments,
            key=key,
            name=name,
            default_client_side_availability=default_client_side_availability,
            id=id,
            include_in_snippet=include_in_snippet,
            tags=tags,
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
        '''Generates CDKTF code for importing a Project resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Project to import.
        :param import_from_id: The id of the existing Project that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Project to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc132d41eed83f0e924ddfad27e2a768c892ddfa36e53b80e5e93f85c5e26180)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putDefaultClientSideAvailability")
    def put_default_client_side_availability(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectDefaultClientSideAvailability", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5bb3ed4d9ac140727819d0a8f4663414f6102a8efa239f4543d65b4960194a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDefaultClientSideAvailability", [value]))

    @jsii.member(jsii_name="putEnvironments")
    def put_environments(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectEnvironments", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ccddfdda7be3737e02b7c182dbb3ebac949b60bbdd8dabefad69ea900975aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEnvironments", [value]))

    @jsii.member(jsii_name="resetDefaultClientSideAvailability")
    def reset_default_client_side_availability(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultClientSideAvailability", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncludeInSnippet")
    def reset_include_in_snippet(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludeInSnippet", []))

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
    @jsii.member(jsii_name="defaultClientSideAvailability")
    def default_client_side_availability(
        self,
    ) -> "ProjectDefaultClientSideAvailabilityList":
        return typing.cast("ProjectDefaultClientSideAvailabilityList", jsii.get(self, "defaultClientSideAvailability"))

    @builtins.property
    @jsii.member(jsii_name="environments")
    def environments(self) -> "ProjectEnvironmentsList":
        return typing.cast("ProjectEnvironmentsList", jsii.get(self, "environments"))

    @builtins.property
    @jsii.member(jsii_name="defaultClientSideAvailabilityInput")
    def default_client_side_availability_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectDefaultClientSideAvailability"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectDefaultClientSideAvailability"]]], jsii.get(self, "defaultClientSideAvailabilityInput"))

    @builtins.property
    @jsii.member(jsii_name="environmentsInput")
    def environments_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectEnvironments"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectEnvironments"]]], jsii.get(self, "environmentsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includeInSnippetInput")
    def include_in_snippet_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "includeInSnippetInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0765ac7341a5088dcf55034b127464d3778dae6c5a7045257939523e23937a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includeInSnippet")
    def include_in_snippet(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "includeInSnippet"))

    @include_in_snippet.setter
    def include_in_snippet(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e98e097ea82115aab1c7121edc474d395a7acc0e91049b703ed6d05bec6235d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeInSnippet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c2db65965af4bdcac1305bb2dc53541ee456e4c53b86e195bd561a587323af6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6501e1acc3ab0cc7e8f0b32bae65a2243791b3b28fe2405fb73677d70ea104a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021e3b4722117b13842e875dfbdcec000068640a1cc831af081b4f02cfdd380d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "environments": "environments",
        "key": "key",
        "name": "name",
        "default_client_side_availability": "defaultClientSideAvailability",
        "id": "id",
        "include_in_snippet": "includeInSnippet",
        "tags": "tags",
    },
)
class ProjectConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        environments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectEnvironments", typing.Dict[builtins.str, typing.Any]]]],
        key: builtins.str,
        name: builtins.str,
        default_client_side_availability: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectDefaultClientSideAvailability", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        include_in_snippet: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param environments: environments block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#environments Project#environments}
        :param key: The project's unique key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#key Project#key}
        :param name: The project's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#name Project#name}
        :param default_client_side_availability: default_client_side_availability block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#default_client_side_availability Project#default_client_side_availability}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#id Project#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param include_in_snippet: Whether feature flags created under the project should be available to client-side SDKs by default. Please migrate to ``default_client_side_availability`` to maintain future compatibility. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#include_in_snippet Project#include_in_snippet}
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#tags Project#tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ae07973b215950e642bea0cd54fd02ef332024a996adeefa1d83b0c07431b53)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument environments", value=environments, expected_type=type_hints["environments"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument default_client_side_availability", value=default_client_side_availability, expected_type=type_hints["default_client_side_availability"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument include_in_snippet", value=include_in_snippet, expected_type=type_hints["include_in_snippet"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "environments": environments,
            "key": key,
            "name": name,
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
        if default_client_side_availability is not None:
            self._values["default_client_side_availability"] = default_client_side_availability
        if id is not None:
            self._values["id"] = id
        if include_in_snippet is not None:
            self._values["include_in_snippet"] = include_in_snippet
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
    def environments(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectEnvironments"]]:
        '''environments block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#environments Project#environments}
        '''
        result = self._values.get("environments")
        assert result is not None, "Required property 'environments' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectEnvironments"]], result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The project's unique key.

        A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#key Project#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The project's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#name Project#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_client_side_availability(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectDefaultClientSideAvailability"]]]:
        '''default_client_side_availability block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#default_client_side_availability Project#default_client_side_availability}
        '''
        result = self._values.get("default_client_side_availability")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectDefaultClientSideAvailability"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#id Project#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def include_in_snippet(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether feature flags created under the project should be available to client-side SDKs by default.

        Please migrate to ``default_client_side_availability`` to maintain future compatibility.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#include_in_snippet Project#include_in_snippet}
        '''
        result = self._values.get("include_in_snippet")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags associated with your resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#tags Project#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectDefaultClientSideAvailability",
    jsii_struct_bases=[],
    name_mapping={
        "using_environment_id": "usingEnvironmentId",
        "using_mobile_key": "usingMobileKey",
    },
)
class ProjectDefaultClientSideAvailability:
    def __init__(
        self,
        *,
        using_environment_id: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        using_mobile_key: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        '''
        :param using_environment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#using_environment_id Project#using_environment_id}.
        :param using_mobile_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#using_mobile_key Project#using_mobile_key}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7874d920a1b7a98a3f26d393bb93580676cb36ccecceef747b568340945c93c)
            check_type(argname="argument using_environment_id", value=using_environment_id, expected_type=type_hints["using_environment_id"])
            check_type(argname="argument using_mobile_key", value=using_mobile_key, expected_type=type_hints["using_mobile_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "using_environment_id": using_environment_id,
            "using_mobile_key": using_mobile_key,
        }

    @builtins.property
    def using_environment_id(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#using_environment_id Project#using_environment_id}.'''
        result = self._values.get("using_environment_id")
        assert result is not None, "Required property 'using_environment_id' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def using_mobile_key(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#using_mobile_key Project#using_mobile_key}.'''
        result = self._values.get("using_mobile_key")
        assert result is not None, "Required property 'using_mobile_key' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectDefaultClientSideAvailability(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectDefaultClientSideAvailabilityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectDefaultClientSideAvailabilityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__52dad5654eb58a0512b30d014f75efb8180250cc67b4b965fdb4a076d846e139)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProjectDefaultClientSideAvailabilityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__005c4140e228cccc8cc6ddea55390bf040036616fe9f455e109616e4a9707759)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProjectDefaultClientSideAvailabilityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb99a432b04e98d7435bb17be8655bfd63082c9194f2e1f2e48ca8d8359c0ffb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49c20e9f500a25993f55618655638e39e48f4c58fb9792fd17d9af5e9762e139)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bdf0aef00dc816cdccfb330c803430ecd07d048b2a37c2613bd8ec88510dc59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectDefaultClientSideAvailability]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectDefaultClientSideAvailability]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectDefaultClientSideAvailability]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feffd7dc2eb815914c135792d351def997cecc9a47a133676989adf3909a37fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProjectDefaultClientSideAvailabilityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectDefaultClientSideAvailabilityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffceb046ff85144beb3f4f3d42262ef9755e08037d5611691e984f3f00162ce2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="usingEnvironmentIdInput")
    def using_environment_id_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "usingEnvironmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="usingMobileKeyInput")
    def using_mobile_key_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "usingMobileKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="usingEnvironmentId")
    def using_environment_id(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "usingEnvironmentId"))

    @using_environment_id.setter
    def using_environment_id(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b75c2bc44778c29190c4da60d03f3b5202e5553690c09a45071caa7462e932)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usingEnvironmentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="usingMobileKey")
    def using_mobile_key(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "usingMobileKey"))

    @using_mobile_key.setter
    def using_mobile_key(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e4b672fdd7b8c5e1f4b70496341bda71ecf0bf89123fb17da3f29326ee752b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "usingMobileKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectDefaultClientSideAvailability]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectDefaultClientSideAvailability]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectDefaultClientSideAvailability]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22fd15909c266d3c7f7d6049bfb938c34f7c994550fe705fcee25ebdf26cf68f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectEnvironments",
    jsii_struct_bases=[],
    name_mapping={
        "color": "color",
        "key": "key",
        "name": "name",
        "approval_settings": "approvalSettings",
        "confirm_changes": "confirmChanges",
        "critical": "critical",
        "default_track_events": "defaultTrackEvents",
        "default_ttl": "defaultTtl",
        "require_comments": "requireComments",
        "secure_mode": "secureMode",
        "tags": "tags",
    },
)
class ProjectEnvironments:
    def __init__(
        self,
        *,
        color: builtins.str,
        key: builtins.str,
        name: builtins.str,
        approval_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ProjectEnvironmentsApprovalSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        confirm_changes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        require_comments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param color: The color swatch as an RGB hex value with no leading ``#``. For example: ``000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#color Project#color}
        :param key: The project-unique key for the environment. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#key Project#key}
        :param name: The name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#name Project#name}
        :param approval_settings: approval_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#approval_settings Project#approval_settings}
        :param confirm_changes: Set to ``true`` if this environment requires confirmation for flag and segment changes. This field will default to ``false`` when not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#confirm_changes Project#confirm_changes}
        :param critical: Denotes whether the environment is critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#critical Project#critical}
        :param default_track_events: Set to ``true`` to enable data export for every flag created in this environment after you configure this argument. This field will default to ``false`` when not set. To learn more, read `Data Export <https://docs.launchdarkly.com/home/data-export>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#default_track_events Project#default_track_events}
        :param default_ttl: The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to ``0`` when not set. To learn more, read `TTL settings <https://docs.launchdarkly.com/home/organize/environments#ttl-settings>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#default_ttl Project#default_ttl}
        :param require_comments: Set to ``true`` if this environment requires comments for flag and segment changes. This field will default to ``false`` when not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#require_comments Project#require_comments}
        :param secure_mode: Set to ``true`` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to ``false`` when not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#secure_mode Project#secure_mode}
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#tags Project#tags}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac2ed1b079b68cb919a5a6db7a4c230b9465cd2b936b69294e4e02637b01c6c4)
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument approval_settings", value=approval_settings, expected_type=type_hints["approval_settings"])
            check_type(argname="argument confirm_changes", value=confirm_changes, expected_type=type_hints["confirm_changes"])
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument default_track_events", value=default_track_events, expected_type=type_hints["default_track_events"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument require_comments", value=require_comments, expected_type=type_hints["require_comments"])
            check_type(argname="argument secure_mode", value=secure_mode, expected_type=type_hints["secure_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "color": color,
            "key": key,
            "name": name,
        }
        if approval_settings is not None:
            self._values["approval_settings"] = approval_settings
        if confirm_changes is not None:
            self._values["confirm_changes"] = confirm_changes
        if critical is not None:
            self._values["critical"] = critical
        if default_track_events is not None:
            self._values["default_track_events"] = default_track_events
        if default_ttl is not None:
            self._values["default_ttl"] = default_ttl
        if require_comments is not None:
            self._values["require_comments"] = require_comments
        if secure_mode is not None:
            self._values["secure_mode"] = secure_mode
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def color(self) -> builtins.str:
        '''The color swatch as an RGB hex value with no leading ``#``. For example: ``000000``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#color Project#color}
        '''
        result = self._values.get("color")
        assert result is not None, "Required property 'color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The project-unique key for the environment.

        A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#key Project#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#name Project#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def approval_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectEnvironmentsApprovalSettings"]]]:
        '''approval_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#approval_settings Project#approval_settings}
        '''
        result = self._values.get("approval_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ProjectEnvironmentsApprovalSettings"]]], result)

    @builtins.property
    def confirm_changes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` if this environment requires confirmation for flag and segment changes.

        This field will default to ``false`` when not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#confirm_changes Project#confirm_changes}
        '''
        result = self._values.get("confirm_changes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def critical(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes whether the environment is critical.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#critical Project#critical}
        '''
        result = self._values.get("critical")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_track_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` to enable data export for every flag created in this environment after you configure this argument.

        This field will default to ``false`` when not set. To learn more, read `Data Export <https://docs.launchdarkly.com/home/data-export>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#default_track_events Project#default_track_events}
        '''
        result = self._values.get("default_track_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''The TTL for the environment.

        This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to ``0`` when not set. To learn more, read `TTL settings <https://docs.launchdarkly.com/home/organize/environments#ttl-settings>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#default_ttl Project#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def require_comments(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` if this environment requires comments for flag and segment changes.

        This field will default to ``false`` when not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#require_comments Project#require_comments}
        '''
        result = self._values.get("require_comments")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secure_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` to ensure a user of the client-side SDK cannot impersonate another user.

        This field will default to ``false`` when not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#secure_mode Project#secure_mode}
        '''
        result = self._values.get("secure_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags associated with your resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#tags Project#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectEnvironments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectEnvironmentsApprovalSettings",
    jsii_struct_bases=[],
    name_mapping={
        "can_apply_declined_changes": "canApplyDeclinedChanges",
        "can_review_own_request": "canReviewOwnRequest",
        "min_num_approvals": "minNumApprovals",
        "required": "required",
        "required_approval_tags": "requiredApprovalTags",
        "service_config": "serviceConfig",
        "service_kind": "serviceKind",
    },
)
class ProjectEnvironmentsApprovalSettings:
    def __init__(
        self,
        *,
        can_apply_declined_changes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        can_review_own_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        min_num_approvals: typing.Optional[jsii.Number] = None,
        required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        required_approval_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        service_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param can_apply_declined_changes: Set to ``true`` if changes can be applied as long as the ``min_num_approvals`` is met, regardless of whether any reviewers have declined a request. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#can_apply_declined_changes Project#can_apply_declined_changes}
        :param can_review_own_request: Set to ``true`` if requesters can approve or decline their own request. They may always comment. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#can_review_own_request Project#can_review_own_request}
        :param min_num_approvals: The number of approvals required before an approval request can be applied. This number must be between 1 and 5. Defaults to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#min_num_approvals Project#min_num_approvals}
        :param required: Set to ``true`` for changes to flags in this environment to require approval. You may only set ``required`` to true if ``required_approval_tags`` is not set and vice versa. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#required Project#required}
        :param required_approval_tags: An array of tags used to specify which flags with those tags require approval. You may only set ``required_approval_tags`` if ``required`` is not set to ``true`` and vice versa. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#required_approval_tags Project#required_approval_tags}
        :param service_config: The configuration for the service associated with this approval. This is specific to each approval service. For a ``service_kind`` of ``servicenow``, the following fields apply:: - `template` (String) The sys_id of the Standard Change Request Template in ServiceNow that LaunchDarkly will use when creating the change request. - `detail_column` (String) The name of the ServiceNow Change Request column LaunchDarkly uses to populate detailed approval request information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#service_config Project#service_config}
        :param service_kind: The kind of service associated with this approval. This determines which platform is used for requesting approval. Valid values are ``servicenow``, ``launchdarkly``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#service_kind Project#service_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0da4efd35c7e9a11f3765c4e842e83118be30fc18f2d3a933612b6d1f5eebf)
            check_type(argname="argument can_apply_declined_changes", value=can_apply_declined_changes, expected_type=type_hints["can_apply_declined_changes"])
            check_type(argname="argument can_review_own_request", value=can_review_own_request, expected_type=type_hints["can_review_own_request"])
            check_type(argname="argument min_num_approvals", value=min_num_approvals, expected_type=type_hints["min_num_approvals"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument required_approval_tags", value=required_approval_tags, expected_type=type_hints["required_approval_tags"])
            check_type(argname="argument service_config", value=service_config, expected_type=type_hints["service_config"])
            check_type(argname="argument service_kind", value=service_kind, expected_type=type_hints["service_kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if can_apply_declined_changes is not None:
            self._values["can_apply_declined_changes"] = can_apply_declined_changes
        if can_review_own_request is not None:
            self._values["can_review_own_request"] = can_review_own_request
        if min_num_approvals is not None:
            self._values["min_num_approvals"] = min_num_approvals
        if required is not None:
            self._values["required"] = required
        if required_approval_tags is not None:
            self._values["required_approval_tags"] = required_approval_tags
        if service_config is not None:
            self._values["service_config"] = service_config
        if service_kind is not None:
            self._values["service_kind"] = service_kind

    @builtins.property
    def can_apply_declined_changes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` if changes can be applied as long as the ``min_num_approvals`` is met, regardless of whether any reviewers have declined a request.

        Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#can_apply_declined_changes Project#can_apply_declined_changes}
        '''
        result = self._values.get("can_apply_declined_changes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def can_review_own_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` if requesters can approve or decline their own request. They may always comment. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#can_review_own_request Project#can_review_own_request}
        '''
        result = self._values.get("can_review_own_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def min_num_approvals(self) -> typing.Optional[jsii.Number]:
        '''The number of approvals required before an approval request can be applied.

        This number must be between 1 and 5. Defaults to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#min_num_approvals Project#min_num_approvals}
        '''
        result = self._values.get("min_num_approvals")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` for changes to flags in this environment to require approval.

        You may only set ``required`` to true if ``required_approval_tags`` is not set and vice versa. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#required Project#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_approval_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of tags used to specify which flags with those tags require approval.

        You may only set ``required_approval_tags`` if ``required`` is not set to ``true`` and vice versa.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#required_approval_tags Project#required_approval_tags}
        '''
        result = self._values.get("required_approval_tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_config(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The configuration for the service associated with this approval.

        This is specific to each approval service. For a ``service_kind`` of ``servicenow``, the following fields apply::

            - `template` (String) The sys_id of the Standard Change Request Template in ServiceNow that LaunchDarkly will use when creating the change request.
            - `detail_column` (String) The name of the ServiceNow Change Request column LaunchDarkly uses to populate detailed approval request information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#service_config Project#service_config}
        '''
        result = self._values.get("service_config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def service_kind(self) -> typing.Optional[builtins.str]:
        '''The kind of service associated with this approval.

        This determines which platform is used for requesting approval. Valid values are ``servicenow``, ``launchdarkly``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/project#service_kind Project#service_kind}
        '''
        result = self._values.get("service_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectEnvironmentsApprovalSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProjectEnvironmentsApprovalSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectEnvironmentsApprovalSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04bc89b00b3eed1b82d9e06ed61f0de6ead9acd8e8bbaecf26b71e4e36067b5e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ProjectEnvironmentsApprovalSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da7c74c58e13c649542038d8bf2b5d0e34ec4efdebd03a74637cb09768ae3605)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProjectEnvironmentsApprovalSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a8e49f7495acbfe858f25c21e81588f9b67854d2e2c9a97250a8a3033103b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d620bb1884b6a6b9d7a4af04f92d2d966672f5bb8e1e9230d0486740e7a12a22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__575b49b5eaf4bc2e6484293553c9e1ac029f31430b656cb8b989a4fa003014c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironmentsApprovalSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironmentsApprovalSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironmentsApprovalSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6575b41366f9ab125c4e1a8589c5116f9982b7920b1eb610c782adfa40a7a493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProjectEnvironmentsApprovalSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectEnvironmentsApprovalSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__429121cb2591cf106618b33163c789b30b61b77190013d88a1c7b33fa470fe80)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCanApplyDeclinedChanges")
    def reset_can_apply_declined_changes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanApplyDeclinedChanges", []))

    @jsii.member(jsii_name="resetCanReviewOwnRequest")
    def reset_can_review_own_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCanReviewOwnRequest", []))

    @jsii.member(jsii_name="resetMinNumApprovals")
    def reset_min_num_approvals(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinNumApprovals", []))

    @jsii.member(jsii_name="resetRequired")
    def reset_required(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequired", []))

    @jsii.member(jsii_name="resetRequiredApprovalTags")
    def reset_required_approval_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequiredApprovalTags", []))

    @jsii.member(jsii_name="resetServiceConfig")
    def reset_service_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceConfig", []))

    @jsii.member(jsii_name="resetServiceKind")
    def reset_service_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceKind", []))

    @builtins.property
    @jsii.member(jsii_name="canApplyDeclinedChangesInput")
    def can_apply_declined_changes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canApplyDeclinedChangesInput"))

    @builtins.property
    @jsii.member(jsii_name="canReviewOwnRequestInput")
    def can_review_own_request_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "canReviewOwnRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="minNumApprovalsInput")
    def min_num_approvals_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minNumApprovalsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredApprovalTagsInput")
    def required_approval_tags_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "requiredApprovalTagsInput"))

    @builtins.property
    @jsii.member(jsii_name="requiredInput")
    def required_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requiredInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceConfigInput")
    def service_config_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "serviceConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceKindInput")
    def service_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceKindInput"))

    @builtins.property
    @jsii.member(jsii_name="canApplyDeclinedChanges")
    def can_apply_declined_changes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canApplyDeclinedChanges"))

    @can_apply_declined_changes.setter
    def can_apply_declined_changes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3d00c44a89ed13c6c208372e7f2f949b857cd5574cbc93d8fa5870f9989dc38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canApplyDeclinedChanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="canReviewOwnRequest")
    def can_review_own_request(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "canReviewOwnRequest"))

    @can_review_own_request.setter
    def can_review_own_request(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c539f864f28a2a8fff5604fa3c8aaf3545dc9e20ac53df1b2dabfa12a0cf1e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canReviewOwnRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNumApprovals")
    def min_num_approvals(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNumApprovals"))

    @min_num_approvals.setter
    def min_num_approvals(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575426ab571814b8f05159825b63ee34cc24d8d2f15c8ce1512d6ffaaec48bbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minNumApprovals", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="required")
    def required(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "required"))

    @required.setter
    def required(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b70e0ed4dc7d42867cf6bec9574065f61d3ca161241e2760a1ffbbb7704daf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredApprovalTags")
    def required_approval_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requiredApprovalTags"))

    @required_approval_tags.setter
    def required_approval_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c628ea0eacb7020a1908dd512bc9fe3797fe504b26ce4bbeb0d6fe7b6f5bccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredApprovalTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceConfig")
    def service_config(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "serviceConfig"))

    @service_config.setter
    def service_config(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__754d9dd8ef79e604b37855dbe2d9001e3f014c3017ce5b8f1d99f88568bdc15a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceKind")
    def service_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceKind"))

    @service_kind.setter
    def service_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab85cc51352f7f86de42ce1bce6649a1f44051031029426e0fdad6833682a4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectEnvironmentsApprovalSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectEnvironmentsApprovalSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectEnvironmentsApprovalSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ae462af1cabdf005fb9c3ba14efba88e9e262399dbfea1ae81ca85766fefc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProjectEnvironmentsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectEnvironmentsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__190d1b16d7bf5ee43b2ba597992cea6d7ae8765e23ccb976cf06ea6f0937c2d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ProjectEnvironmentsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b4abb5c6f3dd9a95ecc8a1650885b4a14f690271fe9224812376b684156e8c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ProjectEnvironmentsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccda1af762a38a406a26cadbdac6592f7820eac357651dbe479d177acf7f36fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9588eb34d73a44e1ace9adddc6335ed27695b9a5942ba1e5a96319f9fb47b9d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34a79359e4c37c0382f57d0ac6d1e2199a42d7f612911b727160d429e26a01cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironments]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironments]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironments]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d8f999364d1004788ff1e1dbbcdab79f487d0bfa968af20b859a72d76394c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ProjectEnvironmentsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.project.ProjectEnvironmentsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b866be0cbe2756e408448bb1e8177c95a79ec0a57bdb673c43b14749a4b4f26)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putApprovalSettings")
    def put_approval_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectEnvironmentsApprovalSettings, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb1fc892f1447a339706e00843e94975fb0a243b4757ca2e91ddcf843f8e1cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putApprovalSettings", [value]))

    @jsii.member(jsii_name="resetApprovalSettings")
    def reset_approval_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApprovalSettings", []))

    @jsii.member(jsii_name="resetConfirmChanges")
    def reset_confirm_changes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfirmChanges", []))

    @jsii.member(jsii_name="resetCritical")
    def reset_critical(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCritical", []))

    @jsii.member(jsii_name="resetDefaultTrackEvents")
    def reset_default_track_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTrackEvents", []))

    @jsii.member(jsii_name="resetDefaultTtl")
    def reset_default_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultTtl", []))

    @jsii.member(jsii_name="resetRequireComments")
    def reset_require_comments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireComments", []))

    @jsii.member(jsii_name="resetSecureMode")
    def reset_secure_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecureMode", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @builtins.property
    @jsii.member(jsii_name="approvalSettings")
    def approval_settings(self) -> ProjectEnvironmentsApprovalSettingsList:
        return typing.cast(ProjectEnvironmentsApprovalSettingsList, jsii.get(self, "approvalSettings"))

    @builtins.property
    @jsii.member(jsii_name="clientSideId")
    def client_side_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSideId"))

    @builtins.property
    @jsii.member(jsii_name="mobileKey")
    def mobile_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mobileKey"))

    @builtins.property
    @jsii.member(jsii_name="approvalSettingsInput")
    def approval_settings_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironmentsApprovalSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironmentsApprovalSettings]]], jsii.get(self, "approvalSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="colorInput")
    def color_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "colorInput"))

    @builtins.property
    @jsii.member(jsii_name="confirmChangesInput")
    def confirm_changes_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "confirmChangesInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTrackEventsInput")
    def default_track_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "defaultTrackEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultTtlInput")
    def default_ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultTtlInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="requireCommentsInput")
    def require_comments_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireCommentsInput"))

    @builtins.property
    @jsii.member(jsii_name="secureModeInput")
    def secure_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "secureModeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="color")
    def color(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "color"))

    @color.setter
    def color(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6daef64a0ff00266b6eff7f66ddf12a442b2f9bfb95111b2c97bf02ff7cd2d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "color", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="confirmChanges")
    def confirm_changes(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "confirmChanges"))

    @confirm_changes.setter
    def confirm_changes(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1569be8cd488d45ed866f20362c1dc3e240accb0eff2470a1bf8f5f654f041)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "confirmChanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "critical"))

    @critical.setter
    def critical(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49188a6af584ef977c9d5a8d7218f980ca794563dbfa05c65b6bcb9f8acf6481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "critical", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTrackEvents")
    def default_track_events(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "defaultTrackEvents"))

    @default_track_events.setter
    def default_track_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2b05efa0ed4c1d191b5240f212ea16600f5764fd16f7d421b7271200b00098a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTrackEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__879eb630d126761bc228a07039179f98b6e1e71cfef1a66d2f26e8e9d3cd24b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243681e7badceef355af6c7d827096e9bd329a434cab1d19b442ece965891004)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c29412989a19d0e6aa323a9578a66f76a678a9f6b26e9fead601932f0791d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireComments")
    def require_comments(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireComments"))

    @require_comments.setter
    def require_comments(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3db41b22e74ea6e456dc3f2a6bde368088a8655e503cc399a22e44502dbd75f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireComments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="secureMode")
    def secure_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "secureMode"))

    @secure_mode.setter
    def secure_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__471afbd43826131e961e318020354235ae664ce49b2b741d125aa8ccbfeea5ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secureMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4767a335e2edbf2ed03ba51b25a22a7f1f155764fb6b597e350bd5f5b7e8bffe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectEnvironments]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectEnvironments]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectEnvironments]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb04691c00c044ebdcdb5c633f4f5e6a603d1fb388b9cbaf55878770e4528fae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Project",
    "ProjectConfig",
    "ProjectDefaultClientSideAvailability",
    "ProjectDefaultClientSideAvailabilityList",
    "ProjectDefaultClientSideAvailabilityOutputReference",
    "ProjectEnvironments",
    "ProjectEnvironmentsApprovalSettings",
    "ProjectEnvironmentsApprovalSettingsList",
    "ProjectEnvironmentsApprovalSettingsOutputReference",
    "ProjectEnvironmentsList",
    "ProjectEnvironmentsOutputReference",
]

publication.publish()

def _typecheckingstub__f93863e3fb3fd83ae81a5fa249223e918b8c59e37a83bd136051efa59baf1c23(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    environments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectEnvironments, typing.Dict[builtins.str, typing.Any]]]],
    key: builtins.str,
    name: builtins.str,
    default_client_side_availability: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectDefaultClientSideAvailability, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_in_snippet: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__bc132d41eed83f0e924ddfad27e2a768c892ddfa36e53b80e5e93f85c5e26180(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5bb3ed4d9ac140727819d0a8f4663414f6102a8efa239f4543d65b4960194a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectDefaultClientSideAvailability, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ccddfdda7be3737e02b7c182dbb3ebac949b60bbdd8dabefad69ea900975aa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectEnvironments, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0765ac7341a5088dcf55034b127464d3778dae6c5a7045257939523e23937a57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e98e097ea82115aab1c7121edc474d395a7acc0e91049b703ed6d05bec6235d2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2db65965af4bdcac1305bb2dc53541ee456e4c53b86e195bd561a587323af6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6501e1acc3ab0cc7e8f0b32bae65a2243791b3b28fe2405fb73677d70ea104a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021e3b4722117b13842e875dfbdcec000068640a1cc831af081b4f02cfdd380d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ae07973b215950e642bea0cd54fd02ef332024a996adeefa1d83b0c07431b53(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    environments: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectEnvironments, typing.Dict[builtins.str, typing.Any]]]],
    key: builtins.str,
    name: builtins.str,
    default_client_side_availability: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectDefaultClientSideAvailability, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    include_in_snippet: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7874d920a1b7a98a3f26d393bb93580676cb36ccecceef747b568340945c93c(
    *,
    using_environment_id: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    using_mobile_key: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52dad5654eb58a0512b30d014f75efb8180250cc67b4b965fdb4a076d846e139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__005c4140e228cccc8cc6ddea55390bf040036616fe9f455e109616e4a9707759(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb99a432b04e98d7435bb17be8655bfd63082c9194f2e1f2e48ca8d8359c0ffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c20e9f500a25993f55618655638e39e48f4c58fb9792fd17d9af5e9762e139(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bdf0aef00dc816cdccfb330c803430ecd07d048b2a37c2613bd8ec88510dc59(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feffd7dc2eb815914c135792d351def997cecc9a47a133676989adf3909a37fd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectDefaultClientSideAvailability]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffceb046ff85144beb3f4f3d42262ef9755e08037d5611691e984f3f00162ce2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b75c2bc44778c29190c4da60d03f3b5202e5553690c09a45071caa7462e932(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e4b672fdd7b8c5e1f4b70496341bda71ecf0bf89123fb17da3f29326ee752b3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22fd15909c266d3c7f7d6049bfb938c34f7c994550fe705fcee25ebdf26cf68f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectDefaultClientSideAvailability]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac2ed1b079b68cb919a5a6db7a4c230b9465cd2b936b69294e4e02637b01c6c4(
    *,
    color: builtins.str,
    key: builtins.str,
    name: builtins.str,
    approval_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectEnvironmentsApprovalSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    confirm_changes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    require_comments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0da4efd35c7e9a11f3765c4e842e83118be30fc18f2d3a933612b6d1f5eebf(
    *,
    can_apply_declined_changes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    can_review_own_request: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    min_num_approvals: typing.Optional[jsii.Number] = None,
    required: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    required_approval_tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_config: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    service_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04bc89b00b3eed1b82d9e06ed61f0de6ead9acd8e8bbaecf26b71e4e36067b5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da7c74c58e13c649542038d8bf2b5d0e34ec4efdebd03a74637cb09768ae3605(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a8e49f7495acbfe858f25c21e81588f9b67854d2e2c9a97250a8a3033103b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d620bb1884b6a6b9d7a4af04f92d2d966672f5bb8e1e9230d0486740e7a12a22(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575b49b5eaf4bc2e6484293553c9e1ac029f31430b656cb8b989a4fa003014c7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6575b41366f9ab125c4e1a8589c5116f9982b7920b1eb610c782adfa40a7a493(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironmentsApprovalSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__429121cb2591cf106618b33163c789b30b61b77190013d88a1c7b33fa470fe80(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3d00c44a89ed13c6c208372e7f2f949b857cd5574cbc93d8fa5870f9989dc38(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c539f864f28a2a8fff5604fa3c8aaf3545dc9e20ac53df1b2dabfa12a0cf1e73(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575426ab571814b8f05159825b63ee34cc24d8d2f15c8ce1512d6ffaaec48bbe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b70e0ed4dc7d42867cf6bec9574065f61d3ca161241e2760a1ffbbb7704daf6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c628ea0eacb7020a1908dd512bc9fe3797fe504b26ce4bbeb0d6fe7b6f5bccf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__754d9dd8ef79e604b37855dbe2d9001e3f014c3017ce5b8f1d99f88568bdc15a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab85cc51352f7f86de42ce1bce6649a1f44051031029426e0fdad6833682a4d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ae462af1cabdf005fb9c3ba14efba88e9e262399dbfea1ae81ca85766fefc6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectEnvironmentsApprovalSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190d1b16d7bf5ee43b2ba597992cea6d7ae8765e23ccb976cf06ea6f0937c2d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b4abb5c6f3dd9a95ecc8a1650885b4a14f690271fe9224812376b684156e8c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccda1af762a38a406a26cadbdac6592f7820eac357651dbe479d177acf7f36fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9588eb34d73a44e1ace9adddc6335ed27695b9a5942ba1e5a96319f9fb47b9d1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a79359e4c37c0382f57d0ac6d1e2199a42d7f612911b727160d429e26a01cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d8f999364d1004788ff1e1dbbcdab79f487d0bfa968af20b859a72d76394c4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ProjectEnvironments]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b866be0cbe2756e408448bb1e8177c95a79ec0a57bdb673c43b14749a4b4f26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb1fc892f1447a339706e00843e94975fb0a243b4757ca2e91ddcf843f8e1cf(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ProjectEnvironmentsApprovalSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6daef64a0ff00266b6eff7f66ddf12a442b2f9bfb95111b2c97bf02ff7cd2d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1569be8cd488d45ed866f20362c1dc3e240accb0eff2470a1bf8f5f654f041(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49188a6af584ef977c9d5a8d7218f980ca794563dbfa05c65b6bcb9f8acf6481(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b05efa0ed4c1d191b5240f212ea16600f5764fd16f7d421b7271200b00098a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879eb630d126761bc228a07039179f98b6e1e71cfef1a66d2f26e8e9d3cd24b4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243681e7badceef355af6c7d827096e9bd329a434cab1d19b442ece965891004(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c29412989a19d0e6aa323a9578a66f76a678a9f6b26e9fead601932f0791d3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3db41b22e74ea6e456dc3f2a6bde368088a8655e503cc399a22e44502dbd75f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471afbd43826131e961e318020354235ae664ce49b2b741d125aa8ccbfeea5ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4767a335e2edbf2ed03ba51b25a22a7f1f155764fb6b597e350bd5f5b7e8bffe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb04691c00c044ebdcdb5c633f4f5e6a603d1fb388b9cbaf55878770e4528fae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ProjectEnvironments]],
) -> None:
    """Type checking stubs"""
    pass
