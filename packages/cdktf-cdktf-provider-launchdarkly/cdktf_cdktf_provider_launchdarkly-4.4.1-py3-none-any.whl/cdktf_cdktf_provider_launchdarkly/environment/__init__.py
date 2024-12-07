r'''
# `launchdarkly_environment`

Refer to the Terraform Registry for docs: [`launchdarkly_environment`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment).
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


class Environment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.environment.Environment",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment launchdarkly_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        color: builtins.str,
        key: builtins.str,
        name: builtins.str,
        project_key: builtins.str,
        approval_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EnvironmentApprovalSettings", typing.Dict[builtins.str, typing.Any]]]]] = None,
        confirm_changes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        require_comments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment launchdarkly_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param color: The color swatch as an RGB hex value with no leading ``#``. For example: ``000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#color Environment#color}
        :param key: The project-unique key for the environment. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#key Environment#key}
        :param name: The name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#name Environment#name}
        :param project_key: The LaunchDarkly project key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#project_key Environment#project_key}
        :param approval_settings: approval_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#approval_settings Environment#approval_settings}
        :param confirm_changes: Set to ``true`` if this environment requires confirmation for flag and segment changes. This field will default to ``false`` when not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#confirm_changes Environment#confirm_changes}
        :param critical: Denotes whether the environment is critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#critical Environment#critical}
        :param default_track_events: Set to ``true`` to enable data export for every flag created in this environment after you configure this argument. This field will default to ``false`` when not set. To learn more, read `Data Export <https://docs.launchdarkly.com/home/data-export>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#default_track_events Environment#default_track_events}
        :param default_ttl: The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to ``0`` when not set. To learn more, read `TTL settings <https://docs.launchdarkly.com/home/organize/environments#ttl-settings>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#default_ttl Environment#default_ttl}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#id Environment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param require_comments: Set to ``true`` if this environment requires comments for flag and segment changes. This field will default to ``false`` when not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#require_comments Environment#require_comments}
        :param secure_mode: Set to ``true`` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to ``false`` when not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#secure_mode Environment#secure_mode}
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#tags Environment#tags}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd90a16264f9116e12cd5895a4e41e5104d28828e360591f952dad4234a7c0b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EnvironmentConfig(
            color=color,
            key=key,
            name=name,
            project_key=project_key,
            approval_settings=approval_settings,
            confirm_changes=confirm_changes,
            critical=critical,
            default_track_events=default_track_events,
            default_ttl=default_ttl,
            id=id,
            require_comments=require_comments,
            secure_mode=secure_mode,
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
        '''Generates CDKTF code for importing a Environment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Environment to import.
        :param import_from_id: The id of the existing Environment that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Environment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b366076fd47c0cd625bd77bfbcfcdd389034a6098566ad233d2747c4b0c7341)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putApprovalSettings")
    def put_approval_settings(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EnvironmentApprovalSettings", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d0507ba4d648d080eaf0c7894d3fb53db398dd77cc2d5dce21f25cca93c142)
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

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetRequireComments")
    def reset_require_comments(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireComments", []))

    @jsii.member(jsii_name="resetSecureMode")
    def reset_secure_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSecureMode", []))

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
    @jsii.member(jsii_name="apiKey")
    def api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiKey"))

    @builtins.property
    @jsii.member(jsii_name="approvalSettings")
    def approval_settings(self) -> "EnvironmentApprovalSettingsList":
        return typing.cast("EnvironmentApprovalSettingsList", jsii.get(self, "approvalSettings"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnvironmentApprovalSettings"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EnvironmentApprovalSettings"]]], jsii.get(self, "approvalSettingsInput"))

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
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="projectKeyInput")
    def project_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectKeyInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__7869cb231164d493a8a2173d7d935c9d1bb6f60afcd265d698024fb59748f43a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ef4d6d43c532a9d239fc83bdb71e15e4ebca6972b357d78fd2a22bbb58ce2ad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06d95444e1d6c74899fc56c0b83090c4a909edc7452964be76562976bf73ae68)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2be7c8a0573241d8fe45f54957b57a13bc79606c362a1a16514a459bc53fbfa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTrackEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultTtl")
    def default_ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultTtl"))

    @default_ttl.setter
    def default_ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a96676cb978e9bdd63565d10ec529e2788da971a37475d4ebf1bd565a28d91a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultTtl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b11c60a6bb2988edc11e296d62d4b4d89e36952177effaae1e44a702bfb412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ddc81c5e9a1cc958359954335393e6faaf85f20900798f8e9bf337f5299e4d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6360d422d29a6634c798c4807ac4e8baa382977be186224f328a2eb167b0882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24ad0a39aa135f9e60b65e3470d7adbe6b54a16f1f6e6730f691199cc1c7bc9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__87e75a3d693b7df5a492e199e2c51a5256b131cd9c4152f88c3eef3b8172cdbf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15d461bfe8a289e0c6c388d6da54e6f3080a142a373cb156c5818073840868e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secureMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8be32378772afc916f92968ee3252382578f65fab04d8767dab3310bc0f74fcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.environment.EnvironmentApprovalSettings",
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
class EnvironmentApprovalSettings:
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
        :param can_apply_declined_changes: Set to ``true`` if changes can be applied as long as the ``min_num_approvals`` is met, regardless of whether any reviewers have declined a request. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#can_apply_declined_changes Environment#can_apply_declined_changes}
        :param can_review_own_request: Set to ``true`` if requesters can approve or decline their own request. They may always comment. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#can_review_own_request Environment#can_review_own_request}
        :param min_num_approvals: The number of approvals required before an approval request can be applied. This number must be between 1 and 5. Defaults to 1. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#min_num_approvals Environment#min_num_approvals}
        :param required: Set to ``true`` for changes to flags in this environment to require approval. You may only set ``required`` to true if ``required_approval_tags`` is not set and vice versa. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#required Environment#required}
        :param required_approval_tags: An array of tags used to specify which flags with those tags require approval. You may only set ``required_approval_tags`` if ``required`` is not set to ``true`` and vice versa. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#required_approval_tags Environment#required_approval_tags}
        :param service_config: The configuration for the service associated with this approval. This is specific to each approval service. For a ``service_kind`` of ``servicenow``, the following fields apply:: - `template` (String) The sys_id of the Standard Change Request Template in ServiceNow that LaunchDarkly will use when creating the change request. - `detail_column` (String) The name of the ServiceNow Change Request column LaunchDarkly uses to populate detailed approval request information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#service_config Environment#service_config}
        :param service_kind: The kind of service associated with this approval. This determines which platform is used for requesting approval. Valid values are ``servicenow``, ``launchdarkly``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#service_kind Environment#service_kind}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde5aff1deb87cd21c5ca5b96f9ed75728472d55dc6c7e315edff7452e2f09dd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#can_apply_declined_changes Environment#can_apply_declined_changes}
        '''
        result = self._values.get("can_apply_declined_changes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def can_review_own_request(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` if requesters can approve or decline their own request. They may always comment. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#can_review_own_request Environment#can_review_own_request}
        '''
        result = self._values.get("can_review_own_request")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def min_num_approvals(self) -> typing.Optional[jsii.Number]:
        '''The number of approvals required before an approval request can be applied.

        This number must be between 1 and 5. Defaults to 1.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#min_num_approvals Environment#min_num_approvals}
        '''
        result = self._values.get("min_num_approvals")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` for changes to flags in this environment to require approval.

        You may only set ``required`` to true if ``required_approval_tags`` is not set and vice versa. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#required Environment#required}
        '''
        result = self._values.get("required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def required_approval_tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of tags used to specify which flags with those tags require approval.

        You may only set ``required_approval_tags`` if ``required`` is not set to ``true`` and vice versa.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#required_approval_tags Environment#required_approval_tags}
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#service_config Environment#service_config}
        '''
        result = self._values.get("service_config")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def service_kind(self) -> typing.Optional[builtins.str]:
        '''The kind of service associated with this approval.

        This determines which platform is used for requesting approval. Valid values are ``servicenow``, ``launchdarkly``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#service_kind Environment#service_kind}
        '''
        result = self._values.get("service_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvironmentApprovalSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EnvironmentApprovalSettingsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.environment.EnvironmentApprovalSettingsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecbe34590f91f29f99eb2fffc1e0150c9bc284290b3d820e82400a0c48f902b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EnvironmentApprovalSettingsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7dee02fee6d0d145b8827aab4dc9655e2909b9fecbbea3b83b93f906d2df71f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EnvironmentApprovalSettingsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fff5ae40ec2b35ed37582d0cea13c75beadfbbeac67b2ea60fbd6302d6ebf7ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7cd5d6fddb81d3e41274d54f9bc9aae544283c55ee190ed65943c999395db70b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c128d7466f07401521b272650390fa0be2c6a2acb8bcf6c5a008738694459943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvironmentApprovalSettings]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvironmentApprovalSettings]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvironmentApprovalSettings]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9af7fed7cf72c859eb3a9c9666a96c68f825c971b2a1ceaf6599f78e15baea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EnvironmentApprovalSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.environment.EnvironmentApprovalSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bee89fa2835d997eb3d7a67d1041a5e4c94cc7e58f58a9c570a44c1d2c1a8f2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd33bbc8b6a4f50eedff72ed3c37b06e9eb3ff1f4e056df7c7d77e91b7497673)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7f088a1c3b4d99a5c945e73a16c542aa5d7aeacdf348ea4337f2e6e24da2309)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "canReviewOwnRequest", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minNumApprovals")
    def min_num_approvals(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minNumApprovals"))

    @min_num_approvals.setter
    def min_num_approvals(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f914a73d3a7bb166642a6fbc67932167bbd6e149ccbe52f220a9015af2181bd1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7423a5998a5103546c6dc3d3bfa951ead443d36a29fe276306910eaa667f9107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "required", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requiredApprovalTags")
    def required_approval_tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "requiredApprovalTags"))

    @required_approval_tags.setter
    def required_approval_tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e61120c81d1d81c4ab317abce36eadcca4e367bc9979bb860616717a021e1d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requiredApprovalTags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceConfig")
    def service_config(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "serviceConfig"))

    @service_config.setter
    def service_config(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb15ab4a61b908a578e7dc64032adffe1be50b673f8a27d81f84d9838a4ff7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceConfig", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceKind")
    def service_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceKind"))

    @service_kind.setter
    def service_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75f5df2ab258b686caa6004618ceef8842b2430b83e210bd5e27fccc729e8cdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnvironmentApprovalSettings]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnvironmentApprovalSettings]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnvironmentApprovalSettings]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e86f11d97a224ca71b8875e50206712aaccf26bd2f67b7c7c38e3bc3ed302a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.environment.EnvironmentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "color": "color",
        "key": "key",
        "name": "name",
        "project_key": "projectKey",
        "approval_settings": "approvalSettings",
        "confirm_changes": "confirmChanges",
        "critical": "critical",
        "default_track_events": "defaultTrackEvents",
        "default_ttl": "defaultTtl",
        "id": "id",
        "require_comments": "requireComments",
        "secure_mode": "secureMode",
        "tags": "tags",
    },
)
class EnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        color: builtins.str,
        key: builtins.str,
        name: builtins.str,
        project_key: builtins.str,
        approval_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnvironmentApprovalSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
        confirm_changes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        default_ttl: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        require_comments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        secure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param color: The color swatch as an RGB hex value with no leading ``#``. For example: ``000000``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#color Environment#color}
        :param key: The project-unique key for the environment. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#key Environment#key}
        :param name: The name of the environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#name Environment#name}
        :param project_key: The LaunchDarkly project key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#project_key Environment#project_key}
        :param approval_settings: approval_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#approval_settings Environment#approval_settings}
        :param confirm_changes: Set to ``true`` if this environment requires confirmation for flag and segment changes. This field will default to ``false`` when not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#confirm_changes Environment#confirm_changes}
        :param critical: Denotes whether the environment is critical. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#critical Environment#critical}
        :param default_track_events: Set to ``true`` to enable data export for every flag created in this environment after you configure this argument. This field will default to ``false`` when not set. To learn more, read `Data Export <https://docs.launchdarkly.com/home/data-export>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#default_track_events Environment#default_track_events}
        :param default_ttl: The TTL for the environment. This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to ``0`` when not set. To learn more, read `TTL settings <https://docs.launchdarkly.com/home/organize/environments#ttl-settings>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#default_ttl Environment#default_ttl}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#id Environment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param require_comments: Set to ``true`` if this environment requires comments for flag and segment changes. This field will default to ``false`` when not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#require_comments Environment#require_comments}
        :param secure_mode: Set to ``true`` to ensure a user of the client-side SDK cannot impersonate another user. This field will default to ``false`` when not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#secure_mode Environment#secure_mode}
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#tags Environment#tags}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0608c2d3a8c4886786970a153e9cd6eadb59d4a6053f51e829a03f3de98831)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument approval_settings", value=approval_settings, expected_type=type_hints["approval_settings"])
            check_type(argname="argument confirm_changes", value=confirm_changes, expected_type=type_hints["confirm_changes"])
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument default_track_events", value=default_track_events, expected_type=type_hints["default_track_events"])
            check_type(argname="argument default_ttl", value=default_ttl, expected_type=type_hints["default_ttl"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument require_comments", value=require_comments, expected_type=type_hints["require_comments"])
            check_type(argname="argument secure_mode", value=secure_mode, expected_type=type_hints["secure_mode"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "color": color,
            "key": key,
            "name": name,
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
        if id is not None:
            self._values["id"] = id
        if require_comments is not None:
            self._values["require_comments"] = require_comments
        if secure_mode is not None:
            self._values["secure_mode"] = secure_mode
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
    def color(self) -> builtins.str:
        '''The color swatch as an RGB hex value with no leading ``#``. For example: ``000000``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#color Environment#color}
        '''
        result = self._values.get("color")
        assert result is not None, "Required property 'color' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The project-unique key for the environment.

        A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#key Environment#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#name Environment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_key(self) -> builtins.str:
        '''The LaunchDarkly project key.

        A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#project_key Environment#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def approval_settings(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvironmentApprovalSettings]]]:
        '''approval_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#approval_settings Environment#approval_settings}
        '''
        result = self._values.get("approval_settings")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvironmentApprovalSettings]]], result)

    @builtins.property
    def confirm_changes(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` if this environment requires confirmation for flag and segment changes.

        This field will default to ``false`` when not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#confirm_changes Environment#confirm_changes}
        '''
        result = self._values.get("confirm_changes")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def critical(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Denotes whether the environment is critical.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#critical Environment#critical}
        '''
        result = self._values.get("critical")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_track_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` to enable data export for every flag created in this environment after you configure this argument.

        This field will default to ``false`` when not set. To learn more, read `Data Export <https://docs.launchdarkly.com/home/data-export>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#default_track_events Environment#default_track_events}
        '''
        result = self._values.get("default_track_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def default_ttl(self) -> typing.Optional[jsii.Number]:
        '''The TTL for the environment.

        This must be between 0 and 60 minutes. The TTL setting only applies to environments using the PHP SDK. This field will default to ``0`` when not set. To learn more, read `TTL settings <https://docs.launchdarkly.com/home/organize/environments#ttl-settings>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#default_ttl Environment#default_ttl}
        '''
        result = self._values.get("default_ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#id Environment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def require_comments(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` if this environment requires comments for flag and segment changes.

        This field will default to ``false`` when not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#require_comments Environment#require_comments}
        '''
        result = self._values.get("require_comments")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def secure_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Set to ``true`` to ensure a user of the client-side SDK cannot impersonate another user.

        This field will default to ``false`` when not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#secure_mode Environment#secure_mode}
        '''
        result = self._values.get("secure_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags associated with your resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/environment#tags Environment#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Environment",
    "EnvironmentApprovalSettings",
    "EnvironmentApprovalSettingsList",
    "EnvironmentApprovalSettingsOutputReference",
    "EnvironmentConfig",
]

