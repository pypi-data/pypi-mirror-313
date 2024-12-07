r'''
# `launchdarkly_segment`

Refer to the Terraform Registry for docs: [`launchdarkly_segment`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment).
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


class Segment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.segment.Segment",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment launchdarkly_segment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        env_key: builtins.str,
        key: builtins.str,
        name: builtins.str,
        project_key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentExcludedContexts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        included: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentIncludedContexts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        unbounded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unbounded_context_kind: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment launchdarkly_segment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param env_key: The segment's environment key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#env_key Segment#env_key}
        :param key: The unique key that references the segment. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#key Segment#key}
        :param name: The human-friendly name for the segment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#name Segment#name}
        :param project_key: The segment's project key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#project_key Segment#project_key}
        :param description: The description of the segment's purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#description Segment#description}
        :param excluded: List of user keys excluded from the segment. To target on other context kinds, use the excluded_contexts block attribute. This attribute is not valid when ``unbounded`` is set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#excluded Segment#excluded}
        :param excluded_contexts: excluded_contexts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#excluded_contexts Segment#excluded_contexts}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#id Segment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included: List of user keys included in the segment. To target on other context kinds, use the included_contexts block attribute. This attribute is not valid when ``unbounded`` is set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#included Segment#included}
        :param included_contexts: included_contexts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#included_contexts Segment#included_contexts}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#rules Segment#rules}
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#tags Segment#tags}
        :param unbounded: Whether to create a standard segment (``false``) or a Big Segment (``true``). Standard segments include rule-based and smaller list-based segments. Big Segments include larger list-based segments and synced segments. Only use a Big Segment if you need to add more than 15,000 individual targets. It is not possible to manage the list of targeted contexts for Big Segments with Terraform. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#unbounded Segment#unbounded}
        :param unbounded_context_kind: For Big Segments, the targeted context kind. If this attribute is not specified it will default to ``user``. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#unbounded_context_kind Segment#unbounded_context_kind}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bc761ed5b800bcee541f20c7692dc1475952f2b353da4883a658b8141010ac2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SegmentConfig(
            env_key=env_key,
            key=key,
            name=name,
            project_key=project_key,
            description=description,
            excluded=excluded,
            excluded_contexts=excluded_contexts,
            id=id,
            included=included,
            included_contexts=included_contexts,
            rules=rules,
            tags=tags,
            unbounded=unbounded,
            unbounded_context_kind=unbounded_context_kind,
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
        '''Generates CDKTF code for importing a Segment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Segment to import.
        :param import_from_id: The id of the existing Segment that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Segment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d563361b02e46803ed18c62be8732cd1f4164094a27ac1ef01893574d839b092)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putExcludedContexts")
    def put_excluded_contexts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentExcludedContexts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292578362c5fea7cdb24974843f5dda598e915c5c2d62b433024dac504b7fc3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExcludedContexts", [value]))

    @jsii.member(jsii_name="putIncludedContexts")
    def put_included_contexts(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentIncludedContexts", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff1731f8af72d01eb4be94e7c281818f22ae80fccfb354f34f9b4a5b3196c78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncludedContexts", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__465042511387850a47b69228bb63e77c0768a0ecf5e46049422eda7891034b02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetExcluded")
    def reset_excluded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcluded", []))

    @jsii.member(jsii_name="resetExcludedContexts")
    def reset_excluded_contexts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedContexts", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIncluded")
    def reset_included(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncluded", []))

    @jsii.member(jsii_name="resetIncludedContexts")
    def reset_included_contexts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludedContexts", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetUnbounded")
    def reset_unbounded(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnbounded", []))

    @jsii.member(jsii_name="resetUnboundedContextKind")
    def reset_unbounded_context_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnboundedContextKind", []))

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
    @jsii.member(jsii_name="creationDate")
    def creation_date(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "creationDate"))

    @builtins.property
    @jsii.member(jsii_name="excludedContexts")
    def excluded_contexts(self) -> "SegmentExcludedContextsList":
        return typing.cast("SegmentExcludedContextsList", jsii.get(self, "excludedContexts"))

    @builtins.property
    @jsii.member(jsii_name="includedContexts")
    def included_contexts(self) -> "SegmentIncludedContextsList":
        return typing.cast("SegmentIncludedContextsList", jsii.get(self, "includedContexts"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "SegmentRulesList":
        return typing.cast("SegmentRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="envKeyInput")
    def env_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedContextsInput")
    def excluded_contexts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentExcludedContexts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentExcludedContexts"]]], jsii.get(self, "excludedContextsInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedInput")
    def excluded_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="includedContextsInput")
    def included_contexts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentIncludedContexts"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentIncludedContexts"]]], jsii.get(self, "includedContextsInput"))

    @builtins.property
    @jsii.member(jsii_name="includedInput")
    def included_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includedInput"))

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
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="unboundedContextKindInput")
    def unbounded_context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unboundedContextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="unboundedInput")
    def unbounded_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "unboundedInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10808533863e447cb5dc53b4fa37231ea254f1e6a49e4b008480fde9af551779)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="envKey")
    def env_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envKey"))

    @env_key.setter
    def env_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__323b1ff4fe8e3eaa5c2115bb8f6b7ea8499b25ff89c5b736c0efd90fce7f803d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excluded")
    def excluded(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excluded"))

    @excluded.setter
    def excluded(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19e60e45c2bbb030828d74ae337f5482fcd13b79497b7bddf248f29f7832bec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excluded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74836c69194025a2e5a47cf7b7b3989881a9292002c9ab44dc2ec5a2ef3eded0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="included")
    def included(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "included"))

    @included.setter
    def included(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__638c1ac67406e1be872332ef10234be089b54b99bb0c3bb04093bf27aa955d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "included", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972183220ac2ca903524493b6a2697f4fa4284b787c42311215e98aee07b822a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e62587cae9d8bc0f747532e4c9c1820e419c8806d381e9d5b4fe0065d8530844)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="projectKey")
    def project_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "projectKey"))

    @project_key.setter
    def project_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a068bc909baee6163c7a5e9ad444b90e53eb4e09ff281269959d6d00bc6ee02e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "projectKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__911ebd837a1b598e965eaad4f090c94def3a768df1f5b589c5665d29192ec08d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unbounded")
    def unbounded(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "unbounded"))

    @unbounded.setter
    def unbounded(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4fe2d6ea955dc9489da335e41cde15f8f9ed4ee058d93d9cc7ed606cf4cacd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unbounded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unboundedContextKind")
    def unbounded_context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unboundedContextKind"))

    @unbounded_context_kind.setter
    def unbounded_context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa291c80629c1e4b00b9f39e3c5e4d7de6aaca0d5ab9d59fdcaceac4eae64733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unboundedContextKind", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentConfig",
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
        "key": "key",
        "name": "name",
        "project_key": "projectKey",
        "description": "description",
        "excluded": "excluded",
        "excluded_contexts": "excludedContexts",
        "id": "id",
        "included": "included",
        "included_contexts": "includedContexts",
        "rules": "rules",
        "tags": "tags",
        "unbounded": "unbounded",
        "unbounded_context_kind": "unboundedContextKind",
    },
)
class SegmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        key: builtins.str,
        name: builtins.str,
        project_key: builtins.str,
        description: typing.Optional[builtins.str] = None,
        excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
        excluded_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentExcludedContexts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        included: typing.Optional[typing.Sequence[builtins.str]] = None,
        included_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentIncludedContexts", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        unbounded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        unbounded_context_kind: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param env_key: The segment's environment key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#env_key Segment#env_key}
        :param key: The unique key that references the segment. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#key Segment#key}
        :param name: The human-friendly name for the segment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#name Segment#name}
        :param project_key: The segment's project key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#project_key Segment#project_key}
        :param description: The description of the segment's purpose. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#description Segment#description}
        :param excluded: List of user keys excluded from the segment. To target on other context kinds, use the excluded_contexts block attribute. This attribute is not valid when ``unbounded`` is set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#excluded Segment#excluded}
        :param excluded_contexts: excluded_contexts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#excluded_contexts Segment#excluded_contexts}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#id Segment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param included: List of user keys included in the segment. To target on other context kinds, use the included_contexts block attribute. This attribute is not valid when ``unbounded`` is set to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#included Segment#included}
        :param included_contexts: included_contexts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#included_contexts Segment#included_contexts}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#rules Segment#rules}
        :param tags: Tags associated with your resource. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#tags Segment#tags}
        :param unbounded: Whether to create a standard segment (``false``) or a Big Segment (``true``). Standard segments include rule-based and smaller list-based segments. Big Segments include larger list-based segments and synced segments. Only use a Big Segment if you need to add more than 15,000 individual targets. It is not possible to manage the list of targeted contexts for Big Segments with Terraform. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#unbounded Segment#unbounded}
        :param unbounded_context_kind: For Big Segments, the targeted context kind. If this attribute is not specified it will default to ``user``. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#unbounded_context_kind Segment#unbounded_context_kind}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6a1b3a85766111d2daacda6a12b49796357a0f41632344015ce3d5effeb417)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument env_key", value=env_key, expected_type=type_hints["env_key"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument project_key", value=project_key, expected_type=type_hints["project_key"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument excluded", value=excluded, expected_type=type_hints["excluded"])
            check_type(argname="argument excluded_contexts", value=excluded_contexts, expected_type=type_hints["excluded_contexts"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument included", value=included, expected_type=type_hints["included"])
            check_type(argname="argument included_contexts", value=included_contexts, expected_type=type_hints["included_contexts"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument unbounded", value=unbounded, expected_type=type_hints["unbounded"])
            check_type(argname="argument unbounded_context_kind", value=unbounded_context_kind, expected_type=type_hints["unbounded_context_kind"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env_key": env_key,
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
        if description is not None:
            self._values["description"] = description
        if excluded is not None:
            self._values["excluded"] = excluded
        if excluded_contexts is not None:
            self._values["excluded_contexts"] = excluded_contexts
        if id is not None:
            self._values["id"] = id
        if included is not None:
            self._values["included"] = included
        if included_contexts is not None:
            self._values["included_contexts"] = included_contexts
        if rules is not None:
            self._values["rules"] = rules
        if tags is not None:
            self._values["tags"] = tags
        if unbounded is not None:
            self._values["unbounded"] = unbounded
        if unbounded_context_kind is not None:
            self._values["unbounded_context_kind"] = unbounded_context_kind

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
        '''The segment's environment key.

        A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#env_key Segment#env_key}
        '''
        result = self._values.get("env_key")
        assert result is not None, "Required property 'env_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key(self) -> builtins.str:
        '''The unique key that references the segment.

        A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#key Segment#key}
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The human-friendly name for the segment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#name Segment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def project_key(self) -> builtins.str:
        '''The segment's project key.

        A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#project_key Segment#project_key}
        '''
        result = self._values.get("project_key")
        assert result is not None, "Required property 'project_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the segment's purpose.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#description Segment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excluded(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user keys excluded from the segment.

        To target on other context kinds, use the excluded_contexts block attribute. This attribute is not valid when ``unbounded`` is set to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#excluded Segment#excluded}
        '''
        result = self._values.get("excluded")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def excluded_contexts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentExcludedContexts"]]]:
        '''excluded_contexts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#excluded_contexts Segment#excluded_contexts}
        '''
        result = self._values.get("excluded_contexts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentExcludedContexts"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#id Segment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def included(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of user keys included in the segment.

        To target on other context kinds, use the included_contexts block attribute. This attribute is not valid when ``unbounded`` is set to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#included Segment#included}
        '''
        result = self._values.get("included")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def included_contexts(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentIncludedContexts"]]]:
        '''included_contexts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#included_contexts Segment#included_contexts}
        '''
        result = self._values.get("included_contexts")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentIncludedContexts"]]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#rules Segment#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentRules"]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Tags associated with your resource.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#tags Segment#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def unbounded(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to create a standard segment (``false``) or a Big Segment (``true``).

        Standard segments include rule-based and smaller list-based segments. Big Segments include larger list-based segments and synced segments. Only use a Big Segment if you need to add more than 15,000 individual targets. It is not possible to manage the list of targeted contexts for Big Segments with Terraform. A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#unbounded Segment#unbounded}
        '''
        result = self._values.get("unbounded")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def unbounded_context_kind(self) -> typing.Optional[builtins.str]:
        '''For Big Segments, the targeted context kind.

        If this attribute is not specified it will default to ``user``. A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#unbounded_context_kind Segment#unbounded_context_kind}
        '''
        result = self._values.get("unbounded_context_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SegmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentExcludedContexts",
    jsii_struct_bases=[],
    name_mapping={"context_kind": "contextKind", "values": "values"},
)
class SegmentExcludedContexts:
    def __init__(
        self,
        *,
        context_kind: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param context_kind: The context kind associated with this segment target. To target on user contexts, use the included and excluded attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#context_kind Segment#context_kind}
        :param values: List of target object keys included in or excluded from the segment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#values Segment#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28d6778735b2a7d16c2528dd49eb754dcee6d745bbd461138a998db1616f9b68)
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context_kind": context_kind,
            "values": values,
        }

    @builtins.property
    def context_kind(self) -> builtins.str:
        '''The context kind associated with this segment target. To target on user contexts, use the included and excluded attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#context_kind Segment#context_kind}
        '''
        result = self._values.get("context_kind")
        assert result is not None, "Required property 'context_kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''List of target object keys included in or excluded from the segment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#values Segment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SegmentExcludedContexts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SegmentExcludedContextsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentExcludedContextsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36cc54c13327182f201eebdc8a7c3ca2b75fad807536a4b9971b1bd4ff2c49c9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SegmentExcludedContextsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bc241251180cfe14bd34d4a1e2ead3d23d5e299fc7013532611a9452f3195f1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SegmentExcludedContextsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9302ed08b4698dd04e72171f48c3e3b80f4fe4ae4f9ae0a6b68463cabf260fce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__508e57afab79d754c7d4f10eb1e979be46da2051a3e17d71570fd65210177d8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8351b7b5e21a90fff7d7be55aaa9664849533870139ac38cefd2b9afee76e0ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentExcludedContexts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentExcludedContexts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentExcludedContexts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1394161dc347d9fcba57b57d0fd7caedeb26018a8dc2abefb70b5c626dbb83ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SegmentExcludedContextsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentExcludedContextsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7be7f4119a6bfffddc12b5112d10a29f13aadc1fbd208b4dd11e2461c8629b3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5da074124a7330468981ae70f16fd97de4121443761daf23c982daf660fb05ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984bf0e5853e2cfb9cf4b1fd9683aff33bbb185276649b41b45da4fa43242293)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentExcludedContexts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentExcludedContexts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentExcludedContexts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c503354bd333c45ed2fa89ab245d4c593dbfbbd5e40248fef4219e9eee1292d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentIncludedContexts",
    jsii_struct_bases=[],
    name_mapping={"context_kind": "contextKind", "values": "values"},
)
class SegmentIncludedContexts:
    def __init__(
        self,
        *,
        context_kind: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param context_kind: The context kind associated with this segment target. To target on user contexts, use the included and excluded attributes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#context_kind Segment#context_kind}
        :param values: List of target object keys included in or excluded from the segment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#values Segment#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25981c1c68a641a81bb8e7eb2bb2fd8444e6a3614ea2665574f3e24bb8f63f3)
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context_kind": context_kind,
            "values": values,
        }

    @builtins.property
    def context_kind(self) -> builtins.str:
        '''The context kind associated with this segment target. To target on user contexts, use the included and excluded attributes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#context_kind Segment#context_kind}
        '''
        result = self._values.get("context_kind")
        assert result is not None, "Required property 'context_kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''List of target object keys included in or excluded from the segment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#values Segment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SegmentIncludedContexts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SegmentIncludedContextsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentIncludedContextsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dabf521e29a19ed12c11350f967cab9c0b0ed5179b916ae0259c97a985045f03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SegmentIncludedContextsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b75445143c57546494b547b8973f8fc51351dfd3cf7e71e76ca4aba5c942889)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SegmentIncludedContextsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac8d1007b77ef5c2823f49e431395560e41b40461fcc5670d001dfdf3a5df37)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6057ca704004ae2ae8af4c833e30151cb534a29a77c8201952d113fc427c4d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20630f47f06f371fdc2e3fa399915a47136bac08ea6419c8e0c1e899c85b0141)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentIncludedContexts]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentIncludedContexts]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentIncludedContexts]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d090bdeb5a525c93599ffab0e0e030de63d465c7fa4a13f072ac175def3551dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SegmentIncludedContextsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentIncludedContextsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__838d3815208b8bb27903e61eaa30325bb180aba6f573d35a2e3624522150ab10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81fe752ab0f461f48d891b9191d5fa34714a7d87d90eb00ca9d76c934e625de5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca015d8320eb2fbfded71ff2f19d697e285417d80a7cdd43eafbec849f059dcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentIncludedContexts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentIncludedContexts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentIncludedContexts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fdfba33c2085fddeb8cea25766f1efe65c478436fe1dacd00ddb86f716d9347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentRules",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_by": "bucketBy",
        "clauses": "clauses",
        "rollout_context_kind": "rolloutContextKind",
        "weight": "weight",
    },
)
class SegmentRules:
    def __init__(
        self,
        *,
        bucket_by: typing.Optional[builtins.str] = None,
        clauses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SegmentRulesClauses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rollout_context_kind: typing.Optional[builtins.str] = None,
        weight: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket_by: The attribute by which to group contexts together. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#bucket_by Segment#bucket_by}
        :param clauses: clauses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#clauses Segment#clauses}
        :param rollout_context_kind: The context kind associated with this segment rule. This argument is only valid if ``weight`` is also specified. If omitted, defaults to ``user``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#rollout_context_kind Segment#rollout_context_kind}
        :param weight: The integer weight of the rule (between 1 and 100000). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#weight Segment#weight}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e16d3fe1514553328b2d7b966d78da4ae66991478e0688d26bf0bfb77386c3a)
            check_type(argname="argument bucket_by", value=bucket_by, expected_type=type_hints["bucket_by"])
            check_type(argname="argument clauses", value=clauses, expected_type=type_hints["clauses"])
            check_type(argname="argument rollout_context_kind", value=rollout_context_kind, expected_type=type_hints["rollout_context_kind"])
            check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_by is not None:
            self._values["bucket_by"] = bucket_by
        if clauses is not None:
            self._values["clauses"] = clauses
        if rollout_context_kind is not None:
            self._values["rollout_context_kind"] = rollout_context_kind
        if weight is not None:
            self._values["weight"] = weight

    @builtins.property
    def bucket_by(self) -> typing.Optional[builtins.str]:
        '''The attribute by which to group contexts together.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#bucket_by Segment#bucket_by}
        '''
        result = self._values.get("bucket_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clauses(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentRulesClauses"]]]:
        '''clauses block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#clauses Segment#clauses}
        '''
        result = self._values.get("clauses")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SegmentRulesClauses"]]], result)

    @builtins.property
    def rollout_context_kind(self) -> typing.Optional[builtins.str]:
        '''The context kind associated with this segment rule.

        This argument is only valid if ``weight`` is also specified. If omitted, defaults to ``user``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#rollout_context_kind Segment#rollout_context_kind}
        '''
        result = self._values.get("rollout_context_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weight(self) -> typing.Optional[jsii.Number]:
        '''The integer weight of the rule (between 1 and 100000).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#weight Segment#weight}
        '''
        result = self._values.get("weight")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SegmentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentRulesClauses",
    jsii_struct_bases=[],
    name_mapping={
        "attribute": "attribute",
        "op": "op",
        "values": "values",
        "context_kind": "contextKind",
        "negate": "negate",
        "value_type": "valueType",
    },
)
class SegmentRulesClauses:
    def __init__(
        self,
        *,
        attribute: builtins.str,
        op: builtins.str,
        values: typing.Sequence[builtins.str],
        context_kind: typing.Optional[builtins.str] = None,
        negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        value_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param attribute: The user attribute to operate on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#attribute Segment#attribute}
        :param op: The operator associated with the rule clause. Available options are ``in``, ``endsWith``, ``startsWith``, ``matches``, ``contains``, ``lessThan``, ``lessThanOrEqual``, ``greaterThanOrEqual``, ``before``, ``after``, ``segmentMatch``, ``semVerEqual``, ``semVerLessThan``, and ``semVerGreaterThan``. Read LaunchDarkly's `Operators <https://docs.launchdarkly.com/sdk/concepts/flag-evaluation-rules#operators>`_ documentation for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#op Segment#op}
        :param values: The list of values associated with the rule clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#values Segment#values}
        :param context_kind: The context kind associated with this rule clause. If omitted, defaults to ``user``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#context_kind Segment#context_kind}
        :param negate: Whether to negate the rule clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#negate Segment#negate}
        :param value_type: The type for each of the clause's values. Available types are ``boolean``, ``string``, and ``number``. If omitted, ``value_type`` defaults to ``string``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#value_type Segment#value_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7311c90332c47a9e3d1696d4575bebbeef73a3698887bf8aaab7fd21a18d62c3)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument op", value=op, expected_type=type_hints["op"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument negate", value=negate, expected_type=type_hints["negate"])
            check_type(argname="argument value_type", value=value_type, expected_type=type_hints["value_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute": attribute,
            "op": op,
            "values": values,
        }
        if context_kind is not None:
            self._values["context_kind"] = context_kind
        if negate is not None:
            self._values["negate"] = negate
        if value_type is not None:
            self._values["value_type"] = value_type

    @builtins.property
    def attribute(self) -> builtins.str:
        '''The user attribute to operate on.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#attribute Segment#attribute}
        '''
        result = self._values.get("attribute")
        assert result is not None, "Required property 'attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def op(self) -> builtins.str:
        '''The operator associated with the rule clause.

        Available options are ``in``, ``endsWith``, ``startsWith``, ``matches``, ``contains``, ``lessThan``, ``lessThanOrEqual``, ``greaterThanOrEqual``, ``before``, ``after``, ``segmentMatch``, ``semVerEqual``, ``semVerLessThan``, and ``semVerGreaterThan``. Read LaunchDarkly's `Operators <https://docs.launchdarkly.com/sdk/concepts/flag-evaluation-rules#operators>`_ documentation for more information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#op Segment#op}
        '''
        result = self._values.get("op")
        assert result is not None, "Required property 'op' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The list of values associated with the rule clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#values Segment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context_kind(self) -> typing.Optional[builtins.str]:
        '''The context kind associated with this rule clause. If omitted, defaults to ``user``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#context_kind Segment#context_kind}
        '''
        result = self._values.get("context_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to negate the rule clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#negate Segment#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def value_type(self) -> typing.Optional[builtins.str]:
        '''The type for each of the clause's values.

        Available types are ``boolean``, ``string``, and ``number``. If omitted, ``value_type`` defaults to ``string``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/segment#value_type Segment#value_type}
        '''
        result = self._values.get("value_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SegmentRulesClauses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SegmentRulesClausesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentRulesClausesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__37e6e834f90a57225ac8a51a0c5ef11a9034822b5f7d50241e494d107b0cc4d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SegmentRulesClausesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520013fe1f86426e682b670689e8953953e7f19d0382558eb7d5583c73541800)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SegmentRulesClausesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8d199f2aed11bf68c14dc4cb21f466fd0e6f62272a725ef12cbf69b7889e0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2432ba8558fb833b7458a72597659e96c81ca7e71e6735837e9cc3db68c4949b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be36a7b20c5618cae1ad49672682356d1ba4337c49bf0e100f5946424bfb9a43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRulesClauses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRulesClauses]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRulesClauses]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d8fc751b4c0acbd03ba1dca4108286efc221d1bd23fb39494d86118a876e28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SegmentRulesClausesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentRulesClausesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__79ceee240cbdb0e898cf798a0503ef50529f92d0ad5282d299224122796e112e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetContextKind")
    def reset_context_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextKind", []))

    @jsii.member(jsii_name="resetNegate")
    def reset_negate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNegate", []))

    @jsii.member(jsii_name="resetValueType")
    def reset_value_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValueType", []))

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="negateInput")
    def negate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "negateInput"))

    @builtins.property
    @jsii.member(jsii_name="opInput")
    def op_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "opInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="valueTypeInput")
    def value_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__840874554b4ddd00f5e6a1bf08bf6188eae1a1866b4352664daba1937c26438e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a619b5661297e37d5bbc37f3c9701fd68436270ab7961965122671644112f8e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="negate")
    def negate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "negate"))

    @negate.setter
    def negate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a59ffdc8c2a4fc51ee6932d3844ae876236027fa8925443c93a543d5d802c3a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="op")
    def op(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "op"))

    @op.setter
    def op(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc4caec6c4d894a0ad177f2a69f893604bdaa0d1c4fc0e5940855ef0606b5c1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "op", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72fcdaf3901d608053fb541033cd1a3c8ceab62cd41325cd09ca6a931560c2a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__982f17cb63de669925da6cff914cce3fc2ae7cda07931c2a6beda89d76bb365d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentRulesClauses]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentRulesClauses]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentRulesClauses]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ccdbf8a7b257ca7faacf2163a7cdb71f4d159bb8597b16b32c8988134cf1c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SegmentRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f2f963ec9131024b552e6d34b23b08e43031a67009d1fd2b9586a46a9e364c0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SegmentRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e802f8f6c050d9df2646a4a8e3985e5c870006587412666e90573da8dbaf1a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SegmentRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37c98ec075c6f17ba2028f3109d47aedd40edb14310ed157e70bf47cfd037ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28adbdfa3481071a77d31a742191b7bbc65cc91a207dc763ec885aff5bd4dd49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d6ad854a56d8528fd52362afed284d30bcec31fcf2cd3c9ac4fd0e2127a9c56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad525976ba098e33df9affad54e45a149eadc8f25937f4f0ee483cf6d466b614)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SegmentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.segment.SegmentRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02c6eaf82882501f6cb408c80f7eb7759f53997db68f07cf3c3cdd1b8a6c8bf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putClauses")
    def put_clauses(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e277627e131a0d72ee3420b34cb4fe727c725bacbbd9fedb83db0a8888318d04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClauses", [value]))

    @jsii.member(jsii_name="resetBucketBy")
    def reset_bucket_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketBy", []))

    @jsii.member(jsii_name="resetClauses")
    def reset_clauses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClauses", []))

    @jsii.member(jsii_name="resetRolloutContextKind")
    def reset_rollout_context_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutContextKind", []))

    @jsii.member(jsii_name="resetWeight")
    def reset_weight(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeight", []))

    @builtins.property
    @jsii.member(jsii_name="clauses")
    def clauses(self) -> SegmentRulesClausesList:
        return typing.cast(SegmentRulesClausesList, jsii.get(self, "clauses"))

    @builtins.property
    @jsii.member(jsii_name="bucketByInput")
    def bucket_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketByInput"))

    @builtins.property
    @jsii.member(jsii_name="clausesInput")
    def clauses_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRulesClauses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRulesClauses]]], jsii.get(self, "clausesInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutContextKindInput")
    def rollout_context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rolloutContextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="weightInput")
    def weight_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "weightInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketBy")
    def bucket_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketBy"))

    @bucket_by.setter
    def bucket_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bbdf3e4ca1b3a62253e8f4142845d0f5912e5fa0f77b133336bb2681f6d7324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rolloutContextKind")
    def rollout_context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rolloutContextKind"))

    @rollout_context_kind.setter
    def rollout_context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d2cfdb405a07be201ae6af9815de36430185f5be4b360a655774025bd921a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolloutContextKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weight")
    def weight(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "weight"))

    @weight.setter
    def weight(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49d53b1c5e91d10eddf67eb8986fba41b3e83f095b5ddc36cc9acf007f719eb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weight", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f6cda2dc633661012ce0192e13b12463d58aed98304e71a3d95dc5c17d31951)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Segment",
    "SegmentConfig",
    "SegmentExcludedContexts",
    "SegmentExcludedContextsList",
    "SegmentExcludedContextsOutputReference",
    "SegmentIncludedContexts",
    "SegmentIncludedContextsList",
    "SegmentIncludedContextsOutputReference",
    "SegmentRules",
    "SegmentRulesClauses",
    "SegmentRulesClausesList",
    "SegmentRulesClausesOutputReference",
    "SegmentRulesList",
    "SegmentRulesOutputReference",
]

