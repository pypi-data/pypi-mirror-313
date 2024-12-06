r'''
# `aws_codepipeline`

Refer to the Terraform Registry for docs: [`aws_codepipeline`](https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline).
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


class Codepipeline(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.Codepipeline",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline aws_codepipeline}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        artifact_store: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineArtifactStore", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        role_arn: builtins.str,
        stage: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineStage", typing.Dict[builtins.str, typing.Any]]]],
        execution_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pipeline_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineTrigger", typing.Dict[builtins.str, typing.Any]]]]] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline aws_codepipeline} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param artifact_store: artifact_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#artifact_store Codepipeline#artifact_store}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#name Codepipeline#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#role_arn Codepipeline#role_arn}.
        :param stage: stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#stage Codepipeline#stage}
        :param execution_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#execution_mode Codepipeline#execution_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#id Codepipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pipeline_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#pipeline_type Codepipeline#pipeline_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#tags Codepipeline#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#tags_all Codepipeline#tags_all}.
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#trigger Codepipeline#trigger}
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#variable Codepipeline#variable}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b05bf9d470a6d541c6793d8c11b37ee4652aafe5fdf5945767bdae8987af99b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = CodepipelineConfig(
            artifact_store=artifact_store,
            name=name,
            role_arn=role_arn,
            stage=stage,
            execution_mode=execution_mode,
            id=id,
            pipeline_type=pipeline_type,
            tags=tags,
            tags_all=tags_all,
            trigger=trigger,
            variable=variable,
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
        '''Generates CDKTF code for importing a Codepipeline resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the Codepipeline to import.
        :param import_from_id: The id of the existing Codepipeline that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the Codepipeline to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ded069c6455f301d07a57e4ce2aab355427daa2c00f59657bbbc6af533bf0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putArtifactStore")
    def put_artifact_store(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineArtifactStore", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f10383963c155174b899e60ffc8f2f98399552b79c35a4de6c1594d741e354f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putArtifactStore", [value]))

    @jsii.member(jsii_name="putStage")
    def put_stage(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineStage", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df349ff7dee10b41aa6aba23f53a3bbf1505b0a1e6327689dc5c6b4f314ad09f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStage", [value]))

    @jsii.member(jsii_name="putTrigger")
    def put_trigger(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineTrigger", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20fed748b626d96524e76b790203bba5a85d495bd2bd16a24fc9a4daac4eaf2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTrigger", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea92293a59909fbde979e65918ccf343a98a17be2322d9716fdaf87810f5857e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetExecutionMode")
    def reset_execution_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExecutionMode", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPipelineType")
    def reset_pipeline_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPipelineType", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="resetTrigger")
    def reset_trigger(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrigger", []))

    @jsii.member(jsii_name="resetVariable")
    def reset_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariable", []))

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
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="artifactStore")
    def artifact_store(self) -> "CodepipelineArtifactStoreList":
        return typing.cast("CodepipelineArtifactStoreList", jsii.get(self, "artifactStore"))

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> "CodepipelineStageList":
        return typing.cast("CodepipelineStageList", jsii.get(self, "stage"))

    @builtins.property
    @jsii.member(jsii_name="trigger")
    def trigger(self) -> "CodepipelineTriggerList":
        return typing.cast("CodepipelineTriggerList", jsii.get(self, "trigger"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "CodepipelineVariableList":
        return typing.cast("CodepipelineVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="artifactStoreInput")
    def artifact_store_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineArtifactStore"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineArtifactStore"]]], jsii.get(self, "artifactStoreInput"))

    @builtins.property
    @jsii.member(jsii_name="executionModeInput")
    def execution_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pipelineTypeInput")
    def pipeline_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pipelineTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="stageInput")
    def stage_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStage"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStage"]]], jsii.get(self, "stageInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerInput")
    def trigger_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTrigger"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTrigger"]]], jsii.get(self, "triggerInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineVariable"]]], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="executionMode")
    def execution_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "executionMode"))

    @execution_mode.setter
    def execution_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d37a3ba48aa73ff30a54fd7550b8a970ef72607f4a9bceb975692b4d7acf147)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "executionMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93f2b93040cead7a9937f01217f6352ea2233d2f400256af3f7e4a7b14cdb3bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad2c1e89e83d86c1039aaf9c1d57abcc0a27d9005cac5eb9a3baf63292f59bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pipelineType")
    def pipeline_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pipelineType"))

    @pipeline_type.setter
    def pipeline_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfcb0d67474d8ca9a6da721f60a72a90512d1eea234aee394b190a8c9e4a6160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pipelineType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d5a262fb418a52d9c077ee2a5b67d24123f15ddcf4a7cb9682b8266004f6d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6ed8943de3fd52a65f1a6203dee739473e5c0cc0256f454d374149682de34b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e16b43e185b495bb94719ac17a947d8bc348193f0e70826ee610bdcd94037d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStore",
    jsii_struct_bases=[],
    name_mapping={
        "location": "location",
        "type": "type",
        "encryption_key": "encryptionKey",
        "region": "region",
    },
)
class CodepipelineArtifactStore:
    def __init__(
        self,
        *,
        location: builtins.str,
        type: builtins.str,
        encryption_key: typing.Optional[typing.Union["CodepipelineArtifactStoreEncryptionKey", typing.Dict[builtins.str, typing.Any]]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#location Codepipeline#location}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#type Codepipeline#type}.
        :param encryption_key: encryption_key block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#encryption_key Codepipeline#encryption_key}
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#region Codepipeline#region}.
        '''
        if isinstance(encryption_key, dict):
            encryption_key = CodepipelineArtifactStoreEncryptionKey(**encryption_key)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__922068355d678dd6effd40fe938c7b4bef095e80aafdc157f6347e9a154a7455)
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "type": type,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#location Codepipeline#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#type Codepipeline#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(
        self,
    ) -> typing.Optional["CodepipelineArtifactStoreEncryptionKey"]:
        '''encryption_key block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#encryption_key Codepipeline#encryption_key}
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional["CodepipelineArtifactStoreEncryptionKey"], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#region Codepipeline#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineArtifactStore(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStoreEncryptionKey",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "type": "type"},
)
class CodepipelineArtifactStoreEncryptionKey:
    def __init__(self, *, id: builtins.str, type: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#id Codepipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#type Codepipeline#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d46126b88ec0637b8870b9918772f62c576de320afd50301c51ff6f2cb4a730)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "type": type,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#id Codepipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#type Codepipeline#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineArtifactStoreEncryptionKey(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineArtifactStoreEncryptionKeyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStoreEncryptionKeyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46c941e35195f370c8e8fed484db32b46c4930061ab32816151a6c9a77ed98a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4af46ebfe947a3e6650b847155aeebc7fd20abb38822fc8a7fa9b66abe127f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6397c6cc84d9b854c5d220f016d81c03041b1cc9f7a19e2737721e673175d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodepipelineArtifactStoreEncryptionKey]:
        return typing.cast(typing.Optional[CodepipelineArtifactStoreEncryptionKey], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodepipelineArtifactStoreEncryptionKey],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f5a35c64dd518ba782d6fe1f72bc901c94647985fcb0f0410d8a36f9758c73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineArtifactStoreList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStoreList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__98845279dd07aa22f658694ce2d785b2f63880044cbc224cd270f73c530ed666)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CodepipelineArtifactStoreOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__110e0ac1b03bc412da726cf99c749a3213d21c96fa6fd765c2801666adaf8ad2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineArtifactStoreOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbd95915f530001cb29302739bba967dc100350855e39797e71f05c760586e1a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__388da3f1639c681b74313cc4f5d5034f54a9d30b265701a8ab65b3bf5fdf4b41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1d3d3d63a3a0886461f20af849e3daeac985588a43d5adb1259efd4988d0a3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6b396dc65bdc3cb55da1e64f1ae1eccffb88c9a19379fe9adc874336629afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineArtifactStoreOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineArtifactStoreOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32a9282c02570c1515b4ff146f29d98b0405b3f91c8562927c494269fbdf24ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putEncryptionKey")
    def put_encryption_key(self, *, id: builtins.str, type: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#id Codepipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#type Codepipeline#type}.
        '''
        value = CodepipelineArtifactStoreEncryptionKey(id=id, type=type)

        return typing.cast(None, jsii.invoke(self, "putEncryptionKey", [value]))

    @jsii.member(jsii_name="resetEncryptionKey")
    def reset_encryption_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionKey", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> CodepipelineArtifactStoreEncryptionKeyOutputReference:
        return typing.cast(CodepipelineArtifactStoreEncryptionKeyOutputReference, jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKeyInput")
    def encryption_key_input(
        self,
    ) -> typing.Optional[CodepipelineArtifactStoreEncryptionKey]:
        return typing.cast(typing.Optional[CodepipelineArtifactStoreEncryptionKey], jsii.get(self, "encryptionKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7073ace0c2ac96908ecd48678800c927f8ee9ea800a55ea3dff5d90d9bd7491)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644a35e7f02a989e4b3fdc9403a5a8d0921a77fdd69b886960fd8556e66a71f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3433081d5bd0381c76a04f4ce558aaf0808eac349c000c7a1f846a58c357cbbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineArtifactStore]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineArtifactStore]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineArtifactStore]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a1b57429ee5766a4a1051555294a5e0a3065da41c51ae3aa106edc5bdc97d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "artifact_store": "artifactStore",
        "name": "name",
        "role_arn": "roleArn",
        "stage": "stage",
        "execution_mode": "executionMode",
        "id": "id",
        "pipeline_type": "pipelineType",
        "tags": "tags",
        "tags_all": "tagsAll",
        "trigger": "trigger",
        "variable": "variable",
    },
)
class CodepipelineConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        artifact_store: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineArtifactStore, typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        role_arn: builtins.str,
        stage: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineStage", typing.Dict[builtins.str, typing.Any]]]],
        execution_mode: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        pipeline_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineTrigger", typing.Dict[builtins.str, typing.Any]]]]] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param artifact_store: artifact_store block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#artifact_store Codepipeline#artifact_store}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#name Codepipeline#name}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#role_arn Codepipeline#role_arn}.
        :param stage: stage block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#stage Codepipeline#stage}
        :param execution_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#execution_mode Codepipeline#execution_mode}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#id Codepipeline#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param pipeline_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#pipeline_type Codepipeline#pipeline_type}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#tags Codepipeline#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#tags_all Codepipeline#tags_all}.
        :param trigger: trigger block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#trigger Codepipeline#trigger}
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#variable Codepipeline#variable}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__009e693604d53e9e0598d73e0bbcfe99d252352f522377b683d9881d7516179f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument artifact_store", value=artifact_store, expected_type=type_hints["artifact_store"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument execution_mode", value=execution_mode, expected_type=type_hints["execution_mode"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument pipeline_type", value=pipeline_type, expected_type=type_hints["pipeline_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_store": artifact_store,
            "name": name,
            "role_arn": role_arn,
            "stage": stage,
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
        if execution_mode is not None:
            self._values["execution_mode"] = execution_mode
        if id is not None:
            self._values["id"] = id
        if pipeline_type is not None:
            self._values["pipeline_type"] = pipeline_type
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all
        if trigger is not None:
            self._values["trigger"] = trigger
        if variable is not None:
            self._values["variable"] = variable

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
    def artifact_store(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]:
        '''artifact_store block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#artifact_store Codepipeline#artifact_store}
        '''
        result = self._values.get("artifact_store")
        assert result is not None, "Required property 'artifact_store' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#name Codepipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#role_arn Codepipeline#role_arn}.'''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStage"]]:
        '''stage block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#stage Codepipeline#stage}
        '''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStage"]], result)

    @builtins.property
    def execution_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#execution_mode Codepipeline#execution_mode}.'''
        result = self._values.get("execution_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#id Codepipeline#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#pipeline_type Codepipeline#pipeline_type}.'''
        result = self._values.get("pipeline_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#tags Codepipeline#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#tags_all Codepipeline#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def trigger(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTrigger"]]]:
        '''trigger block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#trigger Codepipeline#trigger}
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTrigger"]]], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#variable Codepipeline#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStage",
    jsii_struct_bases=[],
    name_mapping={"action": "action", "name": "name"},
)
class CodepipelineStage:
    def __init__(
        self,
        *,
        action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineStageAction", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
    ) -> None:
        '''
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#action Codepipeline#action}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#name Codepipeline#name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f317cae47d1d43bfefb03a17abc49f8c36567a6558090d426f042e0b34d27a61)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "name": name,
        }

    @builtins.property
    def action(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStageAction"]]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#action Codepipeline#action}
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineStageAction"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#name Codepipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineStage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageAction",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "name": "name",
        "owner": "owner",
        "provider": "provider",
        "version": "version",
        "configuration": "configuration",
        "input_artifacts": "inputArtifacts",
        "namespace": "namespace",
        "output_artifacts": "outputArtifacts",
        "region": "region",
        "role_arn": "roleArn",
        "run_order": "runOrder",
        "timeout_in_minutes": "timeoutInMinutes",
    },
)
class CodepipelineStageAction:
    def __init__(
        self,
        *,
        category: builtins.str,
        name: builtins.str,
        owner: builtins.str,
        provider: builtins.str,
        version: builtins.str,
        configuration: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        input_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        namespace: typing.Optional[builtins.str] = None,
        output_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        run_order: typing.Optional[jsii.Number] = None,
        timeout_in_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#category Codepipeline#category}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#name Codepipeline#name}.
        :param owner: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#owner Codepipeline#owner}.
        :param provider: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#provider Codepipeline#provider}.
        :param version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#version Codepipeline#version}.
        :param configuration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#configuration Codepipeline#configuration}.
        :param input_artifacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#input_artifacts Codepipeline#input_artifacts}.
        :param namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#namespace Codepipeline#namespace}.
        :param output_artifacts: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#output_artifacts Codepipeline#output_artifacts}.
        :param region: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#region Codepipeline#region}.
        :param role_arn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#role_arn Codepipeline#role_arn}.
        :param run_order: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#run_order Codepipeline#run_order}.
        :param timeout_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#timeout_in_minutes Codepipeline#timeout_in_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13f69913c0b6ea6e3efee6c519ce7ef6134ab72baa5cf682a9f77dffa02c3355)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument input_artifacts", value=input_artifacts, expected_type=type_hints["input_artifacts"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument output_artifacts", value=output_artifacts, expected_type=type_hints["output_artifacts"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument run_order", value=run_order, expected_type=type_hints["run_order"])
            check_type(argname="argument timeout_in_minutes", value=timeout_in_minutes, expected_type=type_hints["timeout_in_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
            "name": name,
            "owner": owner,
            "provider": provider,
            "version": version,
        }
        if configuration is not None:
            self._values["configuration"] = configuration
        if input_artifacts is not None:
            self._values["input_artifacts"] = input_artifacts
        if namespace is not None:
            self._values["namespace"] = namespace
        if output_artifacts is not None:
            self._values["output_artifacts"] = output_artifacts
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if run_order is not None:
            self._values["run_order"] = run_order
        if timeout_in_minutes is not None:
            self._values["timeout_in_minutes"] = timeout_in_minutes

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#category Codepipeline#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#name Codepipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#owner Codepipeline#owner}.'''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def provider(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#provider Codepipeline#provider}.'''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#version Codepipeline#version}.'''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#configuration Codepipeline#configuration}.'''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def input_artifacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#input_artifacts Codepipeline#input_artifacts}.'''
        result = self._values.get("input_artifacts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def namespace(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#namespace Codepipeline#namespace}.'''
        result = self._values.get("namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def output_artifacts(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#output_artifacts Codepipeline#output_artifacts}.'''
        result = self._values.get("output_artifacts")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#region Codepipeline#region}.'''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#role_arn Codepipeline#role_arn}.'''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#run_order Codepipeline#run_order}.'''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#timeout_in_minutes Codepipeline#timeout_in_minutes}.'''
        result = self._values.get("timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineStageAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineStageActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8810ed8d5fca6b86d5f3e61897150fee4d40ab3a38d59ec10d24620fc503d180)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CodepipelineStageActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb97058b9652c3aba975e5e01d27cea8ca71439863935e57c5f61422b70142d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineStageActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60afb90175647309fe7c3c8019e11a343b68fc29a57a14e64b75661caac136e4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea7e5de378084dca737e0bb27f3222530fde85d7da5493879516d21f2ec020bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7aa31127a50574768b62f5354e439ec55f690e4c318fecf9cff4a30e68fc853a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0365e5a923614b47962dd6a8869d692e0a3de517b8acf8be1912fbacbd24e855)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineStageActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a400239c0382a436b3c6e6aec4423109cf8bfabfbbc604da1dfed460acbef5a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetConfiguration")
    def reset_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfiguration", []))

    @jsii.member(jsii_name="resetInputArtifacts")
    def reset_input_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputArtifacts", []))

    @jsii.member(jsii_name="resetNamespace")
    def reset_namespace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNamespace", []))

    @jsii.member(jsii_name="resetOutputArtifacts")
    def reset_output_artifacts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputArtifacts", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetRoleArn")
    def reset_role_arn(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoleArn", []))

    @jsii.member(jsii_name="resetRunOrder")
    def reset_run_order(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunOrder", []))

    @jsii.member(jsii_name="resetTimeoutInMinutes")
    def reset_timeout_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeoutInMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="configurationInput")
    def configuration_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "configurationInput"))

    @builtins.property
    @jsii.member(jsii_name="inputArtifactsInput")
    def input_artifacts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceInput")
    def namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="outputArtifactsInput")
    def output_artifacts_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "outputArtifactsInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerInput")
    def owner_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerInput"))

    @builtins.property
    @jsii.member(jsii_name="providerInput")
    def provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="roleArnInput")
    def role_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleArnInput"))

    @builtins.property
    @jsii.member(jsii_name="runOrderInput")
    def run_order_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "runOrderInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinutesInput")
    def timeout_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "timeoutInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="versionInput")
    def version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b8bfb8f6f311dfd2c8864480e0a69f0fc9fa4058ed7aff6fcf7ddd64b11936)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c9e8d758e3e917ac8e3c987ad54d8dfcc34dd4ef0cfc04cd3c02c80ccb142bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputArtifacts")
    def input_artifacts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputArtifacts"))

    @input_artifacts.setter
    def input_artifacts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79aed965d763a80850ec35df4f28aa7aa6b309e39142c6ed4eed5b942d15215c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputArtifacts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fde050ff30bbba6a868783c14f24a03e2dff66fca2181ed6b68e1d41ed74c36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespace"))

    @namespace.setter
    def namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf79c669a7f32149d9c0c895f79a360c147f558bdc732d9b1dc3d8f67b64a33a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outputArtifacts")
    def output_artifacts(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outputArtifacts"))

    @output_artifacts.setter
    def output_artifacts(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b49df4f4a3a1a2307b65a67a3c2e392622acc223c6c585a54400751316635f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputArtifacts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="owner")
    def owner(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "owner"))

    @owner.setter
    def owner(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea2179eeb40922294027e6735014b9b45b3f866bbbc64be9c59668bf3f8261ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "owner", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "provider"))

    @provider.setter
    def provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5947bc93c77598764051ecf2a150a2ad8c3ddae39bd4e28c7164c6845173acc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "provider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29b0235e7359ea42567e71d8c02c370a2d9e26c0f6cc9738b86b3d77ef88c387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7231e16431dea3ee3f6f8266be621ac36bc00840ccad75d0fe089335de042be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runOrder")
    def run_order(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "runOrder"))

    @run_order.setter
    def run_order(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f779cddb97adc4192c224fd087dc5d1be6cff4a621ad19117e345c2a0990231d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runOrder", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeoutInMinutes")
    def timeout_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "timeoutInMinutes"))

    @timeout_in_minutes.setter
    def timeout_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f3da8b9f4d532706c6c385a41e72f9442ecd27fac1840df1a6386bfd0e1d556)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeoutInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @version.setter
    def version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db00699348ce1ed0c58ca53ca27d0459f964fda3b96fb586694139bb5e6ee1d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "version", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineStageAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineStageAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineStageAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b73a727fd3392933753d978f5d774e9d980acf7117ddfb7e0cd783218d9e08b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineStageList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2ed8257e31f6f1a4ed7c507154b4c4ea2445204db927df623b260cadd6a12e3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CodepipelineStageOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4a576933848558e35a815c240de4083c95316eb11f80b2c56f86db91ef86ee5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineStageOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e3361d1ae5071052934a34214614d23a156bccfe214018cedb8118c4ba9384)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c11680928851de7087d9cc1ba3919b684f4432ab17df32af118603705aee3286)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe4c2c59cb15d226951da63a32901733443c2aed7731d8422e41d774ce638e7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStage]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStage]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStage]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c820b92db9eaa2fd2b2b3d43f7d2862c8df043311e9c2e4b0b2db58e6c874591)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineStageOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineStageOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__85fbd29b809531d664bc8031778d57c94b24a586ecb8abcb50824d79aa7348d7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStageAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0b1faebfad19d4d53302e79f3e9810ce0f0caede05594062dc56c9c883e052)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> CodepipelineStageActionList:
        return typing.cast(CodepipelineStageActionList, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9583d78f934b5520a6a97e580d120baabd615bce279ff0119efa843b1d69ca97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineStage]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineStage]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineStage]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4843df9e290cc66526e96ccf25839b8fdd7126d05b00512e788bf75996a53a5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTrigger",
    jsii_struct_bases=[],
    name_mapping={
        "git_configuration": "gitConfiguration",
        "provider_type": "providerType",
    },
)
class CodepipelineTrigger:
    def __init__(
        self,
        *,
        git_configuration: typing.Union["CodepipelineTriggerGitConfiguration", typing.Dict[builtins.str, typing.Any]],
        provider_type: builtins.str,
    ) -> None:
        '''
        :param git_configuration: git_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#git_configuration Codepipeline#git_configuration}
        :param provider_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#provider_type Codepipeline#provider_type}.
        '''
        if isinstance(git_configuration, dict):
            git_configuration = CodepipelineTriggerGitConfiguration(**git_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab58e07662622dd9d47d0eeff079555c15bd4947432206493a67e745e450f2a)
            check_type(argname="argument git_configuration", value=git_configuration, expected_type=type_hints["git_configuration"])
            check_type(argname="argument provider_type", value=provider_type, expected_type=type_hints["provider_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "git_configuration": git_configuration,
            "provider_type": provider_type,
        }

    @builtins.property
    def git_configuration(self) -> "CodepipelineTriggerGitConfiguration":
        '''git_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#git_configuration Codepipeline#git_configuration}
        '''
        result = self._values.get("git_configuration")
        assert result is not None, "Required property 'git_configuration' is missing"
        return typing.cast("CodepipelineTriggerGitConfiguration", result)

    @builtins.property
    def provider_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#provider_type Codepipeline#provider_type}.'''
        result = self._values.get("provider_type")
        assert result is not None, "Required property 'provider_type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineTrigger(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "source_action_name": "sourceActionName",
        "pull_request": "pullRequest",
        "push": "push",
    },
)
class CodepipelineTriggerGitConfiguration:
    def __init__(
        self,
        *,
        source_action_name: builtins.str,
        pull_request: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineTriggerGitConfigurationPullRequest", typing.Dict[builtins.str, typing.Any]]]]] = None,
        push: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineTriggerGitConfigurationPush", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param source_action_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#source_action_name Codepipeline#source_action_name}.
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#pull_request Codepipeline#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#push Codepipeline#push}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd766cab73a1fd7e1b37f7697e50af2425c34bc0f38b9473ebb47bbee92a348a)
            check_type(argname="argument source_action_name", value=source_action_name, expected_type=type_hints["source_action_name"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument push", value=push, expected_type=type_hints["push"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_action_name": source_action_name,
        }
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if push is not None:
            self._values["push"] = push

    @builtins.property
    def source_action_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#source_action_name Codepipeline#source_action_name}.'''
        result = self._values.get("source_action_name")
        assert result is not None, "Required property 'source_action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def pull_request(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTriggerGitConfigurationPullRequest"]]]:
        '''pull_request block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#pull_request Codepipeline#pull_request}
        '''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTriggerGitConfigurationPullRequest"]]], result)

    @builtins.property
    def push(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTriggerGitConfigurationPush"]]]:
        '''push block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#push Codepipeline#push}
        '''
        result = self._values.get("push")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTriggerGitConfigurationPush"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineTriggerGitConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineTriggerGitConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0c0a845ef58520c1201fc0dfe82d9663fd2f2817917f328bdc916b099675d2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putPullRequest")
    def put_pull_request(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineTriggerGitConfigurationPullRequest", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c5bb3d683a17070b2e367683586453ebaa1f05d4346fdcfdd21904ce5aa4f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPullRequest", [value]))

    @jsii.member(jsii_name="putPush")
    def put_push(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["CodepipelineTriggerGitConfigurationPush", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42c04345fa51ffa5277d701c8e85d7abfaced674e028b553d8dd2dbf27ba8c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPush", [value]))

    @jsii.member(jsii_name="resetPullRequest")
    def reset_pull_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPullRequest", []))

    @jsii.member(jsii_name="resetPush")
    def reset_push(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPush", []))

    @builtins.property
    @jsii.member(jsii_name="pullRequest")
    def pull_request(self) -> "CodepipelineTriggerGitConfigurationPullRequestList":
        return typing.cast("CodepipelineTriggerGitConfigurationPullRequestList", jsii.get(self, "pullRequest"))

    @builtins.property
    @jsii.member(jsii_name="push")
    def push(self) -> "CodepipelineTriggerGitConfigurationPushList":
        return typing.cast("CodepipelineTriggerGitConfigurationPushList", jsii.get(self, "push"))

    @builtins.property
    @jsii.member(jsii_name="pullRequestInput")
    def pull_request_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTriggerGitConfigurationPullRequest"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTriggerGitConfigurationPullRequest"]]], jsii.get(self, "pullRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="pushInput")
    def push_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTriggerGitConfigurationPush"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["CodepipelineTriggerGitConfigurationPush"]]], jsii.get(self, "pushInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceActionNameInput")
    def source_action_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceActionNameInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceActionName")
    def source_action_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sourceActionName"))

    @source_action_name.setter
    def source_action_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f4e6e2c3f5d4a3a1b016f44e225cb1ecd2e9760869238811c1d1bc59f48ce3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceActionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[CodepipelineTriggerGitConfiguration]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodepipelineTriggerGitConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5fcff12c2589002286a1d5babc7ee7a60317a7360b8c3e99ef3d1b28c4fbfa5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPullRequest",
    jsii_struct_bases=[],
    name_mapping={
        "branches": "branches",
        "events": "events",
        "file_paths": "filePaths",
    },
)
class CodepipelineTriggerGitConfigurationPullRequest:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Union["CodepipelineTriggerGitConfigurationPullRequestBranches", typing.Dict[builtins.str, typing.Any]]] = None,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
        file_paths: typing.Optional[typing.Union["CodepipelineTriggerGitConfigurationPullRequestFilePaths", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param branches: branches block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#branches Codepipeline#branches}
        :param events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#events Codepipeline#events}.
        :param file_paths: file_paths block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#file_paths Codepipeline#file_paths}
        '''
        if isinstance(branches, dict):
            branches = CodepipelineTriggerGitConfigurationPullRequestBranches(**branches)
        if isinstance(file_paths, dict):
            file_paths = CodepipelineTriggerGitConfigurationPullRequestFilePaths(**file_paths)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91e8a25427ddb52d9eadb69b1084afe1e57848dd85fa222c3f6a8bac1ea5f54)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument file_paths", value=file_paths, expected_type=type_hints["file_paths"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if events is not None:
            self._values["events"] = events
        if file_paths is not None:
            self._values["file_paths"] = file_paths

    @builtins.property
    def branches(
        self,
    ) -> typing.Optional["CodepipelineTriggerGitConfigurationPullRequestBranches"]:
        '''branches block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#branches Codepipeline#branches}
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional["CodepipelineTriggerGitConfigurationPullRequestBranches"], result)

    @builtins.property
    def events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#events Codepipeline#events}.'''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def file_paths(
        self,
    ) -> typing.Optional["CodepipelineTriggerGitConfigurationPullRequestFilePaths"]:
        '''file_paths block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#file_paths Codepipeline#file_paths}
        '''
        result = self._values.get("file_paths")
        return typing.cast(typing.Optional["CodepipelineTriggerGitConfigurationPullRequestFilePaths"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineTriggerGitConfigurationPullRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPullRequestBranches",
    jsii_struct_bases=[],
    name_mapping={"excludes": "excludes", "includes": "includes"},
)
class CodepipelineTriggerGitConfigurationPullRequestBranches:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8277f4d733d5d16807d44bec690d442af43afab4d68dc1f69fe3e1c4e4a5bc67)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.'''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.'''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineTriggerGitConfigurationPullRequestBranches(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineTriggerGitConfigurationPullRequestBranchesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPullRequestBranchesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7407ad7b4e0bcdb9d02f0a89283a4648fcfbed885bc1128838ee8202180d66ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetIncludes")
    def reset_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludes", []))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="includesInput")
    def includes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1ff75a48ec3e6ada730ef77b81ea38fab180437ec645b40acb2f239bdf5a24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includes"))

    @includes.setter
    def includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a79f496b1f851145614d6cde5b22f0b639ca9c8f08b4bc11995fa87d8e70e6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfigurationPullRequestBranches]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfigurationPullRequestBranches], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodepipelineTriggerGitConfigurationPullRequestBranches],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4dc69391280aaa6c1b29e2e0476ee727fb3747c5d10428fce8ad8cc39668b7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPullRequestFilePaths",
    jsii_struct_bases=[],
    name_mapping={"excludes": "excludes", "includes": "includes"},
)
class CodepipelineTriggerGitConfigurationPullRequestFilePaths:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29d0139cf1c84fe55552f261d17bc325bdbd5d9d580ab2b43612438683e5de36)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.'''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.'''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineTriggerGitConfigurationPullRequestFilePaths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineTriggerGitConfigurationPullRequestFilePathsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPullRequestFilePathsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3049fbe37db283cb91a30352e7f7be14ab4f49ddc38706cc20dcd8aaf98f9b2b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetIncludes")
    def reset_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludes", []))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="includesInput")
    def includes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f3fb97d33d28149de6cd166a467371086b55047cf6cfb1a6614b4742c1b45a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includes"))

    @includes.setter
    def includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0056e83b22eae8dcfe4e95afa23e80f8d016fff1dcb67e034b65640372a4becd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfigurationPullRequestFilePaths]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfigurationPullRequestFilePaths], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodepipelineTriggerGitConfigurationPullRequestFilePaths],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b764b3378c873318d3183afa100d07c8221785d0b9e6e42b7231af4d241f866)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineTriggerGitConfigurationPullRequestList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPullRequestList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0eb66f43408f7fe3cd560c79fc60cd00484622b34ad402c4cfd7dca581856a15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodepipelineTriggerGitConfigurationPullRequestOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c68634d627e610d1cbd4d2250d4d7ea0206034a0f9e67a726c1bba0eecbf94f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineTriggerGitConfigurationPullRequestOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9f636b5bf8131f904799c7f362f3886400b56e676187dcc57cd99f1ebd7642f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2767a24daca0fa29b6d48c8f51a810288dc9c828019752a5ff0173e01e2e3e8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__43c073af22d0a6dcdb7aeac1b7e35ce698a33e101ebdaf3f52bcd91f56bd9ea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTriggerGitConfigurationPullRequest]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTriggerGitConfigurationPullRequest]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTriggerGitConfigurationPullRequest]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1f2cc9412381a4998c1cf280a716c12366576ab81f8237a0a7e7fb553f10de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineTriggerGitConfigurationPullRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPullRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bb900a68fbb8d232ab1a7d32f9fd37987a8c578ae51cf5dcbb17e971be9553b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBranches")
    def put_branches(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        value = CodepipelineTriggerGitConfigurationPullRequestBranches(
            excludes=excludes, includes=includes
        )

        return typing.cast(None, jsii.invoke(self, "putBranches", [value]))

    @jsii.member(jsii_name="putFilePaths")
    def put_file_paths(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        value = CodepipelineTriggerGitConfigurationPullRequestFilePaths(
            excludes=excludes, includes=includes
        )

        return typing.cast(None, jsii.invoke(self, "putFilePaths", [value]))

    @jsii.member(jsii_name="resetBranches")
    def reset_branches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranches", []))

    @jsii.member(jsii_name="resetEvents")
    def reset_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvents", []))

    @jsii.member(jsii_name="resetFilePaths")
    def reset_file_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePaths", []))

    @builtins.property
    @jsii.member(jsii_name="branches")
    def branches(
        self,
    ) -> CodepipelineTriggerGitConfigurationPullRequestBranchesOutputReference:
        return typing.cast(CodepipelineTriggerGitConfigurationPullRequestBranchesOutputReference, jsii.get(self, "branches"))

    @builtins.property
    @jsii.member(jsii_name="filePaths")
    def file_paths(
        self,
    ) -> CodepipelineTriggerGitConfigurationPullRequestFilePathsOutputReference:
        return typing.cast(CodepipelineTriggerGitConfigurationPullRequestFilePathsOutputReference, jsii.get(self, "filePaths"))

    @builtins.property
    @jsii.member(jsii_name="branchesInput")
    def branches_input(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfigurationPullRequestBranches]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfigurationPullRequestBranches], jsii.get(self, "branchesInput"))

    @builtins.property
    @jsii.member(jsii_name="eventsInput")
    def events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventsInput"))

    @builtins.property
    @jsii.member(jsii_name="filePathsInput")
    def file_paths_input(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfigurationPullRequestFilePaths]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfigurationPullRequestFilePaths], jsii.get(self, "filePathsInput"))

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "events"))

    @events.setter
    def events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cee01bc7e632fba6c500a39bbd2079f96a07959492295662bb8f3dd262d7bfe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTriggerGitConfigurationPullRequest]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTriggerGitConfigurationPullRequest]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTriggerGitConfigurationPullRequest]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb574e81553c592b59779f49b1f5595bb51b1cf5458859da6e30ae5599b37eee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPush",
    jsii_struct_bases=[],
    name_mapping={"branches": "branches", "file_paths": "filePaths", "tags": "tags"},
)
class CodepipelineTriggerGitConfigurationPush:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Union["CodepipelineTriggerGitConfigurationPushBranches", typing.Dict[builtins.str, typing.Any]]] = None,
        file_paths: typing.Optional[typing.Union["CodepipelineTriggerGitConfigurationPushFilePaths", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Union["CodepipelineTriggerGitConfigurationPushTags", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param branches: branches block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#branches Codepipeline#branches}
        :param file_paths: file_paths block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#file_paths Codepipeline#file_paths}
        :param tags: tags block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#tags Codepipeline#tags}
        '''
        if isinstance(branches, dict):
            branches = CodepipelineTriggerGitConfigurationPushBranches(**branches)
        if isinstance(file_paths, dict):
            file_paths = CodepipelineTriggerGitConfigurationPushFilePaths(**file_paths)
        if isinstance(tags, dict):
            tags = CodepipelineTriggerGitConfigurationPushTags(**tags)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e535f18cba02e0fcf5f277e71e038a02f9fca04015b679f17c565ad0e23ef77d)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument file_paths", value=file_paths, expected_type=type_hints["file_paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if file_paths is not None:
            self._values["file_paths"] = file_paths
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def branches(
        self,
    ) -> typing.Optional["CodepipelineTriggerGitConfigurationPushBranches"]:
        '''branches block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#branches Codepipeline#branches}
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional["CodepipelineTriggerGitConfigurationPushBranches"], result)

    @builtins.property
    def file_paths(
        self,
    ) -> typing.Optional["CodepipelineTriggerGitConfigurationPushFilePaths"]:
        '''file_paths block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#file_paths Codepipeline#file_paths}
        '''
        result = self._values.get("file_paths")
        return typing.cast(typing.Optional["CodepipelineTriggerGitConfigurationPushFilePaths"], result)

    @builtins.property
    def tags(self) -> typing.Optional["CodepipelineTriggerGitConfigurationPushTags"]:
        '''tags block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#tags Codepipeline#tags}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional["CodepipelineTriggerGitConfigurationPushTags"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineTriggerGitConfigurationPush(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPushBranches",
    jsii_struct_bases=[],
    name_mapping={"excludes": "excludes", "includes": "includes"},
)
class CodepipelineTriggerGitConfigurationPushBranches:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42cd2414b4f209f64689304840cc9984bcc5fdd8e7954b8f9162da3942bdb0b3)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.'''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.'''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineTriggerGitConfigurationPushBranches(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineTriggerGitConfigurationPushBranchesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPushBranchesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e93262e798687cc3daedc52cda5d70881552e2d12041c6d145e0e2bd2ce8cd52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetIncludes")
    def reset_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludes", []))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="includesInput")
    def includes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce4100cca9228bd96d225a5a0eec912b728afb0df498910fcfe56259543d6c18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includes"))

    @includes.setter
    def includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83f37d15ab8c063e50a4c794f45faa897e8eb0e2c74e30538b2e3dca7c513ed6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfigurationPushBranches]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfigurationPushBranches], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodepipelineTriggerGitConfigurationPushBranches],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27ece39ef25abef883513a2ac5536701db70db2dde3e652e56869cf62c72537d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPushFilePaths",
    jsii_struct_bases=[],
    name_mapping={"excludes": "excludes", "includes": "includes"},
)
class CodepipelineTriggerGitConfigurationPushFilePaths:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c7b5b6747402d8b4fdc3c66120c6eca9fcb06bcee1ca428d0de1eef9be53ea)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.'''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.'''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineTriggerGitConfigurationPushFilePaths(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineTriggerGitConfigurationPushFilePathsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPushFilePathsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a099285dbaa3d401cba51ca9afcb43e24e53a45004a01ac95b13989bf93b91a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetIncludes")
    def reset_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludes", []))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="includesInput")
    def includes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1e20597eb6dda03c09f00cf6d14d92a581ac2f339351043c44e3951bbc08073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includes"))

    @includes.setter
    def includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d17047aa8302556dd4bb2ff8fef3230ef93446d6f5472a189ba9ba5a4b9aa941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfigurationPushFilePaths]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfigurationPushFilePaths], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodepipelineTriggerGitConfigurationPushFilePaths],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__889845af3fdb24a49954822a4ba0f6dc8c2739acaeacdc28c7e8dad6a44514fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineTriggerGitConfigurationPushList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPushList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74c6ddaf360c867b3b56e56efa5cbcc7ea2d280db3b5228fd963f81e24feb6a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "CodepipelineTriggerGitConfigurationPushOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0890b67aee9e9c35ff67ba6bf1a45e47b530d3fea7c1fdb7f8f39528a0f076e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineTriggerGitConfigurationPushOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3387027a06edaf77c1cf11de7c65349f2b6674126faf43b3124be766173adb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c916330433d292dabaedcb447f31d1138fb67acfd31708444e8ccd6d181fdb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7404263b5dbc05f2a2acaee24c1ac30d2e256173b817a2fd5c385b4bcbd62dcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTriggerGitConfigurationPush]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTriggerGitConfigurationPush]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTriggerGitConfigurationPush]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b31d6f37288a090b0a59f8fb227a601baf7cb8e298131b8d0d948d56923ffbe6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineTriggerGitConfigurationPushOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPushOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__00c628a466447633bce7d63b66618142df3b271b6bf4391a304131d9a62a4054)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putBranches")
    def put_branches(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        value = CodepipelineTriggerGitConfigurationPushBranches(
            excludes=excludes, includes=includes
        )

        return typing.cast(None, jsii.invoke(self, "putBranches", [value]))

    @jsii.member(jsii_name="putFilePaths")
    def put_file_paths(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        value = CodepipelineTriggerGitConfigurationPushFilePaths(
            excludes=excludes, includes=includes
        )

        return typing.cast(None, jsii.invoke(self, "putFilePaths", [value]))

    @jsii.member(jsii_name="putTags")
    def put_tags(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        value = CodepipelineTriggerGitConfigurationPushTags(
            excludes=excludes, includes=includes
        )

        return typing.cast(None, jsii.invoke(self, "putTags", [value]))

    @jsii.member(jsii_name="resetBranches")
    def reset_branches(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBranches", []))

    @jsii.member(jsii_name="resetFilePaths")
    def reset_file_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFilePaths", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @builtins.property
    @jsii.member(jsii_name="branches")
    def branches(
        self,
    ) -> CodepipelineTriggerGitConfigurationPushBranchesOutputReference:
        return typing.cast(CodepipelineTriggerGitConfigurationPushBranchesOutputReference, jsii.get(self, "branches"))

    @builtins.property
    @jsii.member(jsii_name="filePaths")
    def file_paths(
        self,
    ) -> CodepipelineTriggerGitConfigurationPushFilePathsOutputReference:
        return typing.cast(CodepipelineTriggerGitConfigurationPushFilePathsOutputReference, jsii.get(self, "filePaths"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> "CodepipelineTriggerGitConfigurationPushTagsOutputReference":
        return typing.cast("CodepipelineTriggerGitConfigurationPushTagsOutputReference", jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="branchesInput")
    def branches_input(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfigurationPushBranches]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfigurationPushBranches], jsii.get(self, "branchesInput"))

    @builtins.property
    @jsii.member(jsii_name="filePathsInput")
    def file_paths_input(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfigurationPushFilePaths]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfigurationPushFilePaths], jsii.get(self, "filePathsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(
        self,
    ) -> typing.Optional["CodepipelineTriggerGitConfigurationPushTags"]:
        return typing.cast(typing.Optional["CodepipelineTriggerGitConfigurationPushTags"], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTriggerGitConfigurationPush]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTriggerGitConfigurationPush]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTriggerGitConfigurationPush]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca376b6ac6ab1578763e227bded177fc4c17e66706ce5e10e1a23d99f28fccf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPushTags",
    jsii_struct_bases=[],
    name_mapping={"excludes": "excludes", "includes": "includes"},
)
class CodepipelineTriggerGitConfigurationPushTags:
    def __init__(
        self,
        *,
        excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param excludes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.
        :param includes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d4dff5122dbfc60ce4024fa10ce78e5de8f92b5d77e14a150a98f4d60b04b93)
            check_type(argname="argument excludes", value=excludes, expected_type=type_hints["excludes"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if excludes is not None:
            self._values["excludes"] = excludes
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def excludes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#excludes Codepipeline#excludes}.'''
        result = self._values.get("excludes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#includes Codepipeline#includes}.'''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineTriggerGitConfigurationPushTags(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineTriggerGitConfigurationPushTagsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerGitConfigurationPushTagsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de3d6010a9cb6cd5bdf0cf403a587fdcd2528e54c5884dcd8d48f2122d1ca446)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetExcludes")
    def reset_excludes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludes", []))

    @jsii.member(jsii_name="resetIncludes")
    def reset_includes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncludes", []))

    @builtins.property
    @jsii.member(jsii_name="excludesInput")
    def excludes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludesInput"))

    @builtins.property
    @jsii.member(jsii_name="includesInput")
    def includes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "includesInput"))

    @builtins.property
    @jsii.member(jsii_name="excludes")
    def excludes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludes"))

    @excludes.setter
    def excludes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb72a826a97876cb9792a1c76036ff4818d0627221f27f88ecac38ddd57a5b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="includes")
    def includes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "includes"))

    @includes.setter
    def includes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc22c54972d42d31477cbb29ec82c8609205c9eaffc52350c6470c3e7c54454)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfigurationPushTags]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfigurationPushTags], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[CodepipelineTriggerGitConfigurationPushTags],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba485afecfc7426e2562bc0fd145acd785a3b1fb76cbc1d0876900f6de1868bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineTriggerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c736d0ee29efd597f97f1c2c7ea346b19970651a0c0cf94866d8be9101752fe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CodepipelineTriggerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d730695377f7b173e0c11d5b868a465e3e92caf5999abd23b3d80cf5f58646)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineTriggerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b37a6390e5d1fa8fd47528202f486b5afc889bf1144ad4060fd5207bdc722047)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7478e1fa145c71f66f804134dd34a3f4ced565b31e7d275c165dca353c5a3921)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32202d5bd48c18226f45a17b7d1fb2e6c31c96686c727c4de2ad4d3d3e3056f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTrigger]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTrigger]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTrigger]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f79dfdde2a6391cf71c3a14cdb66011795a5f5310ea9d1f946283eea46ea9e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineTriggerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineTriggerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2fd393d8fd5f27a08b0f1636e6c21e3f18bc6c782a79c7fe3be1fb0f0dcd51ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putGitConfiguration")
    def put_git_configuration(
        self,
        *,
        source_action_name: builtins.str,
        pull_request: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineTriggerGitConfigurationPullRequest, typing.Dict[builtins.str, typing.Any]]]]] = None,
        push: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineTriggerGitConfigurationPush, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param source_action_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#source_action_name Codepipeline#source_action_name}.
        :param pull_request: pull_request block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#pull_request Codepipeline#pull_request}
        :param push: push block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#push Codepipeline#push}
        '''
        value = CodepipelineTriggerGitConfiguration(
            source_action_name=source_action_name, pull_request=pull_request, push=push
        )

        return typing.cast(None, jsii.invoke(self, "putGitConfiguration", [value]))

    @builtins.property
    @jsii.member(jsii_name="gitConfiguration")
    def git_configuration(self) -> CodepipelineTriggerGitConfigurationOutputReference:
        return typing.cast(CodepipelineTriggerGitConfigurationOutputReference, jsii.get(self, "gitConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="gitConfigurationInput")
    def git_configuration_input(
        self,
    ) -> typing.Optional[CodepipelineTriggerGitConfiguration]:
        return typing.cast(typing.Optional[CodepipelineTriggerGitConfiguration], jsii.get(self, "gitConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="providerTypeInput")
    def provider_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "providerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="providerType")
    def provider_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "providerType"))

    @provider_type.setter
    def provider_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50cd6a51b2f4476ddfc52e08a92bd7c0d15facd99ad64e06f4d31c2f37bbcbb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "providerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTrigger]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTrigger]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTrigger]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__068355edec37d55e04d9cdd5c2cc31057586a259f0ca9ac309b6eeea9f222ece)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineVariable",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "default_value": "defaultValue",
        "description": "description",
    },
)
class CodepipelineVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        default_value: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#name Codepipeline#name}.
        :param default_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#default_value Codepipeline#default_value}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#description Codepipeline#description}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dd56bd1a5f88858d81d7c74c28dd95740706bae1617eb10c91e3f2d18c1e5fb)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument default_value", value=default_value, expected_type=type_hints["default_value"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if default_value is not None:
            self._values["default_value"] = default_value
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#name Codepipeline#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#default_value Codepipeline#default_value}.'''
        result = self._values.get("default_value")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/5.79.0/docs/resources/codepipeline#description Codepipeline#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodepipelineVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodepipelineVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e755ed02def77b4ffaec748f5ecbcb978221f6edb92d1be980b62bdc253c4db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "CodepipelineVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed33744b577583be66cee72770cd55628d80e3de63b198e29c56bf6eab904fc7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("CodepipelineVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1baba675d73af82e0a3ce640dd40dd869894d8ea7e1616eea034c454ae22c8f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1a888012d16033b157e150231e1257d1099458ed84cf192fd1c490f36ecdf49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80ec1e3dd038790b3328ca7df46074493edca06c807cc1b53f5cc97e652e9d7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67c412d9dfe765979e16f00d51cf2d33b69fac2fd7ea3e11f05f262660897efb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class CodepipelineVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.codepipeline.CodepipelineVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__610bfda73513170069ef1d3635f43dddd2d4d1bca31a1b4777af07b39a6e6da7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDefaultValue")
    def reset_default_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultValue", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @builtins.property
    @jsii.member(jsii_name="defaultValueInput")
    def default_value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultValueInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultValue")
    def default_value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultValue"))

    @default_value.setter
    def default_value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__964a89fd8671a3c1e0c855588b1ad3aead8e6792d0591f95d4088f25bfe11110)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94903d32f714e2f75ac7c22196b5e932eb1cb2edcd9cbde553483166d8a44b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4884221d948553e11b5e3e6ed6464cd83d2cec9af62781a22f613f61c1ec07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf4a2f21c52aa5885f566f6ae95a2c51ec957800fe62f5ed93a8faf293a2875)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "Codepipeline",
    "CodepipelineArtifactStore",
    "CodepipelineArtifactStoreEncryptionKey",
    "CodepipelineArtifactStoreEncryptionKeyOutputReference",
    "CodepipelineArtifactStoreList",
    "CodepipelineArtifactStoreOutputReference",
    "CodepipelineConfig",
    "CodepipelineStage",
    "CodepipelineStageAction",
    "CodepipelineStageActionList",
    "CodepipelineStageActionOutputReference",
    "CodepipelineStageList",
    "CodepipelineStageOutputReference",
    "CodepipelineTrigger",
    "CodepipelineTriggerGitConfiguration",
    "CodepipelineTriggerGitConfigurationOutputReference",
    "CodepipelineTriggerGitConfigurationPullRequest",
    "CodepipelineTriggerGitConfigurationPullRequestBranches",
    "CodepipelineTriggerGitConfigurationPullRequestBranchesOutputReference",
    "CodepipelineTriggerGitConfigurationPullRequestFilePaths",
    "CodepipelineTriggerGitConfigurationPullRequestFilePathsOutputReference",
    "CodepipelineTriggerGitConfigurationPullRequestList",
    "CodepipelineTriggerGitConfigurationPullRequestOutputReference",
    "CodepipelineTriggerGitConfigurationPush",
    "CodepipelineTriggerGitConfigurationPushBranches",
    "CodepipelineTriggerGitConfigurationPushBranchesOutputReference",
    "CodepipelineTriggerGitConfigurationPushFilePaths",
    "CodepipelineTriggerGitConfigurationPushFilePathsOutputReference",
    "CodepipelineTriggerGitConfigurationPushList",
    "CodepipelineTriggerGitConfigurationPushOutputReference",
    "CodepipelineTriggerGitConfigurationPushTags",
    "CodepipelineTriggerGitConfigurationPushTagsOutputReference",
    "CodepipelineTriggerList",
    "CodepipelineTriggerOutputReference",
    "CodepipelineVariable",
    "CodepipelineVariableList",
    "CodepipelineVariableOutputReference",
]

