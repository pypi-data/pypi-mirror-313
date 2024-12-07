r'''
# projen-simple

[![License](https://img.shields.io/badge/License-Apache%202.0-green)](https://opensource.org/licenses/Apache-2.0) ![Release](https://github.com/HsiehShuJeng/projen-simple/workflows/Release/badge.svg) [![npm downloads](https://img.shields.io/npm/dt/projen-statemachine-example?label=npm%20downloads&style=plastic)](https://img.shields.io/npm/dt/projen-statemachine-example?label=npm%20downloads&style=plastic) [![pypi downloads](https://img.shields.io/pypi/dm/scotthsieh-projen-statemachine?label=pypi%20downloads&style=plastic)](https://img.shields.io/pypi/dm/scotthsieh-projen-statemachine?label=pypi%20downloads&style=plastic) [![NuGet downloads](https://img.shields.io/nuget/dt/Projen.Statemachine?label=NuGet%20downloads&style=plastic)](https://img.shields.io/nuget/dt/Projen.Statemachine?label=NuGet%20downloads&style=plastic) [![repo languages](https://img.shields.io/github/languages/count/HsiehShuJeng/projen-simple?label=repo%20languages&style=plastic)](https://img.shields.io/github/languages/count/HsiehShuJeng/projen-simple?label=repo%20languages&style=plastic)

| npm (JS/TS) | PyPI (Python) | Maven (Java) | Go | NuGet |
| --- | --- | --- | --- | --- |
| [Link](https://www.npmjs.com/package/projen-simple) | [Link](https://pypi.org/project/scotthsieh_projen_statemachine/) | [Link](https://search.maven.org/artifact/io.github.hsiehshujeng/projen-statemachine) | [Link](https://github.com/HsiehShuJeng/projen-statemachine-go) | [Link](https://www.nuget.org/packages/Projen.Statemachine/) |

Build a custom construct based on an example in an AWS Blog post and use [projen](https://github.com/projen/projen) to publish to 5 language repositories, i.e., npm, PyPI, Central Maven, NuGet, and Go.

# Architecture

This library constrcution is referred to the first example in this AWS blog, [*Introducing Amazon API Gateway service integration for AWS Step Functions*](https://aws.amazon.com/tw/blogs/compute/introducing-amazon-api-gateway-service-integration-for-aws-step-functions/) written by Benjanmin Smith. After you deploy the stack with whatever programming language you like, i.e., Typescript, Python, Java, or C sharp, you'll get a view similar to the following diagram:
![image](https://raw.githubusercontent.com/HsiehShuJeng/projen-simple/main/images/designer_view.png)

# How to utilize polyglot packages and deploy

## TypeScript

```bash
$ cdk --init language typescript
$ yarn add projen-statemachine-example
```

```python
import { StateMachineApiGatewayExample } from 'projen-statemachine-example';

 export class TypescriptStack extends cdk.Stack {
 constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
     super(scope, id, props);

     const stageName = 'default';
     const partPath = 'pets';
     const exampleConstruct = new StateMachineApiGatewayExample(this, 'KerKer', {
         stageName: stageName, partPath: partPath});

     new cdk.CfnOutput(this, 'OStateMachine', {
         value: exampleConstruct.stateMachine.stateMachineArn});
     new cdk.CfnOutput(this, 'OExecutionOutput', {
         value: exampleConstruct.executionInput, description: 'Sample input to StartExecution.'});
 }
```

## Python

```bash
$ cdk init --language python
$ cat <<EOL > requirements.txt
aws-cdk.core
scotthsieh_projen_statemachine
EOL
$ python -m pip install -r requirements.txt
```

```python
from aws_cdk import core as cdk
from scotthsieh_projen_statemachine import StateMachineApiGatewayExample

class PythonStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
         super().__init__(scope, construct_id, **kwargs)

         stage_name = 'default'
         part_path = 'pets'
         example_construct = StateMachineApiGatewayExample(
             self, 'PythonStatemachne', stage_name=stage_name, part_path=part_path,
         )

         cdk.CfnOutput(self, "OStateMachine",
             value=example_construct.state_machine.state_machine_arn
         )
         cdk.CfnOutput(self, "OExecutionOutput", value=example_construct.execution_input, description="Sample input to StartExecution.")
```

## Java

```bash
$ cdk init --language java
$ mvn package
```

```xml
.
.
<properties>
     <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
     <custom.construct.version>2.0.474</custom.construct.version>
     <cdk.version>2.149.0</cdk.version>
     <junit.version>5.7.1</junit.version>
 </properties>
 .
 .
 <dependencies>
     <!-- AWS Cloud Development Kit -->
     .
     .
     .
     <dependency>
         <groupId>io.github.hsiehshujeng</groupId>
         <artifactId>projen-statemachine</artifactId>
         <version>${custom.construct.version}</version>
     </dependency>
     .
     .
     .
 </dependencies>
```

```java
package com.myorg;

import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.CfnOutputProps;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import io.github.hsiehshujeng.projen.statemachine.*;

public class JavaStack extends Stack {
    public JavaStack(final Construct scope, final String id) {
        this(scope, id, null);
     }

     public JavaStack(final Construct scope, final String id, final StackProps props) {
         super(scope, id, props);

         String stageName = "default";
         String partPath = "pets";
         StateMachineApiGatewayExample exampleConstruct = new StateMachineApiGatewayExample(this, "KerKer",
             StateMachineApiGatewayExampleProps.builder()
                 .stageName(stageName)
                 .partPath(partPath)
                 .build());

         new CfnOutput(this, "OStateMachine",
             CfnOutputProps.builder()
                 .value(exampleConstruct.getStateMachine().getStateMachineArn())
                 .build());
         new CfnOutput(this, "OExecutionOutput", CfnOutputProps.builder()
             .value(exampleConstruct.getExecutionInput())
             .description("Sample input to StartExecution.")
             .build());
     }
 }
```

## C#

```bash
$ cdk init --language csharp
$ dotnet add src/Csharp package Projen.Statemachine --version 2.0.474
```

```cs
using Amazon.CDK;
using ScottHsieh.Examples;

namespace Csharp
{
    public class CsharpStack : Stack
    {
        internal CsharpStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            string stageName = "default";
            string partPath = "pets";

            var exampleConstruct = new StateMachineApiGatewayExample(this, "KerKer", new StateMachineApiGatewayExampleProps
            {
                StageName = stageName,
                PartPath = partPath
            });

            new CfnOutput(this, "OStateMachine", new CfnOutputProps
            {
                Value = exampleConstruct.StateMachine.StateMachineArn
            });
            new CfnOutput(this, "OExecutionOutput", new CfnOutputProps
            {
                Value = exampleConstruct.ExecutionInput,
                Description = "Sample input to StartExecution."
            });
        }
    }
 }
```

# References

* [jsii reference](https://github.com/cdklabs/jsii-release)
* [aws-cdk-go](https://github.com/aws/aws-cdk-go)
* [jsii](https://github.com/aws/jsii)
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

import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


class StateMachineApiGatewayExample(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="projen-statemachine-example.StateMachineApiGatewayExample",
):
    '''Converted from an AWS Blog post.

    It is the first example mentioned in https://aws.amazon.com/tw/blogs/compute/introducing-amazon-api-gateway-service-integration-for-aws-step-functions/.
    This constcut will create an API Gateway Rest API with two methods and
    are manipulated by a state machine managed in AWS StepFucntions.
    '''

    def __init__(
        self,
        parent: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        part_path: builtins.str,
        stage_name: builtins.str,
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param part_path: The path part for the resource. Default: 'pets'
        :param stage_name: A stage name for the rest api. Default: 'default'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad1cb3d16bf4c589e6f533d3f0deaded8ff39f147b0601c7402f7763c009067)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = StateMachineApiGatewayExampleProps(
            part_path=part_path, stage_name=stage_name
        )

        jsii.create(self.__class__, self, [parent, name, props])

    @builtins.property
    @jsii.member(jsii_name="executionInput")
    def execution_input(self) -> builtins.str:
        '''sample input to start execution for the workflow.'''
        return typing.cast(builtins.str, jsii.get(self, "executionInput"))

    @builtins.property
    @jsii.member(jsii_name="stateMachine")
    def state_machine(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine:
        '''the representation of a state machine.'''
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine, jsii.get(self, "stateMachine"))


@jsii.data_type(
    jsii_type="projen-statemachine-example.StateMachineApiGatewayExampleProps",
    jsii_struct_bases=[],
    name_mapping={"part_path": "partPath", "stage_name": "stageName"},
)
class StateMachineApiGatewayExampleProps:
    def __init__(self, *, part_path: builtins.str, stage_name: builtins.str) -> None:
        '''
        :param part_path: The path part for the resource. Default: 'pets'
        :param stage_name: A stage name for the rest api. Default: 'default'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf67ea2efe50b06d70277e2d568cdf3fd9f28657db36b8ccb15fe6771df5e1e)
            check_type(argname="argument part_path", value=part_path, expected_type=type_hints["part_path"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "part_path": part_path,
            "stage_name": stage_name,
        }

    @builtins.property
    def part_path(self) -> builtins.str:
        '''The path part for the resource.

        :default: 'pets'
        '''
        result = self._values.get("part_path")
        assert result is not None, "Required property 'part_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''A stage name for the rest api.

        :default: 'default'
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateMachineApiGatewayExampleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "StateMachineApiGatewayExample",
    "StateMachineApiGatewayExampleProps",
]

publication.publish()

def _typecheckingstub__5ad1cb3d16bf4c589e6f533d3f0deaded8ff39f147b0601c7402f7763c009067(
    parent: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    part_path: builtins.str,
    stage_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf67ea2efe50b06d70277e2d568cdf3fd9f28657db36b8ccb15fe6771df5e1e(
    *,
    part_path: builtins.str,
    stage_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
