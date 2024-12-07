r'''
# `launchdarkly_feature_flag_environment`

Refer to the Terraform Registry for docs: [`launchdarkly_feature_flag_environment`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment).
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


class FeatureFlagEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment launchdarkly_feature_flag_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        env_key: builtins.str,
        fallthrough: typing.Union["FeatureFlagEnvironmentFallthrough", typing.Dict[builtins.str, typing.Any]],
        flag_id: builtins.str,
        off_variation: jsii.Number,
        context_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentContextTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prerequisites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentPrerequisites", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment launchdarkly_feature_flag_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param env_key: The environment key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#env_key FeatureFlagEnvironment#env_key}
        :param fallthrough: fallthrough block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#fallthrough FeatureFlagEnvironment#fallthrough}
        :param flag_id: The feature flag's unique ``id`` in the format ``project_key/flag_key``. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#flag_id FeatureFlagEnvironment#flag_id}
        :param off_variation: The index of the variation to serve if targeting is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#off_variation FeatureFlagEnvironment#off_variation}
        :param context_targets: context_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_targets FeatureFlagEnvironment#context_targets}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#id FeatureFlagEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on: Whether targeting is enabled. Defaults to ``false`` if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#on FeatureFlagEnvironment#on}
        :param prerequisites: prerequisites block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#prerequisites FeatureFlagEnvironment#prerequisites}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#rules FeatureFlagEnvironment#rules}
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#targets FeatureFlagEnvironment#targets}
        :param track_events: Whether to send event data back to LaunchDarkly. Defaults to ``false`` if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#track_events FeatureFlagEnvironment#track_events}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7acf209bd69aa69b558e650d96f2255ad49897f02e3ff67d3e391cefa26d15)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FeatureFlagEnvironmentConfig(
            env_key=env_key,
            fallthrough=fallthrough,
            flag_id=flag_id,
            off_variation=off_variation,
            context_targets=context_targets,
            id=id,
            on=on,
            prerequisites=prerequisites,
            rules=rules,
            targets=targets,
            track_events=track_events,
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
        '''Generates CDKTF code for importing a FeatureFlagEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FeatureFlagEnvironment to import.
        :param import_from_id: The id of the existing FeatureFlagEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FeatureFlagEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f298d44f2c9d889c80ebdfd75b63176802aab1902827bcbd69fc9cc192e5c4fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putContextTargets")
    def put_context_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentContextTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8fa67162131bccf10ab78de185fdfc38e7299d843230aef6eaa279e05514298)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContextTargets", [value]))

    @jsii.member(jsii_name="putFallthrough")
    def put_fallthrough(
        self,
        *,
        bucket_by: typing.Optional[builtins.str] = None,
        context_kind: typing.Optional[builtins.str] = None,
        rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
        variation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket_by: Group percentage rollout by a custom attribute. This argument is only valid if rollout_weights is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#bucket_by FeatureFlagEnvironment#bucket_by}
        :param context_kind: The context kind associated with the specified rollout. This argument is only valid if rollout_weights is also specified. If omitted, defaults to ``user``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_kind FeatureFlagEnvironment#context_kind}
        :param rollout_weights: List of integer percentage rollout weights (in thousandths of a percent) to apply to each variation if the rule clauses evaluates to ``true``. The sum of the ``rollout_weights`` must equal 100000 and the number of rollout weights specified in the array must match the number of flag variations. You must specify either ``variation`` or ``rollout_weights``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#rollout_weights FeatureFlagEnvironment#rollout_weights}
        :param variation: The default integer variation index to serve if no ``prerequisites``, ``target``, or ``rules`` apply. You must specify either ``variation`` or ``rollout_weights``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        value = FeatureFlagEnvironmentFallthrough(
            bucket_by=bucket_by,
            context_kind=context_kind,
            rollout_weights=rollout_weights,
            variation=variation,
        )

        return typing.cast(None, jsii.invoke(self, "putFallthrough", [value]))

    @jsii.member(jsii_name="putPrerequisites")
    def put_prerequisites(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentPrerequisites", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcbadc95b49375ad001ed00bb2a1775ce4071bbd241dd04fa7054e79627abf6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPrerequisites", [value]))

    @jsii.member(jsii_name="putRules")
    def put_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77872a0530ffe9579697e63a7a198164725b0028c844a144e5642095cd2ecec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRules", [value]))

    @jsii.member(jsii_name="putTargets")
    def put_targets(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentTargets", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6266f80c43d52f43d4222496da0a2ba72d9e9182f21d25750021a693de389bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTargets", [value]))

    @jsii.member(jsii_name="resetContextTargets")
    def reset_context_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextTargets", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetOn")
    def reset_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOn", []))

    @jsii.member(jsii_name="resetPrerequisites")
    def reset_prerequisites(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrerequisites", []))

    @jsii.member(jsii_name="resetRules")
    def reset_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRules", []))

    @jsii.member(jsii_name="resetTargets")
    def reset_targets(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargets", []))

    @jsii.member(jsii_name="resetTrackEvents")
    def reset_track_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrackEvents", []))

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
    def context_targets(self) -> "FeatureFlagEnvironmentContextTargetsList":
        return typing.cast("FeatureFlagEnvironmentContextTargetsList", jsii.get(self, "contextTargets"))

    @builtins.property
    @jsii.member(jsii_name="fallthrough")
    def fallthrough(self) -> "FeatureFlagEnvironmentFallthroughOutputReference":
        return typing.cast("FeatureFlagEnvironmentFallthroughOutputReference", jsii.get(self, "fallthrough"))

    @builtins.property
    @jsii.member(jsii_name="prerequisites")
    def prerequisites(self) -> "FeatureFlagEnvironmentPrerequisitesList":
        return typing.cast("FeatureFlagEnvironmentPrerequisitesList", jsii.get(self, "prerequisites"))

    @builtins.property
    @jsii.member(jsii_name="rules")
    def rules(self) -> "FeatureFlagEnvironmentRulesList":
        return typing.cast("FeatureFlagEnvironmentRulesList", jsii.get(self, "rules"))

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(self) -> "FeatureFlagEnvironmentTargetsList":
        return typing.cast("FeatureFlagEnvironmentTargetsList", jsii.get(self, "targets"))

    @builtins.property
    @jsii.member(jsii_name="contextTargetsInput")
    def context_targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentContextTargets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentContextTargets"]]], jsii.get(self, "contextTargetsInput"))

    @builtins.property
    @jsii.member(jsii_name="envKeyInput")
    def env_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "envKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="fallthroughInput")
    def fallthrough_input(self) -> typing.Optional["FeatureFlagEnvironmentFallthrough"]:
        return typing.cast(typing.Optional["FeatureFlagEnvironmentFallthrough"], jsii.get(self, "fallthroughInput"))

    @builtins.property
    @jsii.member(jsii_name="flagIdInput")
    def flag_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flagIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="offVariationInput")
    def off_variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "offVariationInput"))

    @builtins.property
    @jsii.member(jsii_name="onInput")
    def on_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "onInput"))

    @builtins.property
    @jsii.member(jsii_name="prerequisitesInput")
    def prerequisites_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentPrerequisites"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentPrerequisites"]]], jsii.get(self, "prerequisitesInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesInput")
    def rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentRules"]]], jsii.get(self, "rulesInput"))

    @builtins.property
    @jsii.member(jsii_name="targetsInput")
    def targets_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentTargets"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentTargets"]]], jsii.get(self, "targetsInput"))

    @builtins.property
    @jsii.member(jsii_name="trackEventsInput")
    def track_events_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trackEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="envKey")
    def env_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "envKey"))

    @env_key.setter
    def env_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ecf7009104d88f74c3c8fe74599e52a39ba4bfe7bbb464b94d380d27e6a732e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "envKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="flagId")
    def flag_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flagId"))

    @flag_id.setter
    def flag_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecca6489e3220d4e374f8131b9089b3be6d2d537fe4ca535b9839c60e0e491a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flagId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e6039817c6551b855bf97b27d6475b3a97a01e8fe07ea43436f8591ebaee21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="offVariation")
    def off_variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "offVariation"))

    @off_variation.setter
    def off_variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0bee136dd1e83f251fadc79add8c554fb14b43f5294905bd51125266f73aceb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "offVariation", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__31d1d62764ffafaef27890ee4fb19b32d2e6f655d2fb5120a4203c0752bc5db7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "on", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="trackEvents")
    def track_events(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trackEvents"))

    @track_events.setter
    def track_events(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8344799f82ac2188814e25b380130110d81f479811df24bf4e7bfb7c46cd8b2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackEvents", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentConfig",
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
        "fallthrough": "fallthrough",
        "flag_id": "flagId",
        "off_variation": "offVariation",
        "context_targets": "contextTargets",
        "id": "id",
        "on": "on",
        "prerequisites": "prerequisites",
        "rules": "rules",
        "targets": "targets",
        "track_events": "trackEvents",
    },
)
class FeatureFlagEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        fallthrough: typing.Union["FeatureFlagEnvironmentFallthrough", typing.Dict[builtins.str, typing.Any]],
        flag_id: builtins.str,
        off_variation: jsii.Number,
        context_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentContextTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        prerequisites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentPrerequisites", typing.Dict[builtins.str, typing.Any]]]]] = None,
        rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentTargets", typing.Dict[builtins.str, typing.Any]]]]] = None,
        track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param env_key: The environment key. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#env_key FeatureFlagEnvironment#env_key}
        :param fallthrough: fallthrough block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#fallthrough FeatureFlagEnvironment#fallthrough}
        :param flag_id: The feature flag's unique ``id`` in the format ``project_key/flag_key``. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#flag_id FeatureFlagEnvironment#flag_id}
        :param off_variation: The index of the variation to serve if targeting is disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#off_variation FeatureFlagEnvironment#off_variation}
        :param context_targets: context_targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_targets FeatureFlagEnvironment#context_targets}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#id FeatureFlagEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param on: Whether targeting is enabled. Defaults to ``false`` if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#on FeatureFlagEnvironment#on}
        :param prerequisites: prerequisites block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#prerequisites FeatureFlagEnvironment#prerequisites}
        :param rules: rules block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#rules FeatureFlagEnvironment#rules}
        :param targets: targets block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#targets FeatureFlagEnvironment#targets}
        :param track_events: Whether to send event data back to LaunchDarkly. Defaults to ``false`` if not set. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#track_events FeatureFlagEnvironment#track_events}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(fallthrough, dict):
            fallthrough = FeatureFlagEnvironmentFallthrough(**fallthrough)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7906af57752c788e0f057973f44c65cc16cb2d8bdf337d01f76caefb9503b806)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument env_key", value=env_key, expected_type=type_hints["env_key"])
            check_type(argname="argument fallthrough", value=fallthrough, expected_type=type_hints["fallthrough"])
            check_type(argname="argument flag_id", value=flag_id, expected_type=type_hints["flag_id"])
            check_type(argname="argument off_variation", value=off_variation, expected_type=type_hints["off_variation"])
            check_type(argname="argument context_targets", value=context_targets, expected_type=type_hints["context_targets"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument on", value=on, expected_type=type_hints["on"])
            check_type(argname="argument prerequisites", value=prerequisites, expected_type=type_hints["prerequisites"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument track_events", value=track_events, expected_type=type_hints["track_events"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "env_key": env_key,
            "fallthrough": fallthrough,
            "flag_id": flag_id,
            "off_variation": off_variation,
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
        if context_targets is not None:
            self._values["context_targets"] = context_targets
        if id is not None:
            self._values["id"] = id
        if on is not None:
            self._values["on"] = on
        if prerequisites is not None:
            self._values["prerequisites"] = prerequisites
        if rules is not None:
            self._values["rules"] = rules
        if targets is not None:
            self._values["targets"] = targets
        if track_events is not None:
            self._values["track_events"] = track_events

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

        A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#env_key FeatureFlagEnvironment#env_key}
        '''
        result = self._values.get("env_key")
        assert result is not None, "Required property 'env_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def fallthrough(self) -> "FeatureFlagEnvironmentFallthrough":
        '''fallthrough block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#fallthrough FeatureFlagEnvironment#fallthrough}
        '''
        result = self._values.get("fallthrough")
        assert result is not None, "Required property 'fallthrough' is missing"
        return typing.cast("FeatureFlagEnvironmentFallthrough", result)

    @builtins.property
    def flag_id(self) -> builtins.str:
        '''The feature flag's unique ``id`` in the format ``project_key/flag_key``.

        A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#flag_id FeatureFlagEnvironment#flag_id}
        '''
        result = self._values.get("flag_id")
        assert result is not None, "Required property 'flag_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def off_variation(self) -> jsii.Number:
        '''The index of the variation to serve if targeting is disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#off_variation FeatureFlagEnvironment#off_variation}
        '''
        result = self._values.get("off_variation")
        assert result is not None, "Required property 'off_variation' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def context_targets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentContextTargets"]]]:
        '''context_targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_targets FeatureFlagEnvironment#context_targets}
        '''
        result = self._values.get("context_targets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentContextTargets"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#id FeatureFlagEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether targeting is enabled. Defaults to ``false`` if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#on FeatureFlagEnvironment#on}
        '''
        result = self._values.get("on")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def prerequisites(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentPrerequisites"]]]:
        '''prerequisites block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#prerequisites FeatureFlagEnvironment#prerequisites}
        '''
        result = self._values.get("prerequisites")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentPrerequisites"]]], result)

    @builtins.property
    def rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentRules"]]]:
        '''rules block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#rules FeatureFlagEnvironment#rules}
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentRules"]]], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentTargets"]]]:
        '''targets block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#targets FeatureFlagEnvironment#targets}
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentTargets"]]], result)

    @builtins.property
    def track_events(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to send event data back to LaunchDarkly. Defaults to ``false`` if not set.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#track_events FeatureFlagEnvironment#track_events}
        '''
        result = self._values.get("track_events")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FeatureFlagEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentContextTargets",
    jsii_struct_bases=[],
    name_mapping={
        "context_kind": "contextKind",
        "values": "values",
        "variation": "variation",
    },
)
class FeatureFlagEnvironmentContextTargets:
    def __init__(
        self,
        *,
        context_kind: builtins.str,
        values: typing.Sequence[builtins.str],
        variation: jsii.Number,
    ) -> None:
        '''
        :param context_kind: The context kind on which the flag should target in this environment. User (``user``) targets should be specified as ``targets`` attribute blocks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_kind FeatureFlagEnvironment#context_kind}
        :param values: List of ``user`` strings to target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#values FeatureFlagEnvironment#values}
        :param variation: The index of the variation to serve if a user target value is matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b5642f26bcae6d4dc7221ef36abd376437c6e3e3763e1e7abb20f783bf5eba)
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "context_kind": context_kind,
            "values": values,
            "variation": variation,
        }

    @builtins.property
    def context_kind(self) -> builtins.str:
        '''The context kind on which the flag should target in this environment.

        User (``user``) targets should be specified as ``targets`` attribute blocks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_kind FeatureFlagEnvironment#context_kind}
        '''
        result = self._values.get("context_kind")
        assert result is not None, "Required property 'context_kind' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''List of ``user`` strings to target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#values FeatureFlagEnvironment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def variation(self) -> jsii.Number:
        '''The index of the variation to serve if a user target value is matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        assert result is not None, "Required property 'variation' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FeatureFlagEnvironmentContextTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FeatureFlagEnvironmentContextTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentContextTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__014195db03da4413c55abb6428f7cc4552305f02b1380565b531f38cb46e9904)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FeatureFlagEnvironmentContextTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dceb5f83ff1a3c78dc20bac4b03d81787ee0246885f7e6eff6dfa33e7f8eb586)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FeatureFlagEnvironmentContextTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2896c2bc48bdd8e6846d65975e617e76847c317ad3e97c56b77e195c9fa6f056)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab92986c0449eea4c9ced16a53a522c3bcfe52a166b098f15d8b7a788d626e95)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47a5232063d3375bd7d0f2a32a775b47da2cef21e126af0b1bc44522b00c7ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentContextTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentContextTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentContextTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf59c6d6d821a092c9517090f4ff4f0a02e8006b8c657db2c54c8b75b578cec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FeatureFlagEnvironmentContextTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentContextTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__196e0be39467781a01b354830174e9e5be6065c7ec1e7a436cbbb87906441848)
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
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__898404979c9cc8de60d9b43c8409473de6e2cb1e41ba840f409bd6f8168837da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c4c33d37cdbdff37615362df5de1d5de357535157a2317adfc799feb96ce30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec35e998cb1e2178046f7db9d4146308e9bb63c74dc3a50e311b5ee767e6142d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentContextTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentContextTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentContextTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9d3f5cfb43022bdef6576bb3e9003fe4c96408185e0eb733f290d1ac5cc583)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentFallthrough",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_by": "bucketBy",
        "context_kind": "contextKind",
        "rollout_weights": "rolloutWeights",
        "variation": "variation",
    },
)
class FeatureFlagEnvironmentFallthrough:
    def __init__(
        self,
        *,
        bucket_by: typing.Optional[builtins.str] = None,
        context_kind: typing.Optional[builtins.str] = None,
        rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
        variation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket_by: Group percentage rollout by a custom attribute. This argument is only valid if rollout_weights is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#bucket_by FeatureFlagEnvironment#bucket_by}
        :param context_kind: The context kind associated with the specified rollout. This argument is only valid if rollout_weights is also specified. If omitted, defaults to ``user``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_kind FeatureFlagEnvironment#context_kind}
        :param rollout_weights: List of integer percentage rollout weights (in thousandths of a percent) to apply to each variation if the rule clauses evaluates to ``true``. The sum of the ``rollout_weights`` must equal 100000 and the number of rollout weights specified in the array must match the number of flag variations. You must specify either ``variation`` or ``rollout_weights``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#rollout_weights FeatureFlagEnvironment#rollout_weights}
        :param variation: The default integer variation index to serve if no ``prerequisites``, ``target``, or ``rules`` apply. You must specify either ``variation`` or ``rollout_weights``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf881e63563456bfb70bbbeb289ea98f58d399b5ee497dbb67f9a344a45c1c2)
            check_type(argname="argument bucket_by", value=bucket_by, expected_type=type_hints["bucket_by"])
            check_type(argname="argument context_kind", value=context_kind, expected_type=type_hints["context_kind"])
            check_type(argname="argument rollout_weights", value=rollout_weights, expected_type=type_hints["rollout_weights"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_by is not None:
            self._values["bucket_by"] = bucket_by
        if context_kind is not None:
            self._values["context_kind"] = context_kind
        if rollout_weights is not None:
            self._values["rollout_weights"] = rollout_weights
        if variation is not None:
            self._values["variation"] = variation

    @builtins.property
    def bucket_by(self) -> typing.Optional[builtins.str]:
        '''Group percentage rollout by a custom attribute. This argument is only valid if rollout_weights is also specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#bucket_by FeatureFlagEnvironment#bucket_by}
        '''
        result = self._values.get("bucket_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def context_kind(self) -> typing.Optional[builtins.str]:
        '''The context kind associated with the specified rollout.

        This argument is only valid if rollout_weights is also specified. If omitted, defaults to ``user``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_kind FeatureFlagEnvironment#context_kind}
        '''
        result = self._values.get("context_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rollout_weights(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''List of integer percentage rollout weights (in thousandths of a percent) to apply to each variation if the rule clauses evaluates to ``true``.

        The sum of the ``rollout_weights`` must equal 100000 and the number of rollout weights specified in the array must match the number of flag variations. You must specify either ``variation`` or ``rollout_weights``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#rollout_weights FeatureFlagEnvironment#rollout_weights}
        '''
        result = self._values.get("rollout_weights")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def variation(self) -> typing.Optional[jsii.Number]:
        '''The default integer variation index to serve if no ``prerequisites``, ``target``, or ``rules`` apply.

        You must specify either ``variation`` or ``rollout_weights``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FeatureFlagEnvironmentFallthrough(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FeatureFlagEnvironmentFallthroughOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentFallthroughOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cb20c5fef881c08623a269ea8889a326a44fab7e90780a9269e4b97686178b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetBucketBy")
    def reset_bucket_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketBy", []))

    @jsii.member(jsii_name="resetContextKind")
    def reset_context_kind(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContextKind", []))

    @jsii.member(jsii_name="resetRolloutWeights")
    def reset_rollout_weights(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutWeights", []))

    @jsii.member(jsii_name="resetVariation")
    def reset_variation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariation", []))

    @builtins.property
    @jsii.member(jsii_name="bucketByInput")
    def bucket_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketByInput"))

    @builtins.property
    @jsii.member(jsii_name="contextKindInput")
    def context_kind_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contextKindInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutWeightsInput")
    def rollout_weights_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "rolloutWeightsInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketBy")
    def bucket_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketBy"))

    @bucket_by.setter
    def bucket_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0c84aae2910d662b267c279eec56f987d25ed5bf19a603f923b50381859ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d81822e9bac77cbf857c26721d048ccd96a05617b33af176bfb17181c4917c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contextKind", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rolloutWeights")
    def rollout_weights(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "rolloutWeights"))

    @rollout_weights.setter
    def rollout_weights(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5c4dc85855993606bf18302d40c1f7448225cef5770d7b2c93bf207bf1c8b10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolloutWeights", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5b2866f97dd5f458e8a259c0cff4e40353a22306626016e9a9d817849c6ce3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FeatureFlagEnvironmentFallthrough]:
        return typing.cast(typing.Optional[FeatureFlagEnvironmentFallthrough], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FeatureFlagEnvironmentFallthrough],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__963fdb2ca3bb31323ec85c48c9051026515e8a22d33a8114fe18239574373a1e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentPrerequisites",
    jsii_struct_bases=[],
    name_mapping={"flag_key": "flagKey", "variation": "variation"},
)
class FeatureFlagEnvironmentPrerequisites:
    def __init__(self, *, flag_key: builtins.str, variation: jsii.Number) -> None:
        '''
        :param flag_key: The prerequisite feature flag's ``key``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#flag_key FeatureFlagEnvironment#flag_key}
        :param variation: The index of the prerequisite feature flag's variation to target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63941fb4c9cc7227c52d5626c12b2db316dd5ebb1ca55a101e171dbb2a76bc08)
            check_type(argname="argument flag_key", value=flag_key, expected_type=type_hints["flag_key"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "flag_key": flag_key,
            "variation": variation,
        }

    @builtins.property
    def flag_key(self) -> builtins.str:
        '''The prerequisite feature flag's ``key``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#flag_key FeatureFlagEnvironment#flag_key}
        '''
        result = self._values.get("flag_key")
        assert result is not None, "Required property 'flag_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def variation(self) -> jsii.Number:
        '''The index of the prerequisite feature flag's variation to target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        assert result is not None, "Required property 'variation' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FeatureFlagEnvironmentPrerequisites(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FeatureFlagEnvironmentPrerequisitesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentPrerequisitesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__30375f7061b216609ca2732ebe9d5bd4ddeee37eb36f38980dc2ec8e358b3af9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FeatureFlagEnvironmentPrerequisitesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4435321a12f437914e752e65b614725808776c1d388bc52e45cc2ba76b4ff132)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FeatureFlagEnvironmentPrerequisitesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50753c37be963b526771dfe9492cf263188cf89bb61249ed27a0b6b281d983f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5de134d924f342d454b00587d3b15b7574261dcfaca14a5b664bbab818d611bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e3a63f2828e48088322124b870b860c1323495495fb83a869bf1ecea36c6d29d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentPrerequisites]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentPrerequisites]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentPrerequisites]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aab2329799159ffd3c16685dc0922da0f790d1abda32dad4e358b70ec56ae68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FeatureFlagEnvironmentPrerequisitesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentPrerequisitesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e40b6ccf02ce4263d327010e196d0e4766caee9958670f1ad5d05a2a0f6255e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="flagKeyInput")
    def flag_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flagKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="flagKey")
    def flag_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "flagKey"))

    @flag_key.setter
    def flag_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0292bc2e7cc7e57395c889d124faeea230237cf4f9554bb00a34d39425031634)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flagKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3c40242ed7241fcfa06e015d410600ecbd2df96a5d5e3f7618226773118ac8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentPrerequisites]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentPrerequisites]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentPrerequisites]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f46daac74ab00832954eb19e3e6424ccab55f4bfb018695f9070eae21a844d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentRules",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_by": "bucketBy",
        "clauses": "clauses",
        "description": "description",
        "rollout_weights": "rolloutWeights",
        "variation": "variation",
    },
)
class FeatureFlagEnvironmentRules:
    def __init__(
        self,
        *,
        bucket_by: typing.Optional[builtins.str] = None,
        clauses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FeatureFlagEnvironmentRulesClauses", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
        variation: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param bucket_by: Group percentage rollout by a custom attribute. This argument is only valid if ``rollout_weights`` is also specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#bucket_by FeatureFlagEnvironment#bucket_by}
        :param clauses: clauses block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#clauses FeatureFlagEnvironment#clauses}
        :param description: A human-readable description of the targeting rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#description FeatureFlagEnvironment#description}
        :param rollout_weights: List of integer percentage rollout weights (in thousandths of a percent) to apply to each variation if the rule clauses evaluates to ``true``. The sum of the ``rollout_weights`` must equal 100000 and the number of rollout weights specified in the array must match the number of flag variations. You must specify either ``variation`` or ``rollout_weights``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#rollout_weights FeatureFlagEnvironment#rollout_weights}
        :param variation: The integer variation index to serve if the rule clauses evaluate to ``true``. You must specify either ``variation`` or ``rollout_weights`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79fd8592ed8cb3c1d7ae89faf7fa874caef359c1bef31b4e19682af92accaf76)
            check_type(argname="argument bucket_by", value=bucket_by, expected_type=type_hints["bucket_by"])
            check_type(argname="argument clauses", value=clauses, expected_type=type_hints["clauses"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rollout_weights", value=rollout_weights, expected_type=type_hints["rollout_weights"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bucket_by is not None:
            self._values["bucket_by"] = bucket_by
        if clauses is not None:
            self._values["clauses"] = clauses
        if description is not None:
            self._values["description"] = description
        if rollout_weights is not None:
            self._values["rollout_weights"] = rollout_weights
        if variation is not None:
            self._values["variation"] = variation

    @builtins.property
    def bucket_by(self) -> typing.Optional[builtins.str]:
        '''Group percentage rollout by a custom attribute. This argument is only valid if ``rollout_weights`` is also specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#bucket_by FeatureFlagEnvironment#bucket_by}
        '''
        result = self._values.get("bucket_by")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def clauses(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentRulesClauses"]]]:
        '''clauses block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#clauses FeatureFlagEnvironment#clauses}
        '''
        result = self._values.get("clauses")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FeatureFlagEnvironmentRulesClauses"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the targeting rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#description FeatureFlagEnvironment#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rollout_weights(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''List of integer percentage rollout weights (in thousandths of a percent) to apply to each variation if the rule clauses evaluates to ``true``.

        The sum of the ``rollout_weights`` must equal 100000 and the number of rollout weights specified in the array must match the number of flag variations. You must specify either ``variation`` or ``rollout_weights``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#rollout_weights FeatureFlagEnvironment#rollout_weights}
        '''
        result = self._values.get("rollout_weights")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def variation(self) -> typing.Optional[jsii.Number]:
        '''The integer variation index to serve if the rule clauses evaluate to ``true``.

        You must specify either ``variation`` or ``rollout_weights``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FeatureFlagEnvironmentRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentRulesClauses",
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
class FeatureFlagEnvironmentRulesClauses:
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
        :param attribute: The user attribute to operate on. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#attribute FeatureFlagEnvironment#attribute}
        :param op: The operator associated with the rule clause. Available options are ``in``, ``endsWith``, ``startsWith``, ``matches``, ``contains``, ``lessThan``, ``lessThanOrEqual``, ``greaterThanOrEqual``, ``before``, ``after``, ``segmentMatch``, ``semVerEqual``, ``semVerLessThan``, and ``semVerGreaterThan``. Read LaunchDarkly's `Operators <https://docs.launchdarkly.com/sdk/concepts/flag-evaluation-rules#operators>`_ documentation for more information. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#op FeatureFlagEnvironment#op}
        :param values: The list of values associated with the rule clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#values FeatureFlagEnvironment#values}
        :param context_kind: The context kind associated with this rule clause. If omitted, defaults to ``user``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_kind FeatureFlagEnvironment#context_kind}
        :param negate: Whether to negate the rule clause. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#negate FeatureFlagEnvironment#negate}
        :param value_type: The type for each of the clause's values. Available types are ``boolean``, ``string``, and ``number``. If omitted, ``value_type`` defaults to ``string``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#value_type FeatureFlagEnvironment#value_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3764dc1ebdf1737e8cb1806314d82ed5209be7d9cb0f28615542c981b19fcf3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#attribute FeatureFlagEnvironment#attribute}
        '''
        result = self._values.get("attribute")
        assert result is not None, "Required property 'attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def op(self) -> builtins.str:
        '''The operator associated with the rule clause.

        Available options are ``in``, ``endsWith``, ``startsWith``, ``matches``, ``contains``, ``lessThan``, ``lessThanOrEqual``, ``greaterThanOrEqual``, ``before``, ``after``, ``segmentMatch``, ``semVerEqual``, ``semVerLessThan``, and ``semVerGreaterThan``. Read LaunchDarkly's `Operators <https://docs.launchdarkly.com/sdk/concepts/flag-evaluation-rules#operators>`_ documentation for more information.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#op FeatureFlagEnvironment#op}
        '''
        result = self._values.get("op")
        assert result is not None, "Required property 'op' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The list of values associated with the rule clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#values FeatureFlagEnvironment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def context_kind(self) -> typing.Optional[builtins.str]:
        '''The context kind associated with this rule clause. If omitted, defaults to ``user``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#context_kind FeatureFlagEnvironment#context_kind}
        '''
        result = self._values.get("context_kind")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def negate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to negate the rule clause.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#negate FeatureFlagEnvironment#negate}
        '''
        result = self._values.get("negate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def value_type(self) -> typing.Optional[builtins.str]:
        '''The type for each of the clause's values.

        Available types are ``boolean``, ``string``, and ``number``. If omitted, ``value_type`` defaults to ``string``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#value_type FeatureFlagEnvironment#value_type}
        '''
        result = self._values.get("value_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FeatureFlagEnvironmentRulesClauses(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FeatureFlagEnvironmentRulesClausesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentRulesClausesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e3450f669601b723eca00ceb36533fe5d92bee6de15be503eaeae7d03fe914c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FeatureFlagEnvironmentRulesClausesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3285b62ca71df7149284420afcd322fdc8af0d74b9c6153e74092e9af5907c99)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FeatureFlagEnvironmentRulesClausesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1dce35e28afddb5dce83d19848916bc959d681a12756469881eda438bb2fd9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d30c29da895a1d0381a59469de5df0db61a730cb22661899e764fca34361a9b5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e5b3b9cc2ea3b3ef04e4d7fce0b813517b4baf2e4f31fdc55467870defed008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRulesClauses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRulesClauses]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRulesClauses]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611b78e5d27acd82a3748dd753fe74d838de0d0286415c83b0d505263e21f592)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FeatureFlagEnvironmentRulesClausesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentRulesClausesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba36a75b27c4b8deda8375c7af36732995637c635a80f19baee7c83144bd7b18)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b4e615e91c9a9350222371222f52a611537c06ec1146fa0f7de59a778eb3a59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contextKind")
    def context_kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "contextKind"))

    @context_kind.setter
    def context_kind(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd7053add15999c6c4913adeae458d1fdf4220a1686d11ec59d0fb5e41b72f8c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9118d74454005ce0b5df316f63efe1390eaa6b695f7250f8f2511e52883b7398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "negate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="op")
    def op(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "op"))

    @op.setter
    def op(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7854fab18c8717e6eabe913002144318a1bec5838281d6537b5c42d5dc9249)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "op", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36a8331221ee68a842150b20aefc48b8806bc655151e6a9ce74d05e65f98337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="valueType")
    def value_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "valueType"))

    @value_type.setter
    def value_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__375972d45b5a257aace211734a5609a015bec83137d772c45122294c8d371083)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "valueType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentRulesClauses]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentRulesClauses]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentRulesClauses]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2008e1d0fa0aace29a1064dd356a25fd61e1bd5d5bdae0c3068924d9c383eead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FeatureFlagEnvironmentRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f73381b52ec715836fd5a16c85eab389b4147cac4da9c29f27b9466f01a67e35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FeatureFlagEnvironmentRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2d5323204e49ecd9182ce2865a3d883a45a2b1f52fd6907d80d71ceadd4e06)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FeatureFlagEnvironmentRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47a3e2685c6ad1dd78a85cefdb7300762f6417fc1a1577d39f27c2323fc28a76)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6266723d111820bc1537e3ebd36b2e915e51e84e346bd9e26df006a5a0cd58cf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9ed3f92a55c46c98c1b5aad4195fc0e9c55e40f149d4bbc0cecdeaf7c627885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96c6f48dce1e0fa05e8a3dd2a811e77e48cce3ae29f90fc695a140254b2f7dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FeatureFlagEnvironmentRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e299a363d580b358909a9cfd2f1e08b92e5b400a392f52a851ba66f688914bb2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putClauses")
    def put_clauses(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__335e2b032fd0edaecfd18a46a4544194d7d1b1457e1e8211f651147de1e67e2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putClauses", [value]))

    @jsii.member(jsii_name="resetBucketBy")
    def reset_bucket_by(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBucketBy", []))

    @jsii.member(jsii_name="resetClauses")
    def reset_clauses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClauses", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetRolloutWeights")
    def reset_rollout_weights(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRolloutWeights", []))

    @jsii.member(jsii_name="resetVariation")
    def reset_variation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariation", []))

    @builtins.property
    @jsii.member(jsii_name="clauses")
    def clauses(self) -> FeatureFlagEnvironmentRulesClausesList:
        return typing.cast(FeatureFlagEnvironmentRulesClausesList, jsii.get(self, "clauses"))

    @builtins.property
    @jsii.member(jsii_name="bucketByInput")
    def bucket_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "bucketByInput"))

    @builtins.property
    @jsii.member(jsii_name="clausesInput")
    def clauses_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRulesClauses]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRulesClauses]]], jsii.get(self, "clausesInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="rolloutWeightsInput")
    def rollout_weights_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "rolloutWeightsInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="bucketBy")
    def bucket_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "bucketBy"))

    @bucket_by.setter
    def bucket_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4523663123c322f897f7c8dbbcbdee64774bab9c25818410a5d942c770c3aaf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bucketBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14de60bc4b435903702bb6c85bfb719344b54250e5b8b08c02909e122c14be5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="rolloutWeights")
    def rollout_weights(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "rolloutWeights"))

    @rollout_weights.setter
    def rollout_weights(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e7881e28c3119f4407e331eaf1d9224fa1255366078445aea50069665df56b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rolloutWeights", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c6c73af1fa23f35451761da7ff65d21eb6d4e1f8d2ca2cf0420458dd7d2b834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentRules]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentRules]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentRules]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40681cba59648b6f5a3f3d9e78f6cad0b862e576efd5cee6c598d70a2926f04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentTargets",
    jsii_struct_bases=[],
    name_mapping={"values": "values", "variation": "variation"},
)
class FeatureFlagEnvironmentTargets:
    def __init__(
        self,
        *,
        values: typing.Sequence[builtins.str],
        variation: jsii.Number,
    ) -> None:
        '''
        :param values: List of ``user`` strings to target. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#values FeatureFlagEnvironment#values}
        :param variation: The index of the variation to serve if a user target value is matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c72fbcaf4343839fe9804c08d329a29b09af1ba31b7c68d3c1dd452b24ef3b9e)
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            check_type(argname="argument variation", value=variation, expected_type=type_hints["variation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "values": values,
            "variation": variation,
        }

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''List of ``user`` strings to target.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#values FeatureFlagEnvironment#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def variation(self) -> jsii.Number:
        '''The index of the variation to serve if a user target value is matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/feature_flag_environment#variation FeatureFlagEnvironment#variation}
        '''
        result = self._values.get("variation")
        assert result is not None, "Required property 'variation' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FeatureFlagEnvironmentTargets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FeatureFlagEnvironmentTargetsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentTargetsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c33de2c5265ff1a8b55663daebf08380433ab1861e2f2147c4a55364f79d07d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "FeatureFlagEnvironmentTargetsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2e93f344266d7fea543aa3fcb0ab6968293e55d54c3a4428f3e0f4e6fbb3fb9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FeatureFlagEnvironmentTargetsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27025bd846d0dce80f31ffa3db3db613ea665c6c2fe6bc57a296514816687179)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56d3d5c29fc8236392eb4bb6bbf9e64b90b1a6e2d0963d6c7c81d6804349ae9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8040e05e049941a485d8ffce0c7377ab59b23464f7f97bbe57c517fe775598e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentTargets]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentTargets]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentTargets]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b844965251b1e61b6de737545259c7719754eaff1b5b815fb04d9288242e64e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FeatureFlagEnvironmentTargetsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.featureFlagEnvironment.FeatureFlagEnvironmentTargetsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73dc8ae6859ac296a2742d6e9e15ad08e884c270959fa76715cbe5683f150b99)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="variationInput")
    def variation_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "variationInput"))

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__677dd73f15707c759247e33bcde580ac1750d654093f5b04e1fc9c73ab7228fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="variation")
    def variation(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "variation"))

    @variation.setter
    def variation(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4121b94aec62952b919bb37f9cac12b1a4055d6fd709e5f96a673a67dca10ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "variation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentTargets]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentTargets]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentTargets]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba161be9c4d91436e6f6c60c38e1c85c494f8395bd7046fc16429c29712b167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FeatureFlagEnvironment",
    "FeatureFlagEnvironmentConfig",
    "FeatureFlagEnvironmentContextTargets",
    "FeatureFlagEnvironmentContextTargetsList",
    "FeatureFlagEnvironmentContextTargetsOutputReference",
    "FeatureFlagEnvironmentFallthrough",
    "FeatureFlagEnvironmentFallthroughOutputReference",
    "FeatureFlagEnvironmentPrerequisites",
    "FeatureFlagEnvironmentPrerequisitesList",
    "FeatureFlagEnvironmentPrerequisitesOutputReference",
    "FeatureFlagEnvironmentRules",
    "FeatureFlagEnvironmentRulesClauses",
    "FeatureFlagEnvironmentRulesClausesList",
    "FeatureFlagEnvironmentRulesClausesOutputReference",
    "FeatureFlagEnvironmentRulesList",
    "FeatureFlagEnvironmentRulesOutputReference",
    "FeatureFlagEnvironmentTargets",
    "FeatureFlagEnvironmentTargetsList",
    "FeatureFlagEnvironmentTargetsOutputReference",
]