publication.publish()

def _typecheckingstub__8b05bf9d470a6d541c6793d8c11b37ee4652aafe5fdf5945767bdae8987af99b(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    artifact_store: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineArtifactStore, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    role_arn: builtins.str,
    stage: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStage, typing.Dict[builtins.str, typing.Any]]]],
    execution_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pipeline_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineTrigger, typing.Dict[builtins.str, typing.Any]]]]] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__70ded069c6455f301d07a57e4ce2aab355427daa2c00f59657bbbc6af533bf0e(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f10383963c155174b899e60ffc8f2f98399552b79c35a4de6c1594d741e354f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineArtifactStore, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df349ff7dee10b41aa6aba23f53a3bbf1505b0a1e6327689dc5c6b4f314ad09f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStage, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20fed748b626d96524e76b790203bba5a85d495bd2bd16a24fc9a4daac4eaf2a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineTrigger, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea92293a59909fbde979e65918ccf343a98a17be2322d9716fdaf87810f5857e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d37a3ba48aa73ff30a54fd7550b8a970ef72607f4a9bceb975692b4d7acf147(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93f2b93040cead7a9937f01217f6352ea2233d2f400256af3f7e4a7b14cdb3bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad2c1e89e83d86c1039aaf9c1d57abcc0a27d9005cac5eb9a3baf63292f59bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfcb0d67474d8ca9a6da721f60a72a90512d1eea234aee394b190a8c9e4a6160(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d5a262fb418a52d9c077ee2a5b67d24123f15ddcf4a7cb9682b8266004f6d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6ed8943de3fd52a65f1a6203dee739473e5c0cc0256f454d374149682de34b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e16b43e185b495bb94719ac17a947d8bc348193f0e70826ee610bdcd94037d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__922068355d678dd6effd40fe938c7b4bef095e80aafdc157f6347e9a154a7455(
    *,
    location: builtins.str,
    type: builtins.str,
    encryption_key: typing.Optional[typing.Union[CodepipelineArtifactStoreEncryptionKey, typing.Dict[builtins.str, typing.Any]]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d46126b88ec0637b8870b9918772f62c576de320afd50301c51ff6f2cb4a730(
    *,
    id: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46c941e35195f370c8e8fed484db32b46c4930061ab32816151a6c9a77ed98a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4af46ebfe947a3e6650b847155aeebc7fd20abb38822fc8a7fa9b66abe127f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6397c6cc84d9b854c5d220f016d81c03041b1cc9f7a19e2737721e673175d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f5a35c64dd518ba782d6fe1f72bc901c94647985fcb0f0410d8a36f9758c73(
    value: typing.Optional[CodepipelineArtifactStoreEncryptionKey],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98845279dd07aa22f658694ce2d785b2f63880044cbc224cd270f73c530ed666(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__110e0ac1b03bc412da726cf99c749a3213d21c96fa6fd765c2801666adaf8ad2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbd95915f530001cb29302739bba967dc100350855e39797e71f05c760586e1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388da3f1639c681b74313cc4f5d5034f54a9d30b265701a8ab65b3bf5fdf4b41(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d3d3d63a3a0886461f20af849e3daeac985588a43d5adb1259efd4988d0a3f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6b396dc65bdc3cb55da1e64f1ae1eccffb88c9a19379fe9adc874336629afa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineArtifactStore]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a9282c02570c1515b4ff146f29d98b0405b3f91c8562927c494269fbdf24ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7073ace0c2ac96908ecd48678800c927f8ee9ea800a55ea3dff5d90d9bd7491(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644a35e7f02a989e4b3fdc9403a5a8d0921a77fdd69b886960fd8556e66a71f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3433081d5bd0381c76a04f4ce558aaf0808eac349c000c7a1f846a58c357cbbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a1b57429ee5766a4a1051555294a5e0a3065da41c51ae3aa106edc5bdc97d2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineArtifactStore]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__009e693604d53e9e0598d73e0bbcfe99d252352f522377b683d9881d7516179f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    artifact_store: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineArtifactStore, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    role_arn: builtins.str,
    stage: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStage, typing.Dict[builtins.str, typing.Any]]]],
    execution_mode: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    pipeline_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    trigger: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineTrigger, typing.Dict[builtins.str, typing.Any]]]]] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f317cae47d1d43bfefb03a17abc49f8c36567a6558090d426f042e0b34d27a61(
    *,
    action: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStageAction, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13f69913c0b6ea6e3efee6c519ce7ef6134ab72baa5cf682a9f77dffa02c3355(
    *,
    category: builtins.str,
    name: builtins.str,
    owner: builtins.str,
    provider: builtins.str,
    version: builtins.str,
    configuration: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    input_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    namespace: typing.Optional[builtins.str] = None,
    output_artifacts: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    run_order: typing.Optional[jsii.Number] = None,
    timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8810ed8d5fca6b86d5f3e61897150fee4d40ab3a38d59ec10d24620fc503d180(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb97058b9652c3aba975e5e01d27cea8ca71439863935e57c5f61422b70142d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60afb90175647309fe7c3c8019e11a343b68fc29a57a14e64b75661caac136e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7e5de378084dca737e0bb27f3222530fde85d7da5493879516d21f2ec020bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa31127a50574768b62f5354e439ec55f690e4c318fecf9cff4a30e68fc853a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0365e5a923614b47962dd6a8869d692e0a3de517b8acf8be1912fbacbd24e855(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStageAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a400239c0382a436b3c6e6aec4423109cf8bfabfbbc604da1dfed460acbef5a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b8bfb8f6f311dfd2c8864480e0a69f0fc9fa4058ed7aff6fcf7ddd64b11936(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c9e8d758e3e917ac8e3c987ad54d8dfcc34dd4ef0cfc04cd3c02c80ccb142bd(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79aed965d763a80850ec35df4f28aa7aa6b309e39142c6ed4eed5b942d15215c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fde050ff30bbba6a868783c14f24a03e2dff66fca2181ed6b68e1d41ed74c36(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf79c669a7f32149d9c0c895f79a360c147f558bdc732d9b1dc3d8f67b64a33a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b49df4f4a3a1a2307b65a67a3c2e392622acc223c6c585a54400751316635f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea2179eeb40922294027e6735014b9b45b3f866bbbc64be9c59668bf3f8261ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5947bc93c77598764051ecf2a150a2ad8c3ddae39bd4e28c7164c6845173acc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29b0235e7359ea42567e71d8c02c370a2d9e26c0f6cc9738b86b3d77ef88c387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7231e16431dea3ee3f6f8266be621ac36bc00840ccad75d0fe089335de042be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f779cddb97adc4192c224fd087dc5d1be6cff4a621ad19117e345c2a0990231d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f3da8b9f4d532706c6c385a41e72f9442ecd27fac1840df1a6386bfd0e1d556(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db00699348ce1ed0c58ca53ca27d0459f964fda3b96fb586694139bb5e6ee1d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b73a727fd3392933753d978f5d774e9d980acf7117ddfb7e0cd783218d9e08b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineStageAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2ed8257e31f6f1a4ed7c507154b4c4ea2445204db927df623b260cadd6a12e3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4a576933848558e35a815c240de4083c95316eb11f80b2c56f86db91ef86ee5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e3361d1ae5071052934a34214614d23a156bccfe214018cedb8118c4ba9384(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c11680928851de7087d9cc1ba3919b684f4432ab17df32af118603705aee3286(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe4c2c59cb15d226951da63a32901733443c2aed7731d8422e41d774ce638e7b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c820b92db9eaa2fd2b2b3d43f7d2862c8df043311e9c2e4b0b2db58e6c874591(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineStage]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85fbd29b809531d664bc8031778d57c94b24a586ecb8abcb50824d79aa7348d7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0b1faebfad19d4d53302e79f3e9810ce0f0caede05594062dc56c9c883e052(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineStageAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9583d78f934b5520a6a97e580d120baabd615bce279ff0119efa843b1d69ca97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4843df9e290cc66526e96ccf25839b8fdd7126d05b00512e788bf75996a53a5c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineStage]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab58e07662622dd9d47d0eeff079555c15bd4947432206493a67e745e450f2a(
    *,
    git_configuration: typing.Union[CodepipelineTriggerGitConfiguration, typing.Dict[builtins.str, typing.Any]],
    provider_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd766cab73a1fd7e1b37f7697e50af2425c34bc0f38b9473ebb47bbee92a348a(
    *,
    source_action_name: builtins.str,
    pull_request: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineTriggerGitConfigurationPullRequest, typing.Dict[builtins.str, typing.Any]]]]] = None,
    push: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineTriggerGitConfigurationPush, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0c0a845ef58520c1201fc0dfe82d9663fd2f2817917f328bdc916b099675d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c5bb3d683a17070b2e367683586453ebaa1f05d4346fdcfdd21904ce5aa4f2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineTriggerGitConfigurationPullRequest, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42c04345fa51ffa5277d701c8e85d7abfaced674e028b553d8dd2dbf27ba8c48(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[CodepipelineTriggerGitConfigurationPush, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f4e6e2c3f5d4a3a1b016f44e225cb1ecd2e9760869238811c1d1bc59f48ce3f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5fcff12c2589002286a1d5babc7ee7a60317a7360b8c3e99ef3d1b28c4fbfa5(
    value: typing.Optional[CodepipelineTriggerGitConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91e8a25427ddb52d9eadb69b1084afe1e57848dd85fa222c3f6a8bac1ea5f54(
    *,
    branches: typing.Optional[typing.Union[CodepipelineTriggerGitConfigurationPullRequestBranches, typing.Dict[builtins.str, typing.Any]]] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
    file_paths: typing.Optional[typing.Union[CodepipelineTriggerGitConfigurationPullRequestFilePaths, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8277f4d733d5d16807d44bec690d442af43afab4d68dc1f69fe3e1c4e4a5bc67(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7407ad7b4e0bcdb9d02f0a89283a4648fcfbed885bc1128838ee8202180d66ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1ff75a48ec3e6ada730ef77b81ea38fab180437ec645b40acb2f239bdf5a24d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a79f496b1f851145614d6cde5b22f0b639ca9c8f08b4bc11995fa87d8e70e6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4dc69391280aaa6c1b29e2e0476ee727fb3747c5d10428fce8ad8cc39668b7a(
    value: typing.Optional[CodepipelineTriggerGitConfigurationPullRequestBranches],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29d0139cf1c84fe55552f261d17bc325bdbd5d9d580ab2b43612438683e5de36(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3049fbe37db283cb91a30352e7f7be14ab4f49ddc38706cc20dcd8aaf98f9b2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f3fb97d33d28149de6cd166a467371086b55047cf6cfb1a6614b4742c1b45a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0056e83b22eae8dcfe4e95afa23e80f8d016fff1dcb67e034b65640372a4becd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b764b3378c873318d3183afa100d07c8221785d0b9e6e42b7231af4d241f866(
    value: typing.Optional[CodepipelineTriggerGitConfigurationPullRequestFilePaths],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb66f43408f7fe3cd560c79fc60cd00484622b34ad402c4cfd7dca581856a15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c68634d627e610d1cbd4d2250d4d7ea0206034a0f9e67a726c1bba0eecbf94f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9f636b5bf8131f904799c7f362f3886400b56e676187dcc57cd99f1ebd7642f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2767a24daca0fa29b6d48c8f51a810288dc9c828019752a5ff0173e01e2e3e8a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c073af22d0a6dcdb7aeac1b7e35ce698a33e101ebdaf3f52bcd91f56bd9ea8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1f2cc9412381a4998c1cf280a716c12366576ab81f8237a0a7e7fb553f10de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTriggerGitConfigurationPullRequest]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bb900a68fbb8d232ab1a7d32f9fd37987a8c578ae51cf5dcbb17e971be9553b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cee01bc7e632fba6c500a39bbd2079f96a07959492295662bb8f3dd262d7bfe0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb574e81553c592b59779f49b1f5595bb51b1cf5458859da6e30ae5599b37eee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTriggerGitConfigurationPullRequest]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e535f18cba02e0fcf5f277e71e038a02f9fca04015b679f17c565ad0e23ef77d(
    *,
    branches: typing.Optional[typing.Union[CodepipelineTriggerGitConfigurationPushBranches, typing.Dict[builtins.str, typing.Any]]] = None,
    file_paths: typing.Optional[typing.Union[CodepipelineTriggerGitConfigurationPushFilePaths, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Union[CodepipelineTriggerGitConfigurationPushTags, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42cd2414b4f209f64689304840cc9984bcc5fdd8e7954b8f9162da3942bdb0b3(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93262e798687cc3daedc52cda5d70881552e2d12041c6d145e0e2bd2ce8cd52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce4100cca9228bd96d225a5a0eec912b728afb0df498910fcfe56259543d6c18(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83f37d15ab8c063e50a4c794f45faa897e8eb0e2c74e30538b2e3dca7c513ed6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27ece39ef25abef883513a2ac5536701db70db2dde3e652e56869cf62c72537d(
    value: typing.Optional[CodepipelineTriggerGitConfigurationPushBranches],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c7b5b6747402d8b4fdc3c66120c6eca9fcb06bcee1ca428d0de1eef9be53ea(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a099285dbaa3d401cba51ca9afcb43e24e53a45004a01ac95b13989bf93b91a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1e20597eb6dda03c09f00cf6d14d92a581ac2f339351043c44e3951bbc08073(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17047aa8302556dd4bb2ff8fef3230ef93446d6f5472a189ba9ba5a4b9aa941(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__889845af3fdb24a49954822a4ba0f6dc8c2739acaeacdc28c7e8dad6a44514fa(
    value: typing.Optional[CodepipelineTriggerGitConfigurationPushFilePaths],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c6ddaf360c867b3b56e56efa5cbcc7ea2d280db3b5228fd963f81e24feb6a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0890b67aee9e9c35ff67ba6bf1a45e47b530d3fea7c1fdb7f8f39528a0f076e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3387027a06edaf77c1cf11de7c65349f2b6674126faf43b3124be766173adb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c916330433d292dabaedcb447f31d1138fb67acfd31708444e8ccd6d181fdb3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7404263b5dbc05f2a2acaee24c1ac30d2e256173b817a2fd5c385b4bcbd62dcb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b31d6f37288a090b0a59f8fb227a601baf7cb8e298131b8d0d948d56923ffbe6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTriggerGitConfigurationPush]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00c628a466447633bce7d63b66618142df3b271b6bf4391a304131d9a62a4054(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca376b6ac6ab1578763e227bded177fc4c17e66706ce5e10e1a23d99f28fccf5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTriggerGitConfigurationPush]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d4dff5122dbfc60ce4024fa10ce78e5de8f92b5d77e14a150a98f4d60b04b93(
    *,
    excludes: typing.Optional[typing.Sequence[builtins.str]] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3d6010a9cb6cd5bdf0cf403a587fdcd2528e54c5884dcd8d48f2122d1ca446(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb72a826a97876cb9792a1c76036ff4818d0627221f27f88ecac38ddd57a5b33(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc22c54972d42d31477cbb29ec82c8609205c9eaffc52350c6470c3e7c54454(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba485afecfc7426e2562bc0fd145acd785a3b1fb76cbc1d0876900f6de1868bf(
    value: typing.Optional[CodepipelineTriggerGitConfigurationPushTags],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c736d0ee29efd597f97f1c2c7ea346b19970651a0c0cf94866d8be9101752fe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d730695377f7b173e0c11d5b868a465e3e92caf5999abd23b3d80cf5f58646(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b37a6390e5d1fa8fd47528202f486b5afc889bf1144ad4060fd5207bdc722047(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7478e1fa145c71f66f804134dd34a3f4ced565b31e7d275c165dca353c5a3921(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32202d5bd48c18226f45a17b7d1fb2e6c31c96686c727c4de2ad4d3d3e3056f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f79dfdde2a6391cf71c3a14cdb66011795a5f5310ea9d1f946283eea46ea9e26(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineTrigger]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fd393d8fd5f27a08b0f1636e6c21e3f18bc6c782a79c7fe3be1fb0f0dcd51ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50cd6a51b2f4476ddfc52e08a92bd7c0d15facd99ad64e06f4d31c2f37bbcbb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__068355edec37d55e04d9cdd5c2cc31057586a259f0ca9ac309b6eeea9f222ece(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineTrigger]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dd56bd1a5f88858d81d7c74c28dd95740706bae1617eb10c91e3f2d18c1e5fb(
    *,
    name: builtins.str,
    default_value: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e755ed02def77b4ffaec748f5ecbcb978221f6edb92d1be980b62bdc253c4db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed33744b577583be66cee72770cd55628d80e3de63b198e29c56bf6eab904fc7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1baba675d73af82e0a3ce640dd40dd869894d8ea7e1616eea034c454ae22c8f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1a888012d16033b157e150231e1257d1099458ed84cf192fd1c490f36ecdf49(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80ec1e3dd038790b3328ca7df46074493edca06c807cc1b53f5cc97e652e9d7f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c412d9dfe765979e16f00d51cf2d33b69fac2fd7ea3e11f05f262660897efb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[CodepipelineVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610bfda73513170069ef1d3635f43dddd2d4d1bca31a1b4777af07b39a6e6da7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964a89fd8671a3c1e0c855588b1ad3aead8e6792d0591f95d4088f25bfe11110(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94903d32f714e2f75ac7c22196b5e932eb1cb2edcd9cbde553483166d8a44b27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4884221d948553e11b5e3e6ed6464cd83d2cec9af62781a22f613f61c1ec07a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf4a2f21c52aa5885f566f6ae95a2c51ec957800fe62f5ed93a8faf293a2875(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, CodepipelineVariable]],
) -> None:
    """Type checking stubs"""
    pass