publication.publish()

def _typecheckingstub__afd90a16264f9116e12cd5895a4e41e5104d28828e360591f952dad4234a7c0b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    color: builtins.str,
    key: builtins.str,
    name: builtins.str,
    project_key: builtins.str,
    approval_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnvironmentApprovalSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    confirm_changes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    require_comments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__7b366076fd47c0cd625bd77bfbcfcdd389034a6098566ad233d2747c4b0c7341(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d0507ba4d648d080eaf0c7894d3fb53db398dd77cc2d5dce21f25cca93c142(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnvironmentApprovalSettings, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7869cb231164d493a8a2173d7d935c9d1bb6f60afcd265d698024fb59748f43a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef4d6d43c532a9d239fc83bdb71e15e4ebca6972b357d78fd2a22bbb58ce2ad(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d95444e1d6c74899fc56c0b83090c4a909edc7452964be76562976bf73ae68(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2be7c8a0573241d8fe45f54957b57a13bc79606c362a1a16514a459bc53fbfa8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a96676cb978e9bdd63565d10ec529e2788da971a37475d4ebf1bd565a28d91a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b11c60a6bb2988edc11e296d62d4b4d89e36952177effaae1e44a702bfb412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ddc81c5e9a1cc958359954335393e6faaf85f20900798f8e9bf337f5299e4d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6360d422d29a6634c798c4807ac4e8baa382977be186224f328a2eb167b0882(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24ad0a39aa135f9e60b65e3470d7adbe6b54a16f1f6e6730f691199cc1c7bc9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e75a3d693b7df5a492e199e2c51a5256b131cd9c4152f88c3eef3b8172cdbf(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15d461bfe8a289e0c6c388d6da54e6f3080a142a373cb156c5818073840868e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8be32378772afc916f92968ee3252382578f65fab04d8767dab3310bc0f74fcf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde5aff1deb87cd21c5ca5b96f9ed75728472d55dc6c7e315edff7452e2f09dd(
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

def _typecheckingstub__ecbe34590f91f29f99eb2fffc1e0150c9bc284290b3d820e82400a0c48f902b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7dee02fee6d0d145b8827aab4dc9655e2909b9fecbbea3b83b93f906d2df71f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fff5ae40ec2b35ed37582d0cea13c75beadfbbeac67b2ea60fbd6302d6ebf7ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cd5d6fddb81d3e41274d54f9bc9aae544283c55ee190ed65943c999395db70b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c128d7466f07401521b272650390fa0be2c6a2acb8bcf6c5a008738694459943(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9af7fed7cf72c859eb3a9c9666a96c68f825c971b2a1ceaf6599f78e15baea0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EnvironmentApprovalSettings]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee89fa2835d997eb3d7a67d1041a5e4c94cc7e58f58a9c570a44c1d2c1a8f2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd33bbc8b6a4f50eedff72ed3c37b06e9eb3ff1f4e056df7c7d77e91b7497673(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7f088a1c3b4d99a5c945e73a16c542aa5d7aeacdf348ea4337f2e6e24da2309(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f914a73d3a7bb166642a6fbc67932167bbd6e149ccbe52f220a9015af2181bd1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7423a5998a5103546c6dc3d3bfa951ead443d36a29fe276306910eaa667f9107(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e61120c81d1d81c4ab317abce36eadcca4e367bc9979bb860616717a021e1d5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb15ab4a61b908a578e7dc64032adffe1be50b673f8a27d81f84d9838a4ff7cf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75f5df2ab258b686caa6004618ceef8842b2430b83e210bd5e27fccc729e8cdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e86f11d97a224ca71b8875e50206712aaccf26bd2f67b7c7c38e3bc3ed302a1f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EnvironmentApprovalSettings]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0608c2d3a8c4886786970a153e9cd6eadb59d4a6053f51e829a03f3de98831(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    color: builtins.str,
    key: builtins.str,
    name: builtins.str,
    project_key: builtins.str,
    approval_settings: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EnvironmentApprovalSettings, typing.Dict[builtins.str, typing.Any]]]]] = None,
    confirm_changes: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    critical: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    default_ttl: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    require_comments: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    secure_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
