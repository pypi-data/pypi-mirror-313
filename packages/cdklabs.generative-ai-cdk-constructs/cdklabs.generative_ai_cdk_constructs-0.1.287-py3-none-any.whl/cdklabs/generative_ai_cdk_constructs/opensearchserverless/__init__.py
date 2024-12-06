r'''
# Amazon OpenSearch Serverless Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> All classes are under active development and subject to non-backward compatible changes or removal in any
> future version. These are not subject to the [Semantic Versioning](https://semver.org/) model.
> This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

| **Language**     | **Package**        |
|:-------------|-----------------|
|![Typescript Logo](https://docs.aws.amazon.com/cdk/api/latest/img/typescript32.png) TypeScript|`@cdklabs/generative-ai-cdk-constructs`|
|![Python Logo](https://docs.aws.amazon.com/cdk/api/latest/img/python32.png) Python|`cdklabs.generative_ai_cdk_constructs`|

This construct library extends the [automatically generated L1 constructs](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_opensearchserverless-readme.html) to provide an L2 construct for a vector collection.

## Table of contents

* [API](#api)
* [Vector Collection](#vector-collection)

## API

See the [API documentation](../../../apidocs/namespaces/opensearchserverless/README.md).

## Vector Collection

This resource creates an Amazon OpenSearch Serverless collection configured for `VECTORSEARCH`. It creates default encryption, network, and data policies for use with Amazon Bedrock Knowledge Bases. For encryption, it uses the default AWS owned KMS key. It allows network connections from the public internet, but access is restricted to specific IAM principals.

### Granting Data Access

The `grantDataAccess` method grants the specified role access to read and write the data in the collection.
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_opensearchserverless as _aws_cdk_aws_opensearchserverless_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.opensearchserverless.CharacterFilterType"
)
class CharacterFilterType(enum.Enum):
    '''(experimental) Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.

    Licensed under the Apache License, Version 2.0 (the "License"). You may not use this file except in compliance
    with the License. A copy of the License is located at Example::

       http://www.apache.org/licenses/LICENSE-2.0

    or in the 'license' file accompanying this file. This file is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES
    OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific language governing permissions
    and limitations under the License.

    :stability: experimental
    '''

    ICU_NORMALIZER = "ICU_NORMALIZER"
    '''
    :stability: experimental
    '''


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.opensearchserverless.TokenFilterType"
)
class TokenFilterType(enum.Enum):
    '''
    :stability: experimental
    '''

    KUROMOJI_BASEFORM = "KUROMOJI_BASEFORM"
    '''
    :stability: experimental
    '''
    KUROMOJI_PART_OF_SPEECH = "KUROMOJI_PART_OF_SPEECH"
    '''
    :stability: experimental
    '''
    KUROMOJI_STEMMER = "KUROMOJI_STEMMER"
    '''
    :stability: experimental
    '''
    CJK_WIDTH = "CJK_WIDTH"
    '''
    :stability: experimental
    '''
    JA_STOP = "JA_STOP"
    '''
    :stability: experimental
    '''
    LOWERCASE = "LOWERCASE"
    '''
    :stability: experimental
    '''
    ICU_FOLDING = "ICU_FOLDING"
    '''
    :stability: experimental
    '''


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.opensearchserverless.TokenizerType"
)
class TokenizerType(enum.Enum):
    '''
    :stability: experimental
    '''

    KUROMOJI_TOKENIZER = "KUROMOJI_TOKENIZER"
    '''
    :stability: experimental
    '''
    ICU_TOKENIZER = "ICU_TOKENIZER"
    '''
    :stability: experimental
    '''


class VectorCollection(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdklabs/generative-ai-cdk-constructs.opensearchserverless.VectorCollection",
):
    '''(experimental) Deploys an OpenSearch Serverless Collection to be used as a vector store.

    It includes all policies.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        collection_name: builtins.str,
        custom_aoss_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy] = None,
        standby_replicas: typing.Optional["VectorCollectionStandbyReplicas"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param collection_name: (experimental) The name of the collection.
        :param custom_aoss_policy: (experimental) A user defined IAM policy that allows API access to the collection.
        :param standby_replicas: (experimental) Indicates whether to use standby replicas for the collection. Default: ENABLED

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b5d04fb7b72dad69932d437e1081404a6e72cb7ba26b7a53f6a739062e8d10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = VectorCollectionProps(
            collection_name=collection_name,
            custom_aoss_policy=custom_aoss_policy,
            standby_replicas=standby_replicas,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantDataAccess")
    def grant_data_access(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grants the specified role access to data in the collection.

        :param grantee: The role to grant access to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c320f537c9d5613bd4eb9158b6f299c7e1d9bbb4f3f8d0c9ad66b1f31b3fb013)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantDataAccess", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="aossPolicy")
    def aoss_policy(self) -> _aws_cdk_aws_iam_ceddda9d.ManagedPolicy:
        '''(experimental) An IAM policy that allows API access to the collection.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.ManagedPolicy, jsii.get(self, "aossPolicy"))

    @aoss_policy.setter
    def aoss_policy(self, value: _aws_cdk_aws_iam_ceddda9d.ManagedPolicy) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e6b1b914ecb08f8add2426201fb5b172a5496e41d55879a9893e923d69e785)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aossPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collectionArn")
    def collection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the collection.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "collectionArn"))

    @collection_arn.setter
    def collection_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__345d8f58416dc282452d28f65ded785c6ca5ea312386630b253c0b93f77bb70d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionArn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collectionId")
    def collection_id(self) -> builtins.str:
        '''(experimental) The ID of the collection.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "collectionId"))

    @collection_id.setter
    def collection_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1abc38143c045f29ad4aad4050a02395094f115c30f78638bc317f2bd10eda3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="collectionName")
    def collection_name(self) -> builtins.str:
        '''(experimental) The name of the collection.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "collectionName"))

    @collection_name.setter
    def collection_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d681c75e2c727fed94552b17f76e3eeb61763bf17fbeb7302ab6f36d0b6e943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "collectionName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dataAccessPolicy")
    def data_access_policy(
        self,
    ) -> _aws_cdk_aws_opensearchserverless_ceddda9d.CfnAccessPolicy:
        '''(experimental) An OpenSearch Access Policy that allows access to the index.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_opensearchserverless_ceddda9d.CfnAccessPolicy, jsii.get(self, "dataAccessPolicy"))

    @data_access_policy.setter
    def data_access_policy(
        self,
        value: _aws_cdk_aws_opensearchserverless_ceddda9d.CfnAccessPolicy,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__064b48f9a1698a63c4504ba3a91564cd33e089498d79ec502bdd747c6ce09294)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataAccessPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="standbyReplicas")
    def standby_replicas(self) -> "VectorCollectionStandbyReplicas":
        '''(experimental) Indicates whether to use standby replicas for the collection.

        :stability: experimental
        '''
        return typing.cast("VectorCollectionStandbyReplicas", jsii.get(self, "standbyReplicas"))

    @standby_replicas.setter
    def standby_replicas(self, value: "VectorCollectionStandbyReplicas") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__802ec9e6f4804378bc578f3818fd93e1ab7dad3ffad6d5de766f87d39360e4c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "standbyReplicas", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.opensearchserverless.VectorCollectionProps",
    jsii_struct_bases=[],
    name_mapping={
        "collection_name": "collectionName",
        "custom_aoss_policy": "customAossPolicy",
        "standby_replicas": "standbyReplicas",
    },
)
class VectorCollectionProps:
    def __init__(
        self,
        *,
        collection_name: builtins.str,
        custom_aoss_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy] = None,
        standby_replicas: typing.Optional["VectorCollectionStandbyReplicas"] = None,
    ) -> None:
        '''
        :param collection_name: (experimental) The name of the collection.
        :param custom_aoss_policy: (experimental) A user defined IAM policy that allows API access to the collection.
        :param standby_replicas: (experimental) Indicates whether to use standby replicas for the collection. Default: ENABLED

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363fe2209dfff74d63efdde544ff5c64a896cadfcf9de13b0a7cd45812b23897)
            check_type(argname="argument collection_name", value=collection_name, expected_type=type_hints["collection_name"])
            check_type(argname="argument custom_aoss_policy", value=custom_aoss_policy, expected_type=type_hints["custom_aoss_policy"])
            check_type(argname="argument standby_replicas", value=standby_replicas, expected_type=type_hints["standby_replicas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "collection_name": collection_name,
        }
        if custom_aoss_policy is not None:
            self._values["custom_aoss_policy"] = custom_aoss_policy
        if standby_replicas is not None:
            self._values["standby_replicas"] = standby_replicas

    @builtins.property
    def collection_name(self) -> builtins.str:
        '''(experimental) The name of the collection.

        :stability: experimental
        '''
        result = self._values.get("collection_name")
        assert result is not None, "Required property 'collection_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_aoss_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy]:
        '''(experimental) A user defined IAM policy that allows API access to the collection.

        :stability: experimental
        '''
        result = self._values.get("custom_aoss_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy], result)

    @builtins.property
    def standby_replicas(self) -> typing.Optional["VectorCollectionStandbyReplicas"]:
        '''(experimental) Indicates whether to use standby replicas for the collection.

        :default: ENABLED

        :stability: experimental
        '''
        result = self._values.get("standby_replicas")
        return typing.cast(typing.Optional["VectorCollectionStandbyReplicas"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VectorCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(
    jsii_type="@cdklabs/generative-ai-cdk-constructs.opensearchserverless.VectorCollectionStandbyReplicas"
)
class VectorCollectionStandbyReplicas(enum.Enum):
    '''
    :stability: experimental
    '''

    ENABLED = "ENABLED"
    '''
    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''
    :stability: experimental
    '''


__all__ = [
    "CharacterFilterType",
    "TokenFilterType",
    "TokenizerType",
    "VectorCollection",
    "VectorCollectionProps",
    "VectorCollectionStandbyReplicas",
]

publication.publish()

def _typecheckingstub__c8b5d04fb7b72dad69932d437e1081404a6e72cb7ba26b7a53f6a739062e8d10(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    collection_name: builtins.str,
    custom_aoss_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy] = None,
    standby_replicas: typing.Optional[VectorCollectionStandbyReplicas] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c320f537c9d5613bd4eb9158b6f299c7e1d9bbb4f3f8d0c9ad66b1f31b3fb013(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41e6b1b914ecb08f8add2426201fb5b172a5496e41d55879a9893e923d69e785(
    value: _aws_cdk_aws_iam_ceddda9d.ManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__345d8f58416dc282452d28f65ded785c6ca5ea312386630b253c0b93f77bb70d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1abc38143c045f29ad4aad4050a02395094f115c30f78638bc317f2bd10eda3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d681c75e2c727fed94552b17f76e3eeb61763bf17fbeb7302ab6f36d0b6e943(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064b48f9a1698a63c4504ba3a91564cd33e089498d79ec502bdd747c6ce09294(
    value: _aws_cdk_aws_opensearchserverless_ceddda9d.CfnAccessPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__802ec9e6f4804378bc578f3818fd93e1ab7dad3ffad6d5de766f87d39360e4c8(
    value: VectorCollectionStandbyReplicas,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363fe2209dfff74d63efdde544ff5c64a896cadfcf9de13b0a7cd45812b23897(
    *,
    collection_name: builtins.str,
    custom_aoss_policy: typing.Optional[_aws_cdk_aws_iam_ceddda9d.ManagedPolicy] = None,
    standby_replicas: typing.Optional[VectorCollectionStandbyReplicas] = None,
) -> None:
    """Type checking stubs"""
    pass