publication.publish()

def _typecheckingstub__0bc761ed5b800bcee541f20c7692dc1475952f2b353da4883a658b8141010ac2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    env_key: builtins.str,
    key: builtins.str,
    name: builtins.str,
    project_key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentExcludedContexts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    included: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentIncludedContexts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    unbounded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unbounded_context_kind: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__d563361b02e46803ed18c62be8732cd1f4164094a27ac1ef01893574d839b092(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292578362c5fea7cdb24974843f5dda598e915c5c2d62b433024dac504b7fc3e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentExcludedContexts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff1731f8af72d01eb4be94e7c281818f22ae80fccfb354f34f9b4a5b3196c78(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentIncludedContexts, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__465042511387850a47b69228bb63e77c0768a0ecf5e46049422eda7891034b02(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10808533863e447cb5dc53b4fa37231ea254f1e6a49e4b008480fde9af551779(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__323b1ff4fe8e3eaa5c2115bb8f6b7ea8499b25ff89c5b736c0efd90fce7f803d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e60e45c2bbb030828d74ae337f5482fcd13b79497b7bddf248f29f7832bec2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74836c69194025a2e5a47cf7b7b3989881a9292002c9ab44dc2ec5a2ef3eded0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__638c1ac67406e1be872332ef10234be089b54b99bb0c3bb04093bf27aa955d0d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972183220ac2ca903524493b6a2697f4fa4284b787c42311215e98aee07b822a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e62587cae9d8bc0f747532e4c9c1820e419c8806d381e9d5b4fe0065d8530844(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a068bc909baee6163c7a5e9ad444b90e53eb4e09ff281269959d6d00bc6ee02e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__911ebd837a1b598e965eaad4f090c94def3a768df1f5b589c5665d29192ec08d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4fe2d6ea955dc9489da335e41cde15f8f9ed4ee058d93d9cc7ed606cf4cacd7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa291c80629c1e4b00b9f39e3c5e4d7de6aaca0d5ab9d59fdcaceac4eae64733(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6a1b3a85766111d2daacda6a12b49796357a0f41632344015ce3d5effeb417(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    env_key: builtins.str,
    key: builtins.str,
    name: builtins.str,
    project_key: builtins.str,
    description: typing.Optional[builtins.str] = None,
    excluded: typing.Optional[typing.Sequence[builtins.str]] = None,
    excluded_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentExcludedContexts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    included: typing.Optional[typing.Sequence[builtins.str]] = None,
    included_contexts: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentIncludedContexts, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    unbounded: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    unbounded_context_kind: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28d6778735b2a7d16c2528dd49eb754dcee6d745bbd461138a998db1616f9b68(
    *,
    context_kind: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cc54c13327182f201eebdc8a7c3ca2b75fad807536a4b9971b1bd4ff2c49c9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bc241251180cfe14bd34d4a1e2ead3d23d5e299fc7013532611a9452f3195f1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9302ed08b4698dd04e72171f48c3e3b80f4fe4ae4f9ae0a6b68463cabf260fce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__508e57afab79d754c7d4f10eb1e979be46da2051a3e17d71570fd65210177d8c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8351b7b5e21a90fff7d7be55aaa9664849533870139ac38cefd2b9afee76e0ba(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1394161dc347d9fcba57b57d0fd7caedeb26018a8dc2abefb70b5c626dbb83ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentExcludedContexts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be7f4119a6bfffddc12b5112d10a29f13aadc1fbd208b4dd11e2461c8629b3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da074124a7330468981ae70f16fd97de4121443761daf23c982daf660fb05ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984bf0e5853e2cfb9cf4b1fd9683aff33bbb185276649b41b45da4fa43242293(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c503354bd333c45ed2fa89ab245d4c593dbfbbd5e40248fef4219e9eee1292d0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentExcludedContexts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25981c1c68a641a81bb8e7eb2bb2fd8444e6a3614ea2665574f3e24bb8f63f3(
    *,
    context_kind: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dabf521e29a19ed12c11350f967cab9c0b0ed5179b916ae0259c97a985045f03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b75445143c57546494b547b8973f8fc51351dfd3cf7e71e76ca4aba5c942889(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac8d1007b77ef5c2823f49e431395560e41b40461fcc5670d001dfdf3a5df37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6057ca704004ae2ae8af4c833e30151cb534a29a77c8201952d113fc427c4d9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20630f47f06f371fdc2e3fa399915a47136bac08ea6419c8e0c1e899c85b0141(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d090bdeb5a525c93599ffab0e0e030de63d465c7fa4a13f072ac175def3551dc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentIncludedContexts]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838d3815208b8bb27903e61eaa30325bb180aba6f573d35a2e3624522150ab10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81fe752ab0f461f48d891b9191d5fa34714a7d87d90eb00ca9d76c934e625de5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca015d8320eb2fbfded71ff2f19d697e285417d80a7cdd43eafbec849f059dcc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fdfba33c2085fddeb8cea25766f1efe65c478436fe1dacd00ddb86f716d9347(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentIncludedContexts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e16d3fe1514553328b2d7b966d78da4ae66991478e0688d26bf0bfb77386c3a(
    *,
    bucket_by: typing.Optional[builtins.str] = None,
    clauses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rollout_context_kind: typing.Optional[builtins.str] = None,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7311c90332c47a9e3d1696d4575bebbeef73a3698887bf8aaab7fd21a18d62c3(
    *,
    attribute: builtins.str,
    op: builtins.str,
    values: typing.Sequence[builtins.str],
    context_kind: typing.Optional[builtins.str] = None,
    negate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    value_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e6e834f90a57225ac8a51a0c5ef11a9034822b5f7d50241e494d107b0cc4d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520013fe1f86426e682b670689e8953953e7f19d0382558eb7d5583c73541800(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8d199f2aed11bf68c14dc4cb21f466fd0e6f62272a725ef12cbf69b7889e0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2432ba8558fb833b7458a72597659e96c81ca7e71e6735837e9cc3db68c4949b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be36a7b20c5618cae1ad49672682356d1ba4337c49bf0e100f5946424bfb9a43(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d8fc751b4c0acbd03ba1dca4108286efc221d1bd23fb39494d86118a876e28(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRulesClauses]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ceee240cbdb0e898cf798a0503ef50529f92d0ad5282d299224122796e112e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__840874554b4ddd00f5e6a1bf08bf6188eae1a1866b4352664daba1937c26438e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a619b5661297e37d5bbc37f3c9701fd68436270ab7961965122671644112f8e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a59ffdc8c2a4fc51ee6932d3844ae876236027fa8925443c93a543d5d802c3a1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc4caec6c4d894a0ad177f2a69f893604bdaa0d1c4fc0e5940855ef0606b5c1e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72fcdaf3901d608053fb541033cd1a3c8ceab62cd41325cd09ca6a931560c2a6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__982f17cb63de669925da6cff914cce3fc2ae7cda07931c2a6beda89d76bb365d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ccdbf8a7b257ca7faacf2163a7cdb71f4d159bb8597b16b32c8988134cf1c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentRulesClauses]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2f963ec9131024b552e6d34b23b08e43031a67009d1fd2b9586a46a9e364c0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e802f8f6c050d9df2646a4a8e3985e5c870006587412666e90573da8dbaf1a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37c98ec075c6f17ba2028f3109d47aedd40edb14310ed157e70bf47cfd037ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28adbdfa3481071a77d31a742191b7bbc65cc91a207dc763ec885aff5bd4dd49(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d6ad854a56d8528fd52362afed284d30bcec31fcf2cd3c9ac4fd0e2127a9c56(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad525976ba098e33df9affad54e45a149eadc8f25937f4f0ee483cf6d466b614(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SegmentRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02c6eaf82882501f6cb408c80f7eb7759f53997db68f07cf3c3cdd1b8a6c8bf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e277627e131a0d72ee3420b34cb4fe727c725bacbbd9fedb83db0a8888318d04(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SegmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bbdf3e4ca1b3a62253e8f4142845d0f5912e5fa0f77b133336bb2681f6d7324(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d2cfdb405a07be201ae6af9815de36430185f5be4b360a655774025bd921a80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d53b1c5e91d10eddf67eb8986fba41b3e83f095b5ddc36cc9acf007f719eb1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6cda2dc633661012ce0192e13b12463d58aed98304e71a3d95dc5c17d31951(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SegmentRules]],
) -> None:
    """Type checking stubs"""
    pass