publication.publish()

def _typecheckingstub__cd7acf209bd69aa69b558e650d96f2255ad49897f02e3ff67d3e391cefa26d15(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    env_key: builtins.str,
    fallthrough: typing.Union[FeatureFlagEnvironmentFallthrough, typing.Dict[builtins.str, typing.Any]],
    flag_id: builtins.str,
    off_variation: jsii.Number,
    context_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentContextTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prerequisites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentPrerequisites, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__f298d44f2c9d889c80ebdfd75b63176802aab1902827bcbd69fc9cc192e5c4fd(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8fa67162131bccf10ab78de185fdfc38e7299d843230aef6eaa279e05514298(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentContextTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcbadc95b49375ad001ed00bb2a1775ce4071bbd241dd04fa7054e79627abf6d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentPrerequisites, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77872a0530ffe9579697e63a7a198164725b0028c844a144e5642095cd2ecec2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6266f80c43d52f43d4222496da0a2ba72d9e9182f21d25750021a693de389bc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentTargets, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ecf7009104d88f74c3c8fe74599e52a39ba4bfe7bbb464b94d380d27e6a732e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecca6489e3220d4e374f8131b9089b3be6d2d537fe4ca535b9839c60e0e491a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e6039817c6551b855bf97b27d6475b3a97a01e8fe07ea43436f8591ebaee21(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0bee136dd1e83f251fadc79add8c554fb14b43f5294905bd51125266f73aceb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d1d62764ffafaef27890ee4fb19b32d2e6f655d2fb5120a4203c0752bc5db7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8344799f82ac2188814e25b380130110d81f479811df24bf4e7bfb7c46cd8b2f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7906af57752c788e0f057973f44c65cc16cb2d8bdf337d01f76caefb9503b806(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    env_key: builtins.str,
    fallthrough: typing.Union[FeatureFlagEnvironmentFallthrough, typing.Dict[builtins.str, typing.Any]],
    flag_id: builtins.str,
    off_variation: jsii.Number,
    context_targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentContextTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    prerequisites: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentPrerequisites, typing.Dict[builtins.str, typing.Any]]]]] = None,
    rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    targets: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentTargets, typing.Dict[builtins.str, typing.Any]]]]] = None,
    track_events: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b5642f26bcae6d4dc7221ef36abd376437c6e3e3763e1e7abb20f783bf5eba(
    *,
    context_kind: builtins.str,
    values: typing.Sequence[builtins.str],
    variation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__014195db03da4413c55abb6428f7cc4552305f02b1380565b531f38cb46e9904(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dceb5f83ff1a3c78dc20bac4b03d81787ee0246885f7e6eff6dfa33e7f8eb586(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2896c2bc48bdd8e6846d65975e617e76847c317ad3e97c56b77e195c9fa6f056(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab92986c0449eea4c9ced16a53a522c3bcfe52a166b098f15d8b7a788d626e95(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a5232063d3375bd7d0f2a32a775b47da2cef21e126af0b1bc44522b00c7ca5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf59c6d6d821a092c9517090f4ff4f0a02e8006b8c657db2c54c8b75b578cec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentContextTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196e0be39467781a01b354830174e9e5be6065c7ec1e7a436cbbb87906441848(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898404979c9cc8de60d9b43c8409473de6e2cb1e41ba840f409bd6f8168837da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c4c33d37cdbdff37615362df5de1d5de357535157a2317adfc799feb96ce30(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec35e998cb1e2178046f7db9d4146308e9bb63c74dc3a50e311b5ee767e6142d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9d3f5cfb43022bdef6576bb3e9003fe4c96408185e0eb733f290d1ac5cc583(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentContextTargets]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf881e63563456bfb70bbbeb289ea98f58d399b5ee497dbb67f9a344a45c1c2(
    *,
    bucket_by: typing.Optional[builtins.str] = None,
    context_kind: typing.Optional[builtins.str] = None,
    rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
    variation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cb20c5fef881c08623a269ea8889a326a44fab7e90780a9269e4b97686178b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0c84aae2910d662b267c279eec56f987d25ed5bf19a603f923b50381859ebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d81822e9bac77cbf857c26721d048ccd96a05617b33af176bfb17181c4917c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5c4dc85855993606bf18302d40c1f7448225cef5770d7b2c93bf207bf1c8b10(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5b2866f97dd5f458e8a259c0cff4e40353a22306626016e9a9d817849c6ce3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__963fdb2ca3bb31323ec85c48c9051026515e8a22d33a8114fe18239574373a1e(
    value: typing.Optional[FeatureFlagEnvironmentFallthrough],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63941fb4c9cc7227c52d5626c12b2db316dd5ebb1ca55a101e171dbb2a76bc08(
    *,
    flag_key: builtins.str,
    variation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30375f7061b216609ca2732ebe9d5bd4ddeee37eb36f38980dc2ec8e358b3af9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4435321a12f437914e752e65b614725808776c1d388bc52e45cc2ba76b4ff132(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50753c37be963b526771dfe9492cf263188cf89bb61249ed27a0b6b281d983f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de134d924f342d454b00587d3b15b7574261dcfaca14a5b664bbab818d611bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a63f2828e48088322124b870b860c1323495495fb83a869bf1ecea36c6d29d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aab2329799159ffd3c16685dc0922da0f790d1abda32dad4e358b70ec56ae68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentPrerequisites]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e40b6ccf02ce4263d327010e196d0e4766caee9958670f1ad5d05a2a0f6255e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0292bc2e7cc7e57395c889d124faeea230237cf4f9554bb00a34d39425031634(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3c40242ed7241fcfa06e015d410600ecbd2df96a5d5e3f7618226773118ac8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f46daac74ab00832954eb19e3e6424ccab55f4bfb018695f9070eae21a844d6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentPrerequisites]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79fd8592ed8cb3c1d7ae89faf7fa874caef359c1bef31b4e19682af92accaf76(
    *,
    bucket_by: typing.Optional[builtins.str] = None,
    clauses: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    rollout_weights: typing.Optional[typing.Sequence[jsii.Number]] = None,
    variation: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3764dc1ebdf1737e8cb1806314d82ed5209be7d9cb0f28615542c981b19fcf3(
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

def _typecheckingstub__2e3450f669601b723eca00ceb36533fe5d92bee6de15be503eaeae7d03fe914c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3285b62ca71df7149284420afcd322fdc8af0d74b9c6153e74092e9af5907c99(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1dce35e28afddb5dce83d19848916bc959d681a12756469881eda438bb2fd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30c29da895a1d0381a59469de5df0db61a730cb22661899e764fca34361a9b5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e5b3b9cc2ea3b3ef04e4d7fce0b813517b4baf2e4f31fdc55467870defed008(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611b78e5d27acd82a3748dd753fe74d838de0d0286415c83b0d505263e21f592(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRulesClauses]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba36a75b27c4b8deda8375c7af36732995637c635a80f19baee7c83144bd7b18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4e615e91c9a9350222371222f52a611537c06ec1146fa0f7de59a778eb3a59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd7053add15999c6c4913adeae458d1fdf4220a1686d11ec59d0fb5e41b72f8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9118d74454005ce0b5df316f63efe1390eaa6b695f7250f8f2511e52883b7398(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7854fab18c8717e6eabe913002144318a1bec5838281d6537b5c42d5dc9249(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36a8331221ee68a842150b20aefc48b8806bc655151e6a9ce74d05e65f98337(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375972d45b5a257aace211734a5609a015bec83137d772c45122294c8d371083(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2008e1d0fa0aace29a1064dd356a25fd61e1bd5d5bdae0c3068924d9c383eead(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentRulesClauses]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73381b52ec715836fd5a16c85eab389b4147cac4da9c29f27b9466f01a67e35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2d5323204e49ecd9182ce2865a3d883a45a2b1f52fd6907d80d71ceadd4e06(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47a3e2685c6ad1dd78a85cefdb7300762f6417fc1a1577d39f27c2323fc28a76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6266723d111820bc1537e3ebd36b2e915e51e84e346bd9e26df006a5a0cd58cf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ed3f92a55c46c98c1b5aad4195fc0e9c55e40f149d4bbc0cecdeaf7c627885(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96c6f48dce1e0fa05e8a3dd2a811e77e48cce3ae29f90fc695a140254b2f7dbb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e299a363d580b358909a9cfd2f1e08b92e5b400a392f52a851ba66f688914bb2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335e2b032fd0edaecfd18a46a4544194d7d1b1457e1e8211f651147de1e67e2d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FeatureFlagEnvironmentRulesClauses, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4523663123c322f897f7c8dbbcbdee64774bab9c25818410a5d942c770c3aaf2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14de60bc4b435903702bb6c85bfb719344b54250e5b8b08c02909e122c14be5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e7881e28c3119f4407e331eaf1d9224fa1255366078445aea50069665df56b(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c6c73af1fa23f35451761da7ff65d21eb6d4e1f8d2ca2cf0420458dd7d2b834(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40681cba59648b6f5a3f3d9e78f6cad0b862e576efd5cee6c598d70a2926f04(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentRules]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c72fbcaf4343839fe9804c08d329a29b09af1ba31b7c68d3c1dd452b24ef3b9e(
    *,
    values: typing.Sequence[builtins.str],
    variation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c33de2c5265ff1a8b55663daebf08380433ab1861e2f2147c4a55364f79d07d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e93f344266d7fea543aa3fcb0ab6968293e55d54c3a4428f3e0f4e6fbb3fb9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27025bd846d0dce80f31ffa3db3db613ea665c6c2fe6bc57a296514816687179(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56d3d5c29fc8236392eb4bb6bbf9e64b90b1a6e2d0963d6c7c81d6804349ae9a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8040e05e049941a485d8ffce0c7377ab59b23464f7f97bbe57c517fe775598e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b844965251b1e61b6de737545259c7719754eaff1b5b815fb04d9288242e64e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FeatureFlagEnvironmentTargets]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73dc8ae6859ac296a2742d6e9e15ad08e884c270959fa76715cbe5683f150b99(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__677dd73f15707c759247e33bcde580ac1750d654093f5b04e1fc9c73ab7228fc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4121b94aec62952b919bb37f9cac12b1a4055d6fd709e5f96a673a67dca10ef6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba161be9c4d91436e6f6c60c38e1c85c494f8395bd7046fc16429c29712b167(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FeatureFlagEnvironmentTargets]],
) -> None:
    """Type checking stubs"""
    pass
