r'''
## `cdk-cr-constructs`

This Construct is collect custom resource

### Example for CustomResourceGetEIP

```python
import { App, Stack, CfnOutput, Duration, aws_iam } from 'aws-cdk-lib';
import { CustomResourceGetEIP } from 'cdk-cr-constructs';
const env = {
  region: process.env.CDK_DEFAULT_REGION,
  account: process.env.CDK_DEFAULT_ACCOUNT,
};
const app = new App();
const stack = new Stack(app, 'testing-stack', { env });
const getIps = new CustomResourceGetEIP(stack, 'CustomResourceGetEIP', {
  /**
   * Discovery us-east-1 Elastic Ips.
   */
  regions: ['us-east-1'],
  /**
   * Add Company Ips.
   */
  companyIps: ['1.2.3.4'],
});
const role = new aws_iam.Role(stack, 'DemoRole', {
  assumedBy: new aws_iam.AccountRootPrincipal(),
});
/**
 * Example create an assume role, allow all action from ip address.
*/
role.addToPolicy(new aws_iam.PolicyStatement({
  effect: aws_iam.Effect.ALLOW,
  resources: ['*'],
  actions: ['*'],
  conditions: {
    IpAddress: {
      'aws:SourceIp': getIps.ipList(),
    },
  },
}));
```
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

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import constructs as _constructs_77d1e7e8


class CustomResourceGetEIP(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-cr-constructs.CustomResourceGetEIP",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: typing.Optional["ICustomResourceGetEIPOptions"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41e92ecb65cc8964973470e63e3e33b23920125494af3a6a91d1efc9c1a0d613)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="ipList")
    def ip_list(self) -> typing.List[builtins.str]:
        '''
        :return: Token.asList(this.outputs.getAtt('IP_LIST'));

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "ipList", []))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> _aws_cdk_ceddda9d.CustomResource:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.CustomResource, jsii.get(self, "outputs"))

    @outputs.setter
    def outputs(self, value: _aws_cdk_ceddda9d.CustomResource) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8bab6ea0e2944299e426ef8b91d8c3d4d81a6ef4f906fcf8efdeb647139e3d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outputs", value) # pyright: ignore[reportArgumentType]


@jsii.interface(jsii_type="cdk-cr-constructs.ICustomResourceGetEIPOptions")
class ICustomResourceGetEIPOptions(typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="alwaysUpdate")
    def always_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicate whether always update the custom resource to get the new stack output.

        :default: true

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="companyIps")
    def company_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        ...


class _ICustomResourceGetEIPOptionsProxy:
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "cdk-cr-constructs.ICustomResourceGetEIPOptions"

    @builtins.property
    @jsii.member(jsii_name="alwaysUpdate")
    def always_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicate whether always update the custom resource to get the new stack output.

        :default: true

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "alwaysUpdate"))

    @builtins.property
    @jsii.member(jsii_name="companyIps")
    def company_ips(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "companyIps"))

    @builtins.property
    @jsii.member(jsii_name="regions")
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "regions"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICustomResourceGetEIPOptions).__jsii_proxy_class__ = lambda : _ICustomResourceGetEIPOptionsProxy


__all__ = [
    "CustomResourceGetEIP",
    "ICustomResourceGetEIPOptions",
]

publication.publish()

def _typecheckingstub__41e92ecb65cc8964973470e63e3e33b23920125494af3a6a91d1efc9c1a0d613(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: typing.Optional[ICustomResourceGetEIPOptions] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bab6ea0e2944299e426ef8b91d8c3d4d81a6ef4f906fcf8efdeb647139e3d8(
    value: _aws_cdk_ceddda9d.CustomResource,
) -> None:
    """Type checking stubs"""
    pass
