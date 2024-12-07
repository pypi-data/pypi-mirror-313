r'''
# cdk-lambda-subminute

[![License](https://img.shields.io/badge/License-Apache%202.0-green)](https://opensource.org/licenses/Apache-2.0) [![Release](https://github.com/HsiehShuJeng/cdk-lambda-subminute/workflows/Release/badge.svg)](https://github.com/HsiehShuJeng/cdk-lambda-subminute/actions/workflows/release.yml) [![npm downloads](https://img.shields.io/npm/dt/cdk-lambda-subminute?label=npm%20downloads&style=plastic)](https://img.shields.io/npm/dt/cdk-lambda-subminute?label=npm%20downloads&style=plastic) [![pypi downloads](https://img.shields.io/pypi/dm/cdk-lambda-subminute?label=pypi%20downloads&style=plastic)](https://img.shields.io/pypi/dm/cdk-lambda-subminute?label=pypi%20downloads&style=plastic) [![NuGet downloads](https://img.shields.io/nuget/dt/Lambda.Subminute?label=NuGet%20downloads&style=plastic)](https://img.shields.io/nuget/dt/Lambda.Subminute?label=NuGet%20downloads&style=plastic) [![repo languages](https://img.shields.io/github/languages/count/HsiehShuJeng/cdk-lambda-subminute?style=plastic)](https://img.shields.io/github/languages/count/HsiehShuJeng/cdk-lambda-subminute?style=plastic)

| npm (JS/TS) | PyPI (Python) | Maven (Java) | Go | NuGet |
| --- | --- | --- | --- | --- |
| [Link](https://www.npmjs.com/package/cdk-lambda-subminute) | [Link](https://pypi.org/project/cdk_lambda_subminute/) | [Link](https://search.maven.org/artifact/io.github.hsiehshujeng/cdk-lambda-subminute) | [Link](https://github.com/HsiehShuJeng/cdk-lambda-subminute-go) | [Link](https://www.nuget.org/packages/Lambda.Subminute/) |

This construct creates a state machine that can invoke a Lambda function per time unit which can be less than one minute, such as invoking every 10 seconds. You only need to craft a Lambda function and then assign it as an argument into the construct. An example is included.

# Serverless Architecture

<p align="center"><img src="https://raw.githubusercontent.com/HsiehShuJeng/cdk-lambda-subminute/main/images/cdk_lambda_subminute.png"/></p>

# Introduction

This construct library is reffered to thie AWS Architecture blog post, [*A serverless solution for invoking AWS Lambda at a sub-minute frequency*](https://aws.amazon.com/tw/blogs/architecture/a-serverless-solution-for-invoking-aws-lambda-at-a-sub-minute-frequency/), written by **Emanuele Menga**. I made it as a constrcut library where you only need to care about a target Lambda function, how frequent and how long you want to execute.

# Example

## Typescript

You could also refer to [here](https://github.com/HsiehShuJeng/cdk-lambda-subminute/tree/main/src/demo/typescript).

```bash
$ cdk --init language typescript
$ yarn add cdk-lambda-subminute
```

```python
class TypescriptStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const targetLabmda = new Function(this, 'targetFunction', {
      code: Code.fromInline('exports.handler = function(event, ctx, cb) { return cb(null, "hi"); })'), // It's just a simple function for demonstration purpose only.
      functionName: 'testTargetFunction',
      runtime: Runtime.NODEJS_18_X,
      handler: 'index.handler',
    });
    const cronJobExample = 'cron(50/1 15-17 ? * SUN-SAT *)';
    const subminuteMaster = new LambdaSubminute(this, 'LambdaSubminute', { targetFunction: targetLabmda, cronjobExpression: cronJobExample });

    new cdk.CfnOutput(this, 'OStateMachineArn', { value: subminuteMaster.stateMachineArn });
    new cdk.CfnOutput(this, 'OIteratorFunctionArn', { value: subminuteMaster.iteratorFunction.functionArn });
  }
}

const app = new cdk.App();
new TypescriptStack(app, 'TypescriptStack', {
});
```

## Python

You could also refer to [here](https://github.com/HsiehShuJeng/cdk-lambda-subminute/tree/main/src/demo/python).

```bash
# upgrading related Python packages
$ python -m ensurepip --upgrade
$ python -m pip install --upgrade pip
$ python -m pip install --upgrade virtualenv
# initialize a CDK Python project
$ cdk init --language python
# make packages installed locally instead of globally
$ source .venv/bin/activate
$ cat <<EOL > requirements.txt
aws-cdk.core
aws-cdk.aws-lambda
cdk-lambda-subminute
EOL
$ python -m pip install -r requirements.txt
```

```python
from aws_cdk import core as cdk
from aws_cdk.aws_lambda import Code, Function, Runtime
from cdk_lambda_subminute import LambdaSubminute

class PythonStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        target_lambda = Function(
            self, "targetFunction",
            code=Code.from_inline(
                "exports.handler = function(event, ctx, cb) { return cb(null, \"hi\"); })"),
            function_name="testTargetFunction",
            runtime=Runtime.NODEJS_18_X,
            handler="index.handler"
        )
        cron_job_example = "cron(10/1 4-5 ? * SUN-SAT *)"
        subminute_master = LambdaSubminute(
            self, "LambdaSubminute",
            target_function=target_lambda,
            cronjob_expression=cron_job_example,
            frequency=7,
            interval_time=8)

        cdk.CfnOutput(self, "OStateMachineArn",
                      value=subminute_master.state_machine_arn)
        cdk.CfnOutput(self, "OIteratorFunctionArn",
                      value=subminute_master.iterator_function.function_arn)
```

```bash
$ deactivate
```

## Java

You could also refer to [here](https://github.com/HsiehShuJeng/cdk-lambda-subminute/tree/main/src/demo/java).

```bash
$ cdk init --language java
$ mvn package
```

```xml
.
.
<properties>
      <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
      <cdk.version>2.149.0</cdk.version>
      <constrcut.verion>2.0.442</constrcut.verion>
      <junit.version>5.7.1</junit.version>
</properties>
 .
 .
 <dependencies>
     <!-- AWS Cloud Development Kit -->
      <dependency>
            <groupId>software.amazon.awscdk</groupId>
            <artifactId>core</artifactId>
            <version>${cdk.version}</version>
      </dependency>
      <dependency>
            <groupId>software.amazon.awscdk</groupId>
            <artifactId>lambda</artifactId>
            <version>${cdk.version}</version>
      </dependency>
      <dependency>
            <groupId>io.github.hsiehshujeng</groupId>
            <artifactId>cdk-lambda-subminute</artifactId>
            <version>${constrcut.verion}</version>
      </dependency>
     .
     .
     .
 </dependencies>
```

```java
package com.myorg;

import software.amazon.awscdk.core.CfnOutput;
import software.amazon.awscdk.core.CfnOutputProps;
import software.amazon.awscdk.core.Construct;
import software.amazon.awscdk.core.Stack;
import software.amazon.awscdk.core.StackProps;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.Function;
import software.amazon.awscdk.services.lambda.FunctionProps;
import software.amazon.awscdk.services.lambda.Runtime;
import io.github.hsiehshujeng.cdk.lambda.subminute.LambdaSubminute;
import io.github.hsiehshujeng.cdk.lambda.subminute.LambdaSubminuteProps;

public class JavaStack extends Stack {
    public JavaStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public JavaStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        Function targetLambda = new Function(this, "targetFunction",
          FunctionProps.builder()
              .code(Code.fromInline("exports.handler = function(event, ctx, cb) { return cb(null, \"hi\"); })"))
              .functionName("estTargetFunction")
              .runtime(Runtime.NODEJS_18_X)
              .handler("index.handler")
              .build());
        String cronJobExample = "cron(50/1 4-5 ? * SUN-SAT *)";
        LambdaSubminute subminuteMaster = new LambdaSubminute(this, "LambdaSubminute", LambdaSubminuteProps.builder()
              .targetFunction(targetLambda)
              .cronjobExpression(cronJobExample)
              .frequency(6)
              .intervalTime(9)
              .build());

        new CfnOutput(this, "OStateMachineArn",
                CfnOutputProps.builder()
                  .value(subminuteMaster.getStateMachineArn())
                  .build());
        new CfnOutput(this, "OIteratorFunctionArn",
                CfnOutputProps.builder()
                  .value(subminuteMaster.getIteratorFunction().getFunctionName())
                  .build());
    }
}

```

## C#

You could also refer to [here](https://github.com/HsiehShuJeng/cdk-lambda-subminute/tree/main/src/demo/csharp).

```bash
$ cdk init --language csharp
$ dotnet add src/Csharp package Amazon.CDK.AWS.Lambda
$ dotnet add src/Csharp package Lambda.Subminute --version 2.0.442
```

```cs
using Amazon.CDK;
using Amazon.CDK.AWS.Lambda;
using ScottHsieh.Cdk;

namespace Csharp
{
    public class CsharpStack : Stack
    {
        internal CsharpStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            var targetLambda = new Function(this, "targetFunction", new FunctionProps
            {
                Code = Code.FromInline("exports.handler = function(event, ctx, cb) { return cb(null, \"hi\"); })"),
                FunctionName = "testTargetFunction",
                Runtime = Runtime.NODEJS_18_X,
                Handler = "index.handler"
            });
            string cronJobExample = "cron(50/1 6-7 ? * SUN-SAT *)";
            var subminuteMaster = new LambdaSubminute(this, "LambdaSubminute", new LambdaSubminuteProps
            {
                TargetFunction = targetLambda,
                CronjobExpression = cronJobExample,
                Frequency = 10,
                IntervalTime = 6,
            });

            new CfnOutput(this, "OStateMachineArn", new CfnOutputProps
            {
                Value = subminuteMaster.StateMachineArn
            });
            new CfnOutput(this, "OIteratorFunctionArn", new CfnOutputProps
            {
                Value = subminuteMaster.IteratorFunction.FunctionArn
            });
        }
    }
}
```

## GO

```bash
# Initialize a new AWS CDK application in the current directory with the Go programming language
cdk init app -l go
# Add this custom CDK construct to your project
go get github.com/HsiehShuJeng/cdk-lambda-subminute-go/cdklambdasubminute/v2@v2.0.442
# Ensure all dependencies are properly listed in the go.mod file and remove any unused ones
go mod tidy
# Upgrade all Go modules in your project to their latest minor or patch versions
go get -u ./...
```

# Statemachine Diagram

![image](https://raw.githubusercontent.com/HsiehShuJeng/cdk-lambda-subminute/main/images/statemachine_diagram.png)

# Known issue

Originally, I utilized `PythonFuncion` in the module of [**@aws-cdk/aws-lambda-python**](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-lambda-python-readme.html) to build the iterator Lambda function. Every thing works fine, including test, on my local machine (MacBook Pro M1), until it comes to the CI in Github Actions, it awlays gave me the following message:

```bash
## cdk version: 1.105.0 (build 4813992)
Bundling did not produce any output. Check that content is written to /asset-output.

      64 |     }));
      65 |
    > 66 |     this.function = new PythonFunction(this, 'Iterator', {
         |                     ^
      67 |       functionName: 'lambda-subminute-iterator',
      68 |       description: 'A function for breaking the limit of 1 minute with the CloudWatch Rules.',
      69 |       logRetention: RetentionDays.THREE_MONTHS,

      at AssetStaging.bundle (node_modules/@aws-cdk/core/lib/asset-staging.ts:484:13)
      at AssetStaging.stageByBundling (node_modules/@aws-cdk/core/lib/asset-staging.ts:328:10)
      at stageThisAsset (node_modules/@aws-cdk/core/lib/asset-staging.ts:194:35)
      at Cache.obtain (node_modules/@aws-cdk/core/lib/private/cache.ts:24:13)
      at new AssetStaging (node_modules/@aws-cdk/core/lib/asset-staging.ts:219:44)
      at new Asset (node_modules/@aws-cdk/aws-s3-assets/lib/asset.ts:127:21)
      at AssetCode.bind (node_modules/@aws-cdk/aws-lambda/lib/code.ts:277:20)
      at new Function (node_modules/@aws-cdk/aws-lambda/lib/function.ts:583:29)
      at new PythonFunction (node_modules/@aws-cdk/aws-lambda-python/lib/function.ts:106:5)
      at new IteratorLambda (src/cdk-lambda-subminute.ts:66:21)
      at new LambdaSubminute (src/cdk-lambda-subminute.ts:25:22)
      at Object.<anonymous>.test (test/integ.test.ts:23:3)
```

I actually have tried many different methods according to the following threads but to no avail.  I'll attempt to test some thoughts or just post the issue onto the CDK Github repo.

* [Asset Bundling](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-s3-assets-readme.html#asset-bundling)
* [Change the bundler's /asset-output local volume mount location #8589](https://github.com/aws/aws-cdk/issues/8589)
* [(aws-lambda-python: PythonFunction): unable to use bundling in BitBucket #14156](https://github.com/aws/aws-cdk/issues/14516)
* [BundlingDockerImage.cp() needs to be explained more in the README #11914](https://github.com/aws/aws-cdk/issues/11914)
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

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


class IteratorLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-subminute.IteratorLambda",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param target_function: The Lambda function that is going to be executed per time unit less than one minute.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332c82c86e22a486f820ef4ef39f374cca2596d6905db3d47d8f91b9c5b4529e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = IteratorLambdaProps(target_function=target_function)

        jsii.create(self.__class__, self, [scope, name, props])

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''A Lambda function that plays the role of the iterator.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, jsii.get(self, "function"))


@jsii.data_type(
    jsii_type="cdk-lambda-subminute.IteratorLambdaProps",
    jsii_struct_bases=[],
    name_mapping={"target_function": "targetFunction"},
)
class IteratorLambdaProps:
    def __init__(
        self,
        *,
        target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> None:
        '''
        :param target_function: The Lambda function that is going to be executed per time unit less than one minute.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6cbabba5a7f52c4ff270d0c0a385fe0ad8e94b3ebf8ba5102b7ce527cbb631)
            check_type(argname="argument target_function", value=target_function, expected_type=type_hints["target_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_function": target_function,
        }

    @builtins.property
    def target_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The Lambda function that is going to be executed per time unit less than one minute.'''
        result = self._values.get("target_function")
        assert result is not None, "Required property 'target_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IteratorLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LambdaSubminute(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-subminute.LambdaSubminute",
):
    def __init__(
        self,
        parent: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        cronjob_expression: typing.Optional[builtins.str] = None,
        frequency: typing.Optional[jsii.Number] = None,
        interval_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param parent: -
        :param name: -
        :param target_function: The Lambda function that is going to be executed per time unit less than one minute.
        :param cronjob_expression: A pattern you want this statemachine to be executed. Default: cron(50/1 15-17 ? * * *) UTC+0 being run every minute starting from 15:00 PM to 17:00 PM.
        :param frequency: How many times you intent to execute in a minute. Default: 6
        :param interval_time: Seconds for an interval, the product of ``frequency`` and ``intervalTime`` should be approximagely 1 minute. Default: 10
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8208a1a2e852a0d77c2ead71cc3a82d0585848ad98de6784ab607d4d3a3a1a9d)
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = LambdaSubminuteProps(
            target_function=target_function,
            cronjob_expression=cronjob_expression,
            frequency=frequency,
            interval_time=interval_time,
        )

        jsii.create(self.__class__, self, [parent, name, props])

    @builtins.property
    @jsii.member(jsii_name="iteratorFunction")
    def iterator_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The Lambda function that plays the role of the iterator.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, jsii.get(self, "iteratorFunction"))

    @builtins.property
    @jsii.member(jsii_name="stateMachineArn")
    def state_machine_arn(self) -> builtins.str:
        '''The ARN of the state machine that executes the target Lambda function per time unit less than one minute.'''
        return typing.cast(builtins.str, jsii.get(self, "stateMachineArn"))


@jsii.data_type(
    jsii_type="cdk-lambda-subminute.LambdaSubminuteProps",
    jsii_struct_bases=[],
    name_mapping={
        "target_function": "targetFunction",
        "cronjob_expression": "cronjobExpression",
        "frequency": "frequency",
        "interval_time": "intervalTime",
    },
)
class LambdaSubminuteProps:
    def __init__(
        self,
        *,
        target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        cronjob_expression: typing.Optional[builtins.str] = None,
        frequency: typing.Optional[jsii.Number] = None,
        interval_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param target_function: The Lambda function that is going to be executed per time unit less than one minute.
        :param cronjob_expression: A pattern you want this statemachine to be executed. Default: cron(50/1 15-17 ? * * *) UTC+0 being run every minute starting from 15:00 PM to 17:00 PM.
        :param frequency: How many times you intent to execute in a minute. Default: 6
        :param interval_time: Seconds for an interval, the product of ``frequency`` and ``intervalTime`` should be approximagely 1 minute. Default: 10
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0edf312d06dc3869b70bad198688ff0769b98ebba7d3a4ed51666480395031)
            check_type(argname="argument target_function", value=target_function, expected_type=type_hints["target_function"])
            check_type(argname="argument cronjob_expression", value=cronjob_expression, expected_type=type_hints["cronjob_expression"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument interval_time", value=interval_time, expected_type=type_hints["interval_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_function": target_function,
        }
        if cronjob_expression is not None:
            self._values["cronjob_expression"] = cronjob_expression
        if frequency is not None:
            self._values["frequency"] = frequency
        if interval_time is not None:
            self._values["interval_time"] = interval_time

    @builtins.property
    def target_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The Lambda function that is going to be executed per time unit less than one minute.'''
        result = self._values.get("target_function")
        assert result is not None, "Required property 'target_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def cronjob_expression(self) -> typing.Optional[builtins.str]:
        '''A pattern you want this statemachine to be executed.

        :default: cron(50/1 15-17 ? * * *) UTC+0 being run every minute starting from 15:00 PM to 17:00 PM.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
        '''
        result = self._values.get("cronjob_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def frequency(self) -> typing.Optional[jsii.Number]:
        '''How many times you intent to execute in a minute.

        :default: 6
        '''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def interval_time(self) -> typing.Optional[jsii.Number]:
        '''Seconds for an interval, the product of ``frequency`` and ``intervalTime`` should be approximagely 1 minute.

        :default: 10
        '''
        result = self._values.get("interval_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaSubminuteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SubminuteStateMachine(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-lambda-subminute.SubminuteStateMachine",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        frequency: jsii.Number,
        interval_time: jsii.Number,
        iterator_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        state_machine_name: builtins.str,
        target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param frequency: How many times you intent to execute in a minute. Default: 6
        :param interval_time: Seconds for an interval, the product of ``frequency`` and ``intervalTime`` should be approximagely 1 minute. Default: 10
        :param iterator_function: the iterator Lambda function for the target Lambda function.
        :param state_machine_name: the name of the state machine.
        :param target_function: the Lambda function that executes your intention.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203fae4d7ae7c206b29ffc6c66a96499b8642ddfc192ac94c8f87c91868f2de5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SubminuteStateMachineProps(
            frequency=frequency,
            interval_time=interval_time,
            iterator_function=iterator_function,
            state_machine_name=state_machine_name,
            target_function=target_function,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="stateMachine")
    def state_machine(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.StateMachine, jsii.get(self, "stateMachine"))


@jsii.data_type(
    jsii_type="cdk-lambda-subminute.SubminuteStateMachineProps",
    jsii_struct_bases=[],
    name_mapping={
        "frequency": "frequency",
        "interval_time": "intervalTime",
        "iterator_function": "iteratorFunction",
        "state_machine_name": "stateMachineName",
        "target_function": "targetFunction",
    },
)
class SubminuteStateMachineProps:
    def __init__(
        self,
        *,
        frequency: jsii.Number,
        interval_time: jsii.Number,
        iterator_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        state_machine_name: builtins.str,
        target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    ) -> None:
        '''
        :param frequency: How many times you intent to execute in a minute. Default: 6
        :param interval_time: Seconds for an interval, the product of ``frequency`` and ``intervalTime`` should be approximagely 1 minute. Default: 10
        :param iterator_function: the iterator Lambda function for the target Lambda function.
        :param state_machine_name: the name of the state machine.
        :param target_function: the Lambda function that executes your intention.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ac3489a5fe552f5228700b662184af6d7f8d3f41a3db4412c10f5f43329032)
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument interval_time", value=interval_time, expected_type=type_hints["interval_time"])
            check_type(argname="argument iterator_function", value=iterator_function, expected_type=type_hints["iterator_function"])
            check_type(argname="argument state_machine_name", value=state_machine_name, expected_type=type_hints["state_machine_name"])
            check_type(argname="argument target_function", value=target_function, expected_type=type_hints["target_function"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency": frequency,
            "interval_time": interval_time,
            "iterator_function": iterator_function,
            "state_machine_name": state_machine_name,
            "target_function": target_function,
        }

    @builtins.property
    def frequency(self) -> jsii.Number:
        '''How many times you intent to execute in a minute.

        :default: 6
        '''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def interval_time(self) -> jsii.Number:
        '''Seconds for an interval, the product of ``frequency`` and ``intervalTime`` should be approximagely 1 minute.

        :default: 10
        '''
        result = self._values.get("interval_time")
        assert result is not None, "Required property 'interval_time' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def iterator_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''the iterator Lambda function for the target Lambda function.'''
        result = self._values.get("iterator_function")
        assert result is not None, "Required property 'iterator_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def state_machine_name(self) -> builtins.str:
        '''the name of the state machine.'''
        result = self._values.get("state_machine_name")
        assert result is not None, "Required property 'state_machine_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''the Lambda function that executes your intention.'''
        result = self._values.get("target_function")
        assert result is not None, "Required property 'target_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubminuteStateMachineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IteratorLambda",
    "IteratorLambdaProps",
    "LambdaSubminute",
    "LambdaSubminuteProps",
    "SubminuteStateMachine",
    "SubminuteStateMachineProps",
]

publication.publish()

def _typecheckingstub__332c82c86e22a486f820ef4ef39f374cca2596d6905db3d47d8f91b9c5b4529e(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6cbabba5a7f52c4ff270d0c0a385fe0ad8e94b3ebf8ba5102b7ce527cbb631(
    *,
    target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8208a1a2e852a0d77c2ead71cc3a82d0585848ad98de6784ab607d4d3a3a1a9d(
    parent: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    cronjob_expression: typing.Optional[builtins.str] = None,
    frequency: typing.Optional[jsii.Number] = None,
    interval_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0edf312d06dc3869b70bad198688ff0769b98ebba7d3a4ed51666480395031(
    *,
    target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    cronjob_expression: typing.Optional[builtins.str] = None,
    frequency: typing.Optional[jsii.Number] = None,
    interval_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203fae4d7ae7c206b29ffc6c66a96499b8642ddfc192ac94c8f87c91868f2de5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    frequency: jsii.Number,
    interval_time: jsii.Number,
    iterator_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    state_machine_name: builtins.str,
    target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ac3489a5fe552f5228700b662184af6d7f8d3f41a3db4412c10f5f43329032(
    *,
    frequency: jsii.Number,
    interval_time: jsii.Number,
    iterator_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    state_machine_name: builtins.str,
    target_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass
