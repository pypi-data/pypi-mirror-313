r'''
# `launchdarkly_access_token`

Refer to the Terraform Registry for docs: [`launchdarkly_access_token`](https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token).
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


class AccessToken(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.accessToken.AccessToken",
):
    '''Represents a {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token launchdarkly_access_token}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        custom_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_api_version: typing.Optional[jsii.Number] = None,
        expire: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        inline_roles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessTokenInlineRoles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        policy_statements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessTokenPolicyStatements", typing.Dict[builtins.str, typing.Any]]]]] = None,
        role: typing.Optional[builtins.str] = None,
        service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token launchdarkly_access_token} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param custom_roles: A list of custom role IDs to use as access limits for the access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#custom_roles AccessToken#custom_roles}
        :param default_api_version: The default API version for this token. Defaults to the latest API version. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#default_api_version AccessToken#default_api_version}
        :param expire: An expiration time for the current token secret, expressed as a Unix epoch time. Replace the computed token secret with a new value. The expired secret will no longer be able to authorize usage of the LaunchDarkly API. This field argument is **deprecated**. Please update your config to remove ``expire`` to maintain compatibility with future versions Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#expire AccessToken#expire}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#id AccessToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inline_roles: inline_roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#inline_roles AccessToken#inline_roles}
        :param name: A human-friendly name for the access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#name AccessToken#name}
        :param policy_statements: policy_statements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#policy_statements AccessToken#policy_statements}
        :param role: A built-in LaunchDarkly role. Can be ``reader``, ``writer``, or ``admin``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#role AccessToken#role}
        :param service_token: Whether the token will be a `service token <https://docs.launchdarkly.com/home/account-security/api-access-tokens#service-tokens>`_. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#service_token AccessToken#service_token}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22ba2bca456454a8f7efcb5c64fa8b3cf446b900f450707fcdb7fbdd0377da1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AccessTokenConfig(
            custom_roles=custom_roles,
            default_api_version=default_api_version,
            expire=expire,
            id=id,
            inline_roles=inline_roles,
            name=name,
            policy_statements=policy_statements,
            role=role,
            service_token=service_token,
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
        '''Generates CDKTF code for importing a AccessToken resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AccessToken to import.
        :param import_from_id: The id of the existing AccessToken that should be imported. Refer to the {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AccessToken to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff521033794a17762ec24876587ce0a56fb17a09b59cfe53ad9f3f40bbb6cb20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putInlineRoles")
    def put_inline_roles(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessTokenInlineRoles", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc77c3c95f29462b35a9fcd8154cffc8db2e49e34e8e7380302d4a4d3274ae73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putInlineRoles", [value]))

    @jsii.member(jsii_name="putPolicyStatements")
    def put_policy_statements(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessTokenPolicyStatements", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136e05f2666da5f05caade94cf64cb03a16e98571a1f52560f0adeea917c98ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPolicyStatements", [value]))

    @jsii.member(jsii_name="resetCustomRoles")
    def reset_custom_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomRoles", []))

    @jsii.member(jsii_name="resetDefaultApiVersion")
    def reset_default_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultApiVersion", []))

    @jsii.member(jsii_name="resetExpire")
    def reset_expire(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExpire", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInlineRoles")
    def reset_inline_roles(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInlineRoles", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPolicyStatements")
    def reset_policy_statements(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyStatements", []))

    @jsii.member(jsii_name="resetRole")
    def reset_role(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRole", []))

    @jsii.member(jsii_name="resetServiceToken")
    def reset_service_token(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceToken", []))

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
    @jsii.member(jsii_name="inlineRoles")
    def inline_roles(self) -> "AccessTokenInlineRolesList":
        return typing.cast("AccessTokenInlineRolesList", jsii.get(self, "inlineRoles"))

    @builtins.property
    @jsii.member(jsii_name="policyStatements")
    def policy_statements(self) -> "AccessTokenPolicyStatementsList":
        return typing.cast("AccessTokenPolicyStatementsList", jsii.get(self, "policyStatements"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "token"))

    @builtins.property
    @jsii.member(jsii_name="customRolesInput")
    def custom_roles_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "customRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultApiVersionInput")
    def default_api_version_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "defaultApiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="expireInput")
    def expire_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "expireInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inlineRolesInput")
    def inline_roles_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessTokenInlineRoles"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessTokenInlineRoles"]]], jsii.get(self, "inlineRolesInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyStatementsInput")
    def policy_statements_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessTokenPolicyStatements"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessTokenPolicyStatements"]]], jsii.get(self, "policyStatementsInput"))

    @builtins.property
    @jsii.member(jsii_name="roleInput")
    def role_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTokenInput")
    def service_token_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "serviceTokenInput"))

    @builtins.property
    @jsii.member(jsii_name="customRoles")
    def custom_roles(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "customRoles"))

    @custom_roles.setter
    def custom_roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c589deb7478139455ab3b8d1ce82009430e1434ae4c6e3518a8fe4ce728ddb58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRoles", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultApiVersion")
    def default_api_version(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "defaultApiVersion"))

    @default_api_version.setter
    def default_api_version(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__099a7066920520946a760725018bb2e90ea1a5f2e3f9e53f343410f15665776a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultApiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="expire")
    def expire(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "expire"))

    @expire.setter
    def expire(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebbfcbad0f61ad8a7b209406c815a6fa9df59789d933d22d84d59568c834693e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expire", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb4f6c6795dd7395e1cccf9dfded501f4f3825f46951cad73e625b74555fa5e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22fa7c034f722b5a8728191c59283119ad8c86c15a0b67d48f42579f53c8a57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @role.setter
    def role(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e102a386ef1a64f3f1ac7e67162db120741fcffc1a26f66d262ef60bf9a2dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "role", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceToken")
    def service_token(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "serviceToken"))

    @service_token.setter
    def service_token(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af8010be7f0fe005056e1b5fc44172654df928a84e242fdc7fbad4322ca927b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceToken", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.accessToken.AccessTokenConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "custom_roles": "customRoles",
        "default_api_version": "defaultApiVersion",
        "expire": "expire",
        "id": "id",
        "inline_roles": "inlineRoles",
        "name": "name",
        "policy_statements": "policyStatements",
        "role": "role",
        "service_token": "serviceToken",
    },
)
class AccessTokenConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        custom_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_api_version: typing.Optional[jsii.Number] = None,
        expire: typing.Optional[jsii.Number] = None,
        id: typing.Optional[builtins.str] = None,
        inline_roles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessTokenInlineRoles", typing.Dict[builtins.str, typing.Any]]]]] = None,
        name: typing.Optional[builtins.str] = None,
        policy_statements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AccessTokenPolicyStatements", typing.Dict[builtins.str, typing.Any]]]]] = None,
        role: typing.Optional[builtins.str] = None,
        service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param custom_roles: A list of custom role IDs to use as access limits for the access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#custom_roles AccessToken#custom_roles}
        :param default_api_version: The default API version for this token. Defaults to the latest API version. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#default_api_version AccessToken#default_api_version}
        :param expire: An expiration time for the current token secret, expressed as a Unix epoch time. Replace the computed token secret with a new value. The expired secret will no longer be able to authorize usage of the LaunchDarkly API. This field argument is **deprecated**. Please update your config to remove ``expire`` to maintain compatibility with future versions Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#expire AccessToken#expire}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#id AccessToken#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param inline_roles: inline_roles block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#inline_roles AccessToken#inline_roles}
        :param name: A human-friendly name for the access token. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#name AccessToken#name}
        :param policy_statements: policy_statements block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#policy_statements AccessToken#policy_statements}
        :param role: A built-in LaunchDarkly role. Can be ``reader``, ``writer``, or ``admin``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#role AccessToken#role}
        :param service_token: Whether the token will be a `service token <https://docs.launchdarkly.com/home/account-security/api-access-tokens#service-tokens>`_. A change in this field will force the destruction of the existing resource and the creation of a new one. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#service_token AccessToken#service_token}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2057e14f74a5d72eae1bfd306b184f12411fbbd7712def89d264547c92f1ea09)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument custom_roles", value=custom_roles, expected_type=type_hints["custom_roles"])
            check_type(argname="argument default_api_version", value=default_api_version, expected_type=type_hints["default_api_version"])
            check_type(argname="argument expire", value=expire, expected_type=type_hints["expire"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument inline_roles", value=inline_roles, expected_type=type_hints["inline_roles"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_statements", value=policy_statements, expected_type=type_hints["policy_statements"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument service_token", value=service_token, expected_type=type_hints["service_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if custom_roles is not None:
            self._values["custom_roles"] = custom_roles
        if default_api_version is not None:
            self._values["default_api_version"] = default_api_version
        if expire is not None:
            self._values["expire"] = expire
        if id is not None:
            self._values["id"] = id
        if inline_roles is not None:
            self._values["inline_roles"] = inline_roles
        if name is not None:
            self._values["name"] = name
        if policy_statements is not None:
            self._values["policy_statements"] = policy_statements
        if role is not None:
            self._values["role"] = role
        if service_token is not None:
            self._values["service_token"] = service_token

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
    def custom_roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of custom role IDs to use as access limits for the access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#custom_roles AccessToken#custom_roles}
        '''
        result = self._values.get("custom_roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_api_version(self) -> typing.Optional[jsii.Number]:
        '''The default API version for this token.

        Defaults to the latest API version. A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#default_api_version AccessToken#default_api_version}
        '''
        result = self._values.get("default_api_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def expire(self) -> typing.Optional[jsii.Number]:
        '''An expiration time for the current token secret, expressed as a Unix epoch time.

        Replace the computed token secret with a new value. The expired secret will no longer be able to authorize usage of the LaunchDarkly API. This field argument is **deprecated**. Please update your config to remove ``expire`` to maintain compatibility with future versions

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#expire AccessToken#expire}
        '''
        result = self._values.get("expire")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#id AccessToken#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def inline_roles(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessTokenInlineRoles"]]]:
        '''inline_roles block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#inline_roles AccessToken#inline_roles}
        '''
        result = self._values.get("inline_roles")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessTokenInlineRoles"]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A human-friendly name for the access token.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#name AccessToken#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_statements(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessTokenPolicyStatements"]]]:
        '''policy_statements block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#policy_statements AccessToken#policy_statements}
        '''
        result = self._values.get("policy_statements")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AccessTokenPolicyStatements"]]], result)

    @builtins.property
    def role(self) -> typing.Optional[builtins.str]:
        '''A built-in LaunchDarkly role. Can be ``reader``, ``writer``, or ``admin``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#role AccessToken#role}
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_token(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the token will be a `service token <https://docs.launchdarkly.com/home/account-security/api-access-tokens#service-tokens>`_. A change in this field will force the destruction of the existing resource and the creation of a new one.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#service_token AccessToken#service_token}
        '''
        result = self._values.get("service_token")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessTokenConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.accessToken.AccessTokenInlineRoles",
    jsii_struct_bases=[],
    name_mapping={
        "effect": "effect",
        "actions": "actions",
        "not_actions": "notActions",
        "not_resources": "notResources",
        "resources": "resources",
    },
)
class AccessTokenInlineRoles:
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
        :param effect: Either ``allow`` or ``deny``. This argument defines whether the statement allows or denies access to the named resources and actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#effect AccessToken#effect}
        :param actions: The list of action specifiers defining the actions to which the statement applies. Either ``actions`` or ``not_actions`` must be specified. For a list of available actions read `Actions reference <https://docs.launchdarkly.com/home/account-security/custom-roles/actions#actions-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#actions AccessToken#actions}
        :param not_actions: The list of action specifiers defining the actions to which the statement does not apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#not_actions AccessToken#not_actions}
        :param not_resources: The list of resource specifiers defining the resources to which the statement does not apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#not_resources AccessToken#not_resources}
        :param resources: The list of resource specifiers defining the resources to which the statement applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#resources AccessToken#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf777dc854b3453cf4763366a000825853d9755645cbb159247ac5859373423)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#effect AccessToken#effect}
        '''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of action specifiers defining the actions to which the statement applies.

        Either ``actions`` or ``not_actions`` must be specified. For a list of available actions read `Actions reference <https://docs.launchdarkly.com/home/account-security/custom-roles/actions#actions-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#actions AccessToken#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of action specifiers defining the actions to which the statement does not apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#not_actions AccessToken#not_actions}
        '''
        result = self._values.get("not_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of resource specifiers defining the resources to which the statement does not apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#not_resources AccessToken#not_resources}
        '''
        result = self._values.get("not_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of resource specifiers defining the resources to which the statement applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#resources AccessToken#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessTokenInlineRoles(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessTokenInlineRolesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.accessToken.AccessTokenInlineRolesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b2be51178631640077d8cdfc95399ad65323e56e51ce8b4715f9516831b1d8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessTokenInlineRolesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e463c5bd285d35dde3c91cfdc8efa49529bd77eec51e6e7eeabab5064c864d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessTokenInlineRolesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2440ab51225b438f715c70d98459d8bffaaf94cec1d049ed8f022a2ff4ca468b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5813aa8cc7e0adc64bdf7791cf75545736ff7dc4a1a38bdcdd48ad8fb62c7a33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8e73ed4b9a200ee953287d0b4f4423480550ceb5348ab1b670545db5e69c337)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessTokenInlineRoles]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessTokenInlineRoles]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessTokenInlineRoles]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef68ccd105929840008ada0ed8daee5b2c8762865abb07160f1e77a47b4bd823)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessTokenInlineRolesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.accessToken.AccessTokenInlineRolesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0937984cf9d108d06f0a7547f4758c2db15bf44fc54aeac4a941b46c3b9f7a7d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2bfbf3d2c43bc92fa3e6635b698719954229ca43727364304f05b3808e9cad4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f863da7bb705f5fbccb338293a5ccfc443826ace429dc20e63a4db234076c567)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notActions")
    def not_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notActions"))

    @not_actions.setter
    def not_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e3c6274a0ff08e0e41f0144755537fe12209155ecccc7db541afaacf4d5d19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notActions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notResources")
    def not_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notResources"))

    @not_resources.setter
    def not_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddff622db6047379c3bf5cf7a6ff476a90676ea43e4b92933d7d574a9559b9f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5238f1a86a868cfbffb858a6397e2679a05f52d0118e6b4085bf7391a2acb2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessTokenInlineRoles]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessTokenInlineRoles]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessTokenInlineRoles]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9e4ec76014ec2246e0b8963cde02ef37a94b70bcc09bb2b1f26f240c9dcd9f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-launchdarkly.accessToken.AccessTokenPolicyStatements",
    jsii_struct_bases=[],
    name_mapping={
        "effect": "effect",
        "actions": "actions",
        "not_actions": "notActions",
        "not_resources": "notResources",
        "resources": "resources",
    },
)
class AccessTokenPolicyStatements:
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
        :param effect: Either ``allow`` or ``deny``. This argument defines whether the statement allows or denies access to the named resources and actions. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#effect AccessToken#effect}
        :param actions: The list of action specifiers defining the actions to which the statement applies. Either ``actions`` or ``not_actions`` must be specified. For a list of available actions read `Actions reference <https://docs.launchdarkly.com/home/account-security/custom-roles/actions#actions-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#actions AccessToken#actions}
        :param not_actions: The list of action specifiers defining the actions to which the statement does not apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#not_actions AccessToken#not_actions}
        :param not_resources: The list of resource specifiers defining the resources to which the statement does not apply. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#not_resources AccessToken#not_resources}
        :param resources: The list of resource specifiers defining the resources to which the statement applies. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#resources AccessToken#resources}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69536178ec1dc81c007afab784c9a2f1c87f74bac4ab24e4995657c04b64bc4a)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#effect AccessToken#effect}
        '''
        result = self._values.get("effect")
        assert result is not None, "Required property 'effect' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of action specifiers defining the actions to which the statement applies.

        Either ``actions`` or ``not_actions`` must be specified. For a list of available actions read `Actions reference <https://docs.launchdarkly.com/home/account-security/custom-roles/actions#actions-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#actions AccessToken#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of action specifiers defining the actions to which the statement does not apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#not_actions AccessToken#not_actions}
        '''
        result = self._values.get("not_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of resource specifiers defining the resources to which the statement does not apply.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#not_resources AccessToken#not_resources}
        '''
        result = self._values.get("not_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of resource specifiers defining the resources to which the statement applies.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/launchdarkly/launchdarkly/2.21.2/docs/resources/access_token#resources AccessToken#resources}
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessTokenPolicyStatements(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AccessTokenPolicyStatementsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.accessToken.AccessTokenPolicyStatementsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__486bf104c9f6880ff2162f66bf60dd8f772ab302c68582162ad0608468794a17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "AccessTokenPolicyStatementsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d595c7e0c1ed05657efb0b52fc0bf7386e28307beb2a7fb16277a6d9b95626)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AccessTokenPolicyStatementsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9398c955d3af1556202e957591a598faa8cbc01ee64fe6c201bc7d05cf0a76a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a4c3b3ec2ce7ec7aa0e525ad4cc916d65e5a84ecbbe3b8ea0aa328cb7b4f8fa9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d72d8e6c874add96ffa40e874028e390101f6e3fdf12f24a596dc19fc665a6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessTokenPolicyStatements]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessTokenPolicyStatements]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessTokenPolicyStatements]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__050bcc1167bef4614a4bd61614d201d0a0e7151d489bb45e4d5c2c796a3525a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AccessTokenPolicyStatementsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-launchdarkly.accessToken.AccessTokenPolicyStatementsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a880a6db06bb85415e7ed9449a759975e4afe9550a590982807de5404ae8b5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0d3be2f9fd13be57e5ee674fa61c7a624d014cc4dfb2688386a2cbaf064b575)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12f946b4dcdf0f540d2f167d7cedaf10a951b23ef8cfe4487b3d65a73335df9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notActions")
    def not_actions(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notActions"))

    @not_actions.setter
    def not_actions(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3286da058cc98e30f5fd601582fd0dad46eb7649b84a916480279dc975fa2541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notActions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notResources")
    def not_resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notResources"))

    @not_resources.setter
    def not_resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3990e15ae10a61c2793eb34b617efc625d1b1fe64699f1b92501f8f5a90d1a8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05081338609a94ac00251ae24f44547db17eb77e21f536522afec6cc22e8947)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessTokenPolicyStatements]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessTokenPolicyStatements]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessTokenPolicyStatements]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71acc12224ea493091e5f6b1895a158de3149678adf77dddf2bb7592cf117f0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AccessToken",
    "AccessTokenConfig",
    "AccessTokenInlineRoles",
    "AccessTokenInlineRolesList",
    "AccessTokenInlineRolesOutputReference",
    "AccessTokenPolicyStatements",
    "AccessTokenPolicyStatementsList",
    "AccessTokenPolicyStatementsOutputReference",
]

publication.publish()

def _typecheckingstub__22ba2bca456454a8f7efcb5c64fa8b3cf446b900f450707fcdb7fbdd0377da1e(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    custom_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_api_version: typing.Optional[jsii.Number] = None,
    expire: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    inline_roles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessTokenInlineRoles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    policy_statements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessTokenPolicyStatements, typing.Dict[builtins.str, typing.Any]]]]] = None,
    role: typing.Optional[builtins.str] = None,
    service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__ff521033794a17762ec24876587ce0a56fb17a09b59cfe53ad9f3f40bbb6cb20(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc77c3c95f29462b35a9fcd8154cffc8db2e49e34e8e7380302d4a4d3274ae73(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessTokenInlineRoles, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136e05f2666da5f05caade94cf64cb03a16e98571a1f52560f0adeea917c98ce(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessTokenPolicyStatements, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c589deb7478139455ab3b8d1ce82009430e1434ae4c6e3518a8fe4ce728ddb58(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099a7066920520946a760725018bb2e90ea1a5f2e3f9e53f343410f15665776a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebbfcbad0f61ad8a7b209406c815a6fa9df59789d933d22d84d59568c834693e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb4f6c6795dd7395e1cccf9dfded501f4f3825f46951cad73e625b74555fa5e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22fa7c034f722b5a8728191c59283119ad8c86c15a0b67d48f42579f53c8a57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e102a386ef1a64f3f1ac7e67162db120741fcffc1a26f66d262ef60bf9a2dc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af8010be7f0fe005056e1b5fc44172654df928a84e242fdc7fbad4322ca927b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2057e14f74a5d72eae1bfd306b184f12411fbbd7712def89d264547c92f1ea09(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    custom_roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_api_version: typing.Optional[jsii.Number] = None,
    expire: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    inline_roles: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessTokenInlineRoles, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: typing.Optional[builtins.str] = None,
    policy_statements: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AccessTokenPolicyStatements, typing.Dict[builtins.str, typing.Any]]]]] = None,
    role: typing.Optional[builtins.str] = None,
    service_token: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf777dc854b3453cf4763366a000825853d9755645cbb159247ac5859373423(
    *,
    effect: builtins.str,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2be51178631640077d8cdfc95399ad65323e56e51ce8b4715f9516831b1d8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e463c5bd285d35dde3c91cfdc8efa49529bd77eec51e6e7eeabab5064c864d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2440ab51225b438f715c70d98459d8bffaaf94cec1d049ed8f022a2ff4ca468b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5813aa8cc7e0adc64bdf7791cf75545736ff7dc4a1a38bdcdd48ad8fb62c7a33(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8e73ed4b9a200ee953287d0b4f4423480550ceb5348ab1b670545db5e69c337(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef68ccd105929840008ada0ed8daee5b2c8762865abb07160f1e77a47b4bd823(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessTokenInlineRoles]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0937984cf9d108d06f0a7547f4758c2db15bf44fc54aeac4a941b46c3b9f7a7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2bfbf3d2c43bc92fa3e6635b698719954229ca43727364304f05b3808e9cad4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f863da7bb705f5fbccb338293a5ccfc443826ace429dc20e63a4db234076c567(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e3c6274a0ff08e0e41f0144755537fe12209155ecccc7db541afaacf4d5d19(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddff622db6047379c3bf5cf7a6ff476a90676ea43e4b92933d7d574a9559b9f8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5238f1a86a868cfbffb858a6397e2679a05f52d0118e6b4085bf7391a2acb2e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9e4ec76014ec2246e0b8963cde02ef37a94b70bcc09bb2b1f26f240c9dcd9f7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessTokenInlineRoles]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69536178ec1dc81c007afab784c9a2f1c87f74bac4ab24e4995657c04b64bc4a(
    *,
    effect: builtins.str,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__486bf104c9f6880ff2162f66bf60dd8f772ab302c68582162ad0608468794a17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d595c7e0c1ed05657efb0b52fc0bf7386e28307beb2a7fb16277a6d9b95626(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9398c955d3af1556202e957591a598faa8cbc01ee64fe6c201bc7d05cf0a76a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c3b3ec2ce7ec7aa0e525ad4cc916d65e5a84ecbbe3b8ea0aa328cb7b4f8fa9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d72d8e6c874add96ffa40e874028e390101f6e3fdf12f24a596dc19fc665a6c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__050bcc1167bef4614a4bd61614d201d0a0e7151d489bb45e4d5c2c796a3525a5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AccessTokenPolicyStatements]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a880a6db06bb85415e7ed9449a759975e4afe9550a590982807de5404ae8b5f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0d3be2f9fd13be57e5ee674fa61c7a624d014cc4dfb2688386a2cbaf064b575(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12f946b4dcdf0f540d2f167d7cedaf10a951b23ef8cfe4487b3d65a73335df9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3286da058cc98e30f5fd601582fd0dad46eb7649b84a916480279dc975fa2541(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3990e15ae10a61c2793eb34b617efc625d1b1fe64699f1b92501f8f5a90d1a8d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05081338609a94ac00251ae24f44547db17eb77e21f536522afec6cc22e8947(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71acc12224ea493091e5f6b1895a158de3149678adf77dddf2bb7592cf117f0a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AccessTokenPolicyStatements]],
) -> None:
    """Type checking stubs"""
    pass
