r'''
# cdk-databrew-cicd

This construct creates a **CodePipeline** pipeline where users can push a **DataBrew** recipe into the **CodeCommit** repository and the recipe will be pushed to a pre-production AWS account and a production AWS account by order automatically.

| npm (JS/TS) | PyPI (Python) | Maven (Java) | Go | NuGet |
| --- | --- | --- | --- | --- |
| [Link](https://www.npmjs.com/package/cdk-databrew-cicd) | [Link](https://pypi.org/project/cdk_databrew_cicd/) | [Link](https://search.maven.org/artifact/io.github.hsiehshujeng/cdk-databrew-cicd) | [Link](https://github.com/HsiehShuJeng/cdk-databrew-cicd-go) | [Link](https://www.nuget.org/packages/Databrew.Cicd/) |

[![License](https://img.shields.io/badge/License-Apache%202.0-green)](https://opensource.org/licenses/Apache-2.0) [![Release](https://github.com/HsiehShuJeng/cdk-databrew-cicd/workflows/Release/badge.svg)](https://github.com/HsiehShuJeng/cdk-databrew-cicd/actions/workflows/release.yml) [![npm downloads](https://img.shields.io/npm/dt/cdk-databrew-cicd?label=npm%20downloads&style=plastic)](https://img.shields.io/npm/dt/cdk-databrew-cicd?label=npm%20downloads&style=plastic) [![pypi downloads](https://img.shields.io/pypi/dm/cdk-databrew-cicd?label=pypi%20downloads&style=plastic)](https://img.shields.io/pypi/dm/cdk-databrew-cicd?label=pypi%20downloads&style=plastic) [![NuGet downloads](https://img.shields.io/nuget/dt/Databrew.Cicd?label=NuGet%20downloads&style=plastic)](https://img.shields.io/nuget/dt/Databrew.Cicd?label=NuGet%20downloads&style=plastic) [![repo languages](https://img.shields.io/github/languages/count/HsiehShuJeng/cdk-databrew-cicd?label=repo%20languages&style=plastic)](https://img.shields.io/github/languages/count/HsiehShuJeng/cdk-databrew-cicd?label=repo%20languages&style=plastic)

# Table of Contents

* [Serverless Architecture](#serverless-architecture)
* [Introduction](#introduction)
* [Example](#example)

  * [Typescript](#typescript)
  * [Python](#python)
  * [Java](#java)
  * [C#](#c)
  * [Go](#go)
* [Some Efforts after Stack Creation](#some-efforts-after-stack-creation)
* [How Successful Commits Look Like](#how-successful-commits-look-like)

# Serverless Architecture

![image](https://d2908q01vomqb2.cloudfront.net/b6692ea5df920cad691c20319a6fffd7a4a766b8/2021/05/19/image001.jpg) *Romi B. and Gaurav W., 2021*

# Introduction

The architecture was introduced by **Romi Boimer** and **Gaurav Wadhawan** and was posted on the AWS Blog as [*Set up CI/CD pipelines for AWS Glue DataBrew using AWS Developer Tools*](https://aws.amazon.com/tw/blogs/big-data/set-up-ci-cd-pipelines-for-aws-glue-databrew-using-aws-developer-tools/).
I converted the architecture into a CDK construct for 5 programming languages. Before applying the AWS construct, make sure you've set up a proper IAM role for the pre-production and production AWS accounts. You could achieve it either by creating manually or creating through a custom construct in this library.

```python
import { IamRole } from 'cdk-databrew-cicd';

new IamRole(this, 'AccountIamRole', {
    environment: 'preproduction', // or 'production'
    accountID: 'ACCOUNT_ID',
    // roleName: 'OPTIONAL'
});
```

# Example

## Typescript

You could also refer to [here](https://github.com/HsiehShuJeng/cdk-databrew-cicd/tree/main/src/demo/typescript).

```bash
$ cdk --init language typescript
$ yarn add cdk-databrew-cicd
```

```python
import * as cdk from '@aws-cdk/core';
import { DataBrewCodePipeline } from 'cdk-databrew-cicd';

class TypescriptStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const preproductionAccountId = 'PREPRODUCTION_ACCOUNT_ID';
    const productionAccountId = 'PRODUCTION_ACCOUNT_ID';

    const dataBrewPipeline = new DataBrewCodePipeline(this, 'DataBrewCicdPipeline', {
      preproductionIamRoleArn: `arn:${cdk.Aws.PARTITION}:iam::${preproductionAccountId}:role/preproduction-Databrew-Cicd-Role`,
      productionIamRoleArn: `arn:${cdk.Aws.PARTITION}:iam::${productionAccountId}:role/production-Databrew-Cicd-Role`,
      // bucketName: 'OPTIONAL',
      // repoName: 'OPTIONAL',
      // branchName: 'OPTIONAL',
      // pipelineName: 'OPTIONAL'
    });

    new cdk.CfnOutput(this, 'OPreproductionLambdaArn', { value: dataBrewPipeline.preproductionFunctionArn });
    new cdk.CfnOutput(this, 'OProductionLambdaArn', { value: dataBrewPipeline.productionFunctionArn });
    new cdk.CfnOutput(this, 'OCodeCommitRepoArn', { value: dataBrewPipeline.codeCommitRepoArn });
    new cdk.CfnOutput(this, 'OCodePipelineArn', { value: dataBrewPipeline.codePipelineArn });
  }
}

const app = new cdk.App();
new TypescriptStack(app, 'TypescriptStack', {
  stackName: 'DataBrew-CICD'
});
```

## Python

You could also refer to [here](https://github.com/HsiehShuJeng/cdk-databrew-cicd/tree/main/src/demo/python).

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
cdk-databrew-cicd
EOL
$ python -m pip install -r requirements.txt
```

```python
from aws_cdk import core as cdk
from cdk_databrew_cicd import DataBrewCodePipeline

class PythonStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        preproduction_account_id = "PREPRODUCTION_ACCOUNT_ID"
        production_account_id = "PRODUCTION_ACCOUNT_ID"

        databrew_pipeline = DataBrewCodePipeline(self,
        "DataBrewCicdPipeline",
        preproduction_iam_role_arn=f"arn:{cdk.Aws.PARTITION}:iam::{preproduction_account_id}:role/preproduction-Databrew-Cicd-Role",
        production_iam_role_arn=f"arn:{cdk.Aws.PARTITION}:iam::{production_account_id}:role/preproduction-Databrew-Cicd-Role",
            # bucket_name="OPTIONAL",
            # repo_name="OPTIONAL",
            # repo_name="OPTIONAL",
            # branch_namne="OPTIONAL",
            # pipeline_name="OPTIONAL"
            )

        cdk.CfnOutput(self, 'OPreproductionLambdaArn', value=databrew_pipeline.preproduction_function_arn)
        cdk.CfnOutput(self, 'OProductionLambdaArn', value=databrew_pipeline.production_function_arn)
        cdk.CfnOutput(self, 'OCodeCommitRepoArn', value=databrew_pipeline.code_commit_repo_arn)
        cdk.CfnOutput(self, 'OCodePipelineArn', value=databrew_pipeline.code_pipeline_arn)
```

```bash
$ deactivate
```

## Java

You could also refer to [here](https://github.com/HsiehShuJeng/cdk-databrew-cicd/tree/main/src/demo/java).

```bash
$ cdk init --language java
$ mvn package
```

```xml
.
.
<properties>
      <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
      <cdk.version>2.87.0</cdk.version>
      <constrcut.verion>2.0.196</constrcut.verion>
      <junit.version>5.7.1</junit.version>
</properties>
 .
 .
 <dependencies>
     <!-- AWS Cloud Development Kit -->
      <dependency>
            <groupId>software.amazon.awscdk</groupId>
            <artifactId>aws-cdk-lib</artifactId>
            <version>${cdk.version}</version>
      </dependency>
      <dependency>
        <groupId>io.github.hsiehshujeng</groupId>
        <artifactId>cdk-databrew-cicd</artifactId>
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
import io.github.hsiehshujeng.cdk.databrew.cicd.DataBrewCodePipeline;
import io.github.hsiehshujeng.cdk.databrew.cicd.DataBrewCodePipelineProps;

public class JavaStack extends Stack {
    public JavaStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public JavaStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);
        String preproductionAccountId = "PREPRODUCTION_ACCOUNT_ID";
        String productionAccountId = "PRODUCTION_ACCOUNT_ID";
        DataBrewCodePipeline databrewPipeline = new DataBrewCodePipeline(this, "DataBrewCicdPipeline",
                DataBrewCodePipelineProps.builder().preproductionIamRoleArn(preproductionAccountId)
                        .productionIamRoleArn(productionAccountId)
                        // .bucketName("OPTIONAL")
                        // .branchName("OPTIONAL")
                        // .pipelineName("OPTIONAL")
                        .build());

        new CfnOutput(this, "OPreproductionLambdaArn",
                CfnOutputProps.builder()
                    .value(databrewPipeline.getPreproductionFunctionArn())
                    .build());
        new CfnOutput(this, "OProductionLambdaArn",
                CfnOutputProps.builder()
                    .value(databrewPipeline.getProductionFunctionArn())
                    .build());
        new CfnOutput(this, "OCodeCommitRepoArn",
                CfnOutputProps.builder()
                    .value(databrewPipeline.getCodeCommitRepoArn())
                    .build());
        new CfnOutput(this, "OCodePipelineArn",
                CfnOutputProps.builder()
                    .value(databrewPipeline.getCodePipelineArn())
                    .build());
    }
}
```

## C#

You could also refer to [here](https://github.com/HsiehShuJeng/cdk-databrew-cicd/tree/main/src/demo/csharp).

```bash
$ cdk init --language csharp
$ dotnet add src/Csharp package Databrew.Cicd --version 2.0.196
```

```cs
using Amazon.CDK;
using ScottHsieh.Cdk;

namespace Csharp
{
    public class CsharpStack : Stack
    {
        internal CsharpStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            var preproductionAccountId = "PREPRODUCTION_ACCOUNT_ID";
            var productionAccountId = "PRODUCTION_ACCOUNT_ID";

            var dataBrewPipeline = new DataBrewCodePipeline(this, "DataBrewCicdPipeline", new DataBrewCodePipelineProps
            {
                PreproductionIamRoleArn = $"arn:{Aws.PARTITION}:iam::{preproductionAccountId}:role/preproduction-Databrew-Cicd-Role",
                ProductionIamRoleArn = $"arn:{Aws.PARTITION}:iam::{productionAccountId}:role/preproduction-Databrew-Cicd-Role",
                // BucketName = "OPTIONAL",
                // RepoName = "OPTIONAL",
                // BranchName = "OPTIONAL",
                // PipelineName = "OPTIONAL"
            });
            new CfnOutput(this, "OPreproductionLambdaArn", new CfnOutputProps
            {
                Value = dataBrewPipeline.PreproductionFunctionArn
            });
            new CfnOutput(this, "OProductionLambdaArn", new CfnOutputProps
            {
                Value = dataBrewPipeline.ProductionFunctionArn
            });
            new CfnOutput(this, "OCodeCommitRepoArn", new CfnOutputProps
            {
                Value = dataBrewPipeline.CodeCommitRepoArn
            });
            new CfnOutput(this, "OCodePipelineArn", new CfnOutputProps
            {
                Value = dataBrewPipeline.CodeCommitRepoArn
            });
        }
    }
}
```

## Go

You could also refer to [here](src/demo/go_lang/).

```bash
# Initialize a new AWS CDK application in the current directory with the Go programming language
cdk init app -l go
# Add this custom CDK construct to your project
go get github.com/HsiehShuJeng/cdk-databrew-cicd-go/cdkdatabrewcicd/v2@v2.0.196
# Ensure all dependencies are properly listed in the go.mod file and remove any unused ones
go mod tidy
# Upgrade all Go modules in your project to their latest minor or patch versions
go get -u ./...
```

```go
package main

import (
	"fmt"

	"github.com/aws/aws-cdk-go/awscdk/v2"

	// "github.com/aws/aws-cdk-go/awscdk/v2/awssqs"
	"github.com/HsiehShuJeng/cdk-databrew-cicd-go/cdkdatabrewcicd/v2"
	"github.com/aws/constructs-go/constructs/v10"
	"github.com/aws/jsii-runtime-go"
)

type GoLangStackProps struct {
	awscdk.StackProps
}

func NewGoLangStack(scope constructs.Construct, id string, props *GoLangStackProps) awscdk.Stack {
	var sprops awscdk.StackProps
	if props != nil {
		sprops = props.StackProps
	}
	stack := awscdk.NewStack(scope, &id, &sprops)

	preproductionAccountId := "PREPRODUCTION_ACCOUNT_ID"
	productionAccountId := "PRODUCTION_ACCOUNT_ID"

	dataBrewPipeline := cdkdatabrewcicd.NewDataBrewCodePipeline(stack, jsii.String("DataBrewCicdPipeline"), &cdkdatabrewcicd.DataBrewCodePipelineProps{
		PreproductionIamRoleArn: jsii.String(fmt.Sprintf("arn:%s:iam::%s:role/preproduction-Databrew-Cicd-Role", *awscdk.Aws_PARTITION(), preproductionAccountId)),
		ProductionIamRoleArn:    jsii.String(fmt.Sprintf("arn:%s:iam::%s:role/production-Databrew-Cicd-Role", *awscdk.Aws_PARTITION(), productionAccountId)),
		// BucketName:   jsii.String("OPTIONAL"),
		// RepoName:     jsii.String("OPTIONAL"),
		// BranchName:   jsii.String("OPTIONAL"),
		// PipelineName: jsii.String("OPTIONAL"),
	})

	awscdk.NewCfnOutput(stack, jsii.String("OPreproductionLambdaArn"), &awscdk.CfnOutputProps{Value: dataBrewPipeline.PreproductionFunctionArn()})
	awscdk.NewCfnOutput(stack, jsii.String("OProductionLambdaArn"), &awscdk.CfnOutputProps{Value: dataBrewPipeline.ProductionFunctionArn()})
	awscdk.NewCfnOutput(stack, jsii.String("OCodeCommitRepoArn"), &awscdk.CfnOutputProps{Value: dataBrewPipeline.CodeCommitRepoArn()})
	awscdk.NewCfnOutput(stack, jsii.String("OCodePipelineArn"), &awscdk.CfnOutputProps{Value: dataBrewPipeline.CodePipelineArn()})

	return stack
}

func main() {
	defer jsii.Close()

	app := awscdk.NewApp(nil)

	NewGoLangStack(app, "GoLangStack", &GoLangStackProps{
		awscdk.StackProps{
			Env: env(),
		},
	})

	app.Synth(nil)
}

func env() *awscdk.Environment {
	return nil
}

```

# Some Efforts after Stack Creation

## CodeCommit

1. Create HTTPS Git credentials for AWS CodeCommit with an IAM user that you're going to use.
   ![image](https://raw.githubusercontent.com/HsiehShuJeng/cdk-databrew-cicd/main/images/codecommit_credentials.png)
2. Run through the steps noted on the README.md of the CodeCommit repository after finishing establishing the stack via CDK. The returned message with success should be looked like the following (assume you have installed [`git-remote-codecommit`](https://pypi.org/project/git-remote-codecommit/)):

   ```bash
   $ git clone codecommit://scott.codecommit@DataBrew-Recipes-Repo
   Cloning into 'DataBrew-Recipes-Repo'...
   remote: Counting objects: 6, done.
   Unpacking objects: 100% (6/6), 2.03 KiB | 138.00 KiB/s, done.
   ```
3. Add a DataBrew recipe into the local repositroy (directory) and commit the change. (either directly on the main branch or merging another branch into the main branch)

## Glue DataBrew

1. Download any recipe either generated out by following [*Getting started with AWS Glue DataBrew*](https://docs.aws.amazon.com/zh_tw/databrew/latest/dg/getting-started.html) or made by yourself as **JSON file**.
   ![image](https://raw.githubusercontent.com/HsiehShuJeng/cdk-databrew-cicd/main/images/databrew_recipes.png)
2. Move the recipe from the download directory to the local directory for the CodeCommit repository.

   ```bash
   $ mv ${DOWNLOAD_DIRECTORY}/chess-project-recipe.json ${CODECOMMIT_LOCAL_DIRECTORY}/
   ```
3. Commit the change to a branch with a name you prefer.

   ```bash
   $ cd ${{CODECOMMIT_LOCAL_DIRECTORY}}
   $ git checkout -b add-recipe main
   $ git add .
   $ git commit -m "first recipe"
   $ git push --set-upstream origin add-recipe
   ```
4. Merge the branch into the main branch. Just go to the **AWS CodeCommit** web console to do the merge as its process is purely the same as you've already done thousands of times on **Github** but only with different UIs.

# How Successful Commits Look Like

1. In the infrastructure account, the status of the CodePipeline DataBrew pipeline should be similar as the following:
   ![image](https://raw.githubusercontent.com/HsiehShuJeng/cdk-databrew-cicd/main/images/infra_codepipeline.png)
2. In the **pre-production** account with the same region as where the CICD pipeline is deployed at the infrastructue account, you'll see this.
   ![image](https://raw.githubusercontent.com/HsiehShuJeng/cdk-databrew-cicd/main/images/preproduction-recipe.png)
3. In the **production** account with the same region as where the CICD pipeline is deployed at the infrastructue account, you'll see this.
   ![image](https://raw.githubusercontent.com/HsiehShuJeng/cdk-databrew-cicd/main/images/production-recipe.png)
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

import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import constructs as _constructs_77d1e7e8


class CodePipelineIamRole(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-databrew-cicd.CodePipelineIamRole",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        bucket_arn: builtins.str,
        preproduction_lambda_arn: builtins.str,
        production_lambda_arn: builtins.str,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param bucket_arn: The ARN of the S3 bucket where you store your artifacts.
        :param preproduction_lambda_arn: The ARN of the Lambda function for the pre-production account.
        :param production_lambda_arn: The ARN of the Lambda function for the production account.
        :param role_name: The role name for the CodePipeline CICD pipeline. Default: 'DataBrew-Recipe-Pipeline-Role'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4b3cedca9c3d8560bb9b34d56b1758c3a3ba17f69dcb6e4844d1cd8257728f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = CodePipelineIamRoleProps(
            bucket_arn=bucket_arn,
            preproduction_lambda_arn=preproduction_lambda_arn,
            production_lambda_arn=production_lambda_arn,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.Role:
        '''The representative of the IAM role for the CodePipeline CICD pipeline.'''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Role, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role for the CodePipeline CICD pipeline.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))


@jsii.data_type(
    jsii_type="cdk-databrew-cicd.CodePipelineIamRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "preproduction_lambda_arn": "preproductionLambdaArn",
        "production_lambda_arn": "productionLambdaArn",
        "role_name": "roleName",
    },
)
class CodePipelineIamRoleProps:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        preproduction_lambda_arn: builtins.str,
        production_lambda_arn: builtins.str,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: The ARN of the S3 bucket where you store your artifacts.
        :param preproduction_lambda_arn: The ARN of the Lambda function for the pre-production account.
        :param production_lambda_arn: The ARN of the Lambda function for the production account.
        :param role_name: The role name for the CodePipeline CICD pipeline. Default: 'DataBrew-Recipe-Pipeline-Role'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c88298ceb251680594e19748f268c88132a53d9230ce141ab38c138f8bc599)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument preproduction_lambda_arn", value=preproduction_lambda_arn, expected_type=type_hints["preproduction_lambda_arn"])
            check_type(argname="argument production_lambda_arn", value=production_lambda_arn, expected_type=type_hints["production_lambda_arn"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "preproduction_lambda_arn": preproduction_lambda_arn,
            "production_lambda_arn": production_lambda_arn,
        }
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''The ARN of the S3 bucket where you store your artifacts.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preproduction_lambda_arn(self) -> builtins.str:
        '''The ARN of the Lambda function for the pre-production account.'''
        result = self._values.get("preproduction_lambda_arn")
        assert result is not None, "Required property 'preproduction_lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def production_lambda_arn(self) -> builtins.str:
        '''The ARN of the Lambda function for the production account.'''
        result = self._values.get("production_lambda_arn")
        assert result is not None, "Required property 'production_lambda_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''The role name for the CodePipeline CICD pipeline.

        :default: 'DataBrew-Recipe-Pipeline-Role'
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodePipelineIamRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataBrewCodePipeline(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-databrew-cicd.DataBrewCodePipeline",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        preproduction_iam_role_arn: builtins.str,
        production_iam_role_arn: builtins.str,
        branch_name: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        first_stage_artifact_name: typing.Optional[builtins.str] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        repo_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param preproduction_iam_role_arn: The ARN of the IAM role in the pre-production account.
        :param production_iam_role_arn: The ARN of the IAM role in the production account.
        :param branch_name: The name of the branch that will trigger the DataBrew CICD pipeline. Default: 'main'
        :param bucket_name: The name of the S3 bucket for the CodePipeline DataBrew CICD pipeline. Default: 'databrew-cicd-codepipelineartifactstorebucket'
        :param first_stage_artifact_name: the (required) name of the Artifact at the first stage. Default: 'SourceOutput'
        :param pipeline_name: The name of the CodePipeline Databrew CICD pipeline. Default: 'DataBrew-Recipe-Application'
        :param repo_name: The name of the CodeCommit repositroy for the DataBrew CICD pipeline. Default: 'DataBrew-Recipes-Repo'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8c42e0835720c39be9e5881e6e6fcdf267e0208a259aeb42f0ad40b070d536)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = DataBrewCodePipelineProps(
            preproduction_iam_role_arn=preproduction_iam_role_arn,
            production_iam_role_arn=production_iam_role_arn,
            branch_name=branch_name,
            bucket_name=bucket_name,
            first_stage_artifact_name=first_stage_artifact_name,
            pipeline_name=pipeline_name,
            repo_name=repo_name,
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''The name of the branch that will trigger the DataBrew CICD pipeline.'''
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

    @builtins.property
    @jsii.member(jsii_name="bucketArn")
    def bucket_arn(self) -> builtins.str:
        '''The ARN of the S3 bucket for the CodePipeline DataBrew CICD pipeline.'''
        return typing.cast(builtins.str, jsii.get(self, "bucketArn"))

    @builtins.property
    @jsii.member(jsii_name="codeCommitRepoArn")
    def code_commit_repo_arn(self) -> builtins.str:
        '''The ARN of the CodeCommit repository.'''
        return typing.cast(builtins.str, jsii.get(self, "codeCommitRepoArn"))

    @builtins.property
    @jsii.member(jsii_name="codePipelineArn")
    def code_pipeline_arn(self) -> builtins.str:
        '''The ARN of the DataBrew CICD pipeline.'''
        return typing.cast(builtins.str, jsii.get(self, "codePipelineArn"))

    @builtins.property
    @jsii.member(jsii_name="firstStageArtifactName")
    def first_stage_artifact_name(self) -> builtins.str:
        '''the (required) name of the Artifact at the first stage.'''
        return typing.cast(builtins.str, jsii.get(self, "firstStageArtifactName"))

    @builtins.property
    @jsii.member(jsii_name="preproductionFunctionArn")
    def preproduction_function_arn(self) -> builtins.str:
        '''The ARN of the Lambda function for the pre-production account.'''
        return typing.cast(builtins.str, jsii.get(self, "preproductionFunctionArn"))

    @builtins.property
    @jsii.member(jsii_name="productionFunctionArn")
    def production_function_arn(self) -> builtins.str:
        '''The ARN of the Lambda function for the production account.'''
        return typing.cast(builtins.str, jsii.get(self, "productionFunctionArn"))

    @builtins.property
    @jsii.member(jsii_name="repoName")
    def repo_name(self) -> builtins.str:
        '''The name of the CodeCommit repositroy for the DataBrew CICD pipeline.'''
        return typing.cast(builtins.str, jsii.get(self, "repoName"))


@jsii.data_type(
    jsii_type="cdk-databrew-cicd.DataBrewCodePipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "preproduction_iam_role_arn": "preproductionIamRoleArn",
        "production_iam_role_arn": "productionIamRoleArn",
        "branch_name": "branchName",
        "bucket_name": "bucketName",
        "first_stage_artifact_name": "firstStageArtifactName",
        "pipeline_name": "pipelineName",
        "repo_name": "repoName",
    },
)
class DataBrewCodePipelineProps:
    def __init__(
        self,
        *,
        preproduction_iam_role_arn: builtins.str,
        production_iam_role_arn: builtins.str,
        branch_name: typing.Optional[builtins.str] = None,
        bucket_name: typing.Optional[builtins.str] = None,
        first_stage_artifact_name: typing.Optional[builtins.str] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        repo_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param preproduction_iam_role_arn: The ARN of the IAM role in the pre-production account.
        :param production_iam_role_arn: The ARN of the IAM role in the production account.
        :param branch_name: The name of the branch that will trigger the DataBrew CICD pipeline. Default: 'main'
        :param bucket_name: The name of the S3 bucket for the CodePipeline DataBrew CICD pipeline. Default: 'databrew-cicd-codepipelineartifactstorebucket'
        :param first_stage_artifact_name: the (required) name of the Artifact at the first stage. Default: 'SourceOutput'
        :param pipeline_name: The name of the CodePipeline Databrew CICD pipeline. Default: 'DataBrew-Recipe-Application'
        :param repo_name: The name of the CodeCommit repositroy for the DataBrew CICD pipeline. Default: 'DataBrew-Recipes-Repo'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92658886e139cd36492ca37aa02eb2e4ea2d74477ca0c1670c351079f1ff7b4e)
            check_type(argname="argument preproduction_iam_role_arn", value=preproduction_iam_role_arn, expected_type=type_hints["preproduction_iam_role_arn"])
            check_type(argname="argument production_iam_role_arn", value=production_iam_role_arn, expected_type=type_hints["production_iam_role_arn"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument first_stage_artifact_name", value=first_stage_artifact_name, expected_type=type_hints["first_stage_artifact_name"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "preproduction_iam_role_arn": preproduction_iam_role_arn,
            "production_iam_role_arn": production_iam_role_arn,
        }
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if bucket_name is not None:
            self._values["bucket_name"] = bucket_name
        if first_stage_artifact_name is not None:
            self._values["first_stage_artifact_name"] = first_stage_artifact_name
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if repo_name is not None:
            self._values["repo_name"] = repo_name

    @builtins.property
    def preproduction_iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role in the pre-production account.'''
        result = self._values.get("preproduction_iam_role_arn")
        assert result is not None, "Required property 'preproduction_iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def production_iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role in the production account.'''
        result = self._values.get("production_iam_role_arn")
        assert result is not None, "Required property 'production_iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''The name of the branch that will trigger the DataBrew CICD pipeline.

        :default: 'main'
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_name(self) -> typing.Optional[builtins.str]:
        '''The name of the S3 bucket for the CodePipeline DataBrew CICD pipeline.

        :default: 'databrew-cicd-codepipelineartifactstorebucket'
        '''
        result = self._values.get("bucket_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def first_stage_artifact_name(self) -> typing.Optional[builtins.str]:
        '''the (required) name of the Artifact at the first stage.

        :default: 'SourceOutput'
        '''
        result = self._values.get("first_stage_artifact_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        '''The name of the CodePipeline Databrew CICD pipeline.

        :default: 'DataBrew-Recipe-Application'
        '''
        result = self._values.get("pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repo_name(self) -> typing.Optional[builtins.str]:
        '''The name of the CodeCommit repositroy for the DataBrew CICD pipeline.

        :default: 'DataBrew-Recipes-Repo'
        '''
        result = self._values.get("repo_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataBrewCodePipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirstCommitHandler(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-databrew-cicd.FirstCommitHandler",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        branch_name: builtins.str,
        code_commit_repo_arn: builtins.str,
        repo_name: builtins.str,
        function_name: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param branch_name: The branch name used in the CodeCommit repo.
        :param code_commit_repo_arn: The ARN of the CodeCommit repository.
        :param repo_name: The name of the CodeCommit repo.
        :param function_name: The name of the Lambda function which deals with first commit via AWS CodeCommit. Default: 'FirstCommitHandler'
        :param role_name: The name of the IAM role for the Lambda function which deals with first commit via AWS CodeCommit. Default: 'LambdaForInitialCommitRole'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c94ebf5d0f0646f9bd465f2e48aac6716fbdebb72bc0b4d3dbabf7f7d1661b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = FirstCommitHandlerProps(
            branch_name=branch_name,
            code_commit_repo_arn=code_commit_repo_arn,
            repo_name=repo_name,
            function_name=function_name,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The representative of Lambda function which deals with first commit via AWS CodeCommit.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, jsii.get(self, "function"))

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        '''The name of the Lambda function which deals with first commit via AWS CodeCommit.'''
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''The name of the IAM role for the Lambda function which deals with first commit via AWS CodeCommit.'''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))


@jsii.data_type(
    jsii_type="cdk-databrew-cicd.FirstCommitHandlerProps",
    jsii_struct_bases=[],
    name_mapping={
        "branch_name": "branchName",
        "code_commit_repo_arn": "codeCommitRepoArn",
        "repo_name": "repoName",
        "function_name": "functionName",
        "role_name": "roleName",
    },
)
class FirstCommitHandlerProps:
    def __init__(
        self,
        *,
        branch_name: builtins.str,
        code_commit_repo_arn: builtins.str,
        repo_name: builtins.str,
        function_name: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param branch_name: The branch name used in the CodeCommit repo.
        :param code_commit_repo_arn: The ARN of the CodeCommit repository.
        :param repo_name: The name of the CodeCommit repo.
        :param function_name: The name of the Lambda function which deals with first commit via AWS CodeCommit. Default: 'FirstCommitHandler'
        :param role_name: The name of the IAM role for the Lambda function which deals with first commit via AWS CodeCommit. Default: 'LambdaForInitialCommitRole'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c58e09bbf56172e632a96611953e1ffee8fa846c0c4cb85b70ab890e8bdc43c)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument code_commit_repo_arn", value=code_commit_repo_arn, expected_type=type_hints["code_commit_repo_arn"])
            check_type(argname="argument repo_name", value=repo_name, expected_type=type_hints["repo_name"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch_name": branch_name,
            "code_commit_repo_arn": code_commit_repo_arn,
            "repo_name": repo_name,
        }
        if function_name is not None:
            self._values["function_name"] = function_name
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''The branch name used in the CodeCommit repo.'''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code_commit_repo_arn(self) -> builtins.str:
        '''The ARN of the CodeCommit repository.'''
        result = self._values.get("code_commit_repo_arn")
        assert result is not None, "Required property 'code_commit_repo_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repo_name(self) -> builtins.str:
        '''The name of the CodeCommit repo.'''
        result = self._values.get("repo_name")
        assert result is not None, "Required property 'repo_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Lambda function which deals with first commit via AWS CodeCommit.

        :default: 'FirstCommitHandler'
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role for the Lambda function which deals with first commit via AWS CodeCommit.

        :default: 'LambdaForInitialCommitRole'
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirstCommitHandlerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IamRole(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-databrew-cicd.IamRole",
):
    '''IAM Role.

    Defines an IAM role for pre-production and production AWS accounts.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        account_id: builtins.str,
        environment: builtins.str,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param account_id: The ID of your infrastructure account.
        :param environment: 'preproduction' or 'production'.
        :param role_name: The role name. Default: '{environment}-Databrew-Cicd-Role'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72cb2011349b8a9e66b3c943c3b2ef730a2065d923d556221587d2ad288d77b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = IamRoleProps(
            account_id=account_id, environment=environment, role_name=role_name
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role for pre-production or production.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))


@jsii.data_type(
    jsii_type="cdk-databrew-cicd.IamRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "account_id": "accountID",
        "environment": "environment",
        "role_name": "roleName",
    },
)
class IamRoleProps:
    def __init__(
        self,
        *,
        account_id: builtins.str,
        environment: builtins.str,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account_id: The ID of your infrastructure account.
        :param environment: 'preproduction' or 'production'.
        :param role_name: The role name. Default: '{environment}-Databrew-Cicd-Role'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f03732f915db1d749b6f9404cba16b860ffd31d3f75fd61d697b03a91bc76da4)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "environment": environment,
        }
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def account_id(self) -> builtins.str:
        '''The ID of your infrastructure account.'''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment(self) -> builtins.str:
        ''''preproduction' or 'production'.'''
        result = self._values.get("environment")
        assert result is not None, "Required property 'environment' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''The role name.

        :default: '{environment}-Databrew-Cicd-Role'
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IamRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InfraIamRole(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-databrew-cicd.InfraIamRole",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param role_name: The role name for the infrastructure account. Default: 'CrossAccountRepositoryContributorRole'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b75a148dbd27b9ab3c80a4aa84232b84c5e563450dc4475796ba74b2bb8c448d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = InfraIamRoleProps(role_name=role_name)

        jsii.create(self.__class__, self, [scope, name, props])

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The ARN of the IAM role for the infrastructure account.'''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))


@jsii.data_type(
    jsii_type="cdk-databrew-cicd.InfraIamRoleProps",
    jsii_struct_bases=[],
    name_mapping={"role_name": "roleName"},
)
class InfraIamRoleProps:
    def __init__(self, *, role_name: typing.Optional[builtins.str] = None) -> None:
        '''
        :param role_name: The role name for the infrastructure account. Default: 'CrossAccountRepositoryContributorRole'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5745e821cbdcdd9e6286b013c8579bd6278273ee512ce50d00572c0d09a8c240)
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''The role name for the infrastructure account.

        :default: 'CrossAccountRepositoryContributorRole'
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfraIamRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PreProductionLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-databrew-cicd.PreProductionLambda",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        bucket_arn: builtins.str,
        preproduction_iam_role_arn: builtins.str,
        function_name: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param bucket_arn: The ARN of the S3 bucket for the DataBrew CICD pipeline.
        :param preproduction_iam_role_arn: The ARN of the IAM role in the pre-production account.
        :param function_name: The Lambda funciton name for the pre-production account. Default: 'PreProd-DataBrew-Recipe-Deployer'
        :param role_name: The name of the IAM role for the pre-produciton Lambda function. Default: 'PreProd-DataBrew-Recipe-Deployer-role'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8efe3608b5814e558117f24f9265534319eaf3e415df05794ab820a21200a7b3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = PreProductionLambdaProps(
            bucket_arn=bucket_arn,
            preproduction_iam_role_arn=preproduction_iam_role_arn,
            function_name=function_name,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The representative of Lambda function for the pre-production account.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, jsii.get(self, "function"))

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        '''The Lambda funciton name for the pre-production account.'''
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''The name of the IAM role for the pre-produciton Lambda function.'''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))


@jsii.data_type(
    jsii_type="cdk-databrew-cicd.PreProductionLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "preproduction_iam_role_arn": "preproductionIamRoleArn",
        "function_name": "functionName",
        "role_name": "roleName",
    },
)
class PreProductionLambdaProps:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        preproduction_iam_role_arn: builtins.str,
        function_name: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: The ARN of the S3 bucket for the DataBrew CICD pipeline.
        :param preproduction_iam_role_arn: The ARN of the IAM role in the pre-production account.
        :param function_name: The Lambda funciton name for the pre-production account. Default: 'PreProd-DataBrew-Recipe-Deployer'
        :param role_name: The name of the IAM role for the pre-produciton Lambda function. Default: 'PreProd-DataBrew-Recipe-Deployer-role'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79502b2a44ad96d989a482171dc7c527e78823de7038a9b13474cb69e4b012aa)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument preproduction_iam_role_arn", value=preproduction_iam_role_arn, expected_type=type_hints["preproduction_iam_role_arn"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "preproduction_iam_role_arn": preproduction_iam_role_arn,
        }
        if function_name is not None:
            self._values["function_name"] = function_name
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''The ARN of the S3 bucket for the DataBrew CICD pipeline.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def preproduction_iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role in the pre-production account.'''
        result = self._values.get("preproduction_iam_role_arn")
        assert result is not None, "Required property 'preproduction_iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The Lambda funciton name for the pre-production account.

        :default: 'PreProd-DataBrew-Recipe-Deployer'
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role for the pre-produciton Lambda function.

        :default: 'PreProd-DataBrew-Recipe-Deployer-role'
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PreProductionLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProductionLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-databrew-cicd.ProductionLambda",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        name: builtins.str,
        *,
        bucket_arn: builtins.str,
        production_iam_role_arn: builtins.str,
        function_name: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param name: -
        :param bucket_arn: The ARN of the S3 bucket for the DataBrew CICD pipeline.
        :param production_iam_role_arn: The ARN of the IAM role in the production account.
        :param function_name: The Lambda funciton name for the production account. Default: 'Prod-DataBrew-Recipe-Deployer'
        :param role_name: The name of the IAM role for the produciton Lambda function. Default: 'Prod-DataBrew-Recipe-Deployer-role'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f76a26b0d61f092ccfd9316a19580d3ee054a24967aadc6607fccb931ac182f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        props = ProductionLambdaProps(
            bucket_arn=bucket_arn,
            production_iam_role_arn=production_iam_role_arn,
            function_name=function_name,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, name, props])

    @builtins.property
    @jsii.member(jsii_name="function")
    def function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''The representative of Lambda function for the production account.'''
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, jsii.get(self, "function"))

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        '''The Lambda funciton name for the production account.'''
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''The name of the IAM role for the produciton Lambda function.'''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))


@jsii.data_type(
    jsii_type="cdk-databrew-cicd.ProductionLambdaProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_arn": "bucketArn",
        "production_iam_role_arn": "productionIamRoleArn",
        "function_name": "functionName",
        "role_name": "roleName",
    },
)
class ProductionLambdaProps:
    def __init__(
        self,
        *,
        bucket_arn: builtins.str,
        production_iam_role_arn: builtins.str,
        function_name: typing.Optional[builtins.str] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bucket_arn: The ARN of the S3 bucket for the DataBrew CICD pipeline.
        :param production_iam_role_arn: The ARN of the IAM role in the production account.
        :param function_name: The Lambda funciton name for the production account. Default: 'Prod-DataBrew-Recipe-Deployer'
        :param role_name: The name of the IAM role for the produciton Lambda function. Default: 'Prod-DataBrew-Recipe-Deployer-role'
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e2ab50a969fe86bf2f4d34a712c420d3dc55ea2f5882e03f7fdd38731c6ba4)
            check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
            check_type(argname="argument production_iam_role_arn", value=production_iam_role_arn, expected_type=type_hints["production_iam_role_arn"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_arn": bucket_arn,
            "production_iam_role_arn": production_iam_role_arn,
        }
        if function_name is not None:
            self._values["function_name"] = function_name
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def bucket_arn(self) -> builtins.str:
        '''The ARN of the S3 bucket for the DataBrew CICD pipeline.'''
        result = self._values.get("bucket_arn")
        assert result is not None, "Required property 'bucket_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def production_iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role in the production account.'''
        result = self._values.get("production_iam_role_arn")
        assert result is not None, "Required property 'production_iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''The Lambda funciton name for the production account.

        :default: 'Prod-DataBrew-Recipe-Deployer'
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the IAM role for the produciton Lambda function.

        :default: 'Prod-DataBrew-Recipe-Deployer-role'
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProductionLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CodePipelineIamRole",
    "CodePipelineIamRoleProps",
    "DataBrewCodePipeline",
    "DataBrewCodePipelineProps",
    "FirstCommitHandler",
    "FirstCommitHandlerProps",
    "IamRole",
    "IamRoleProps",
    "InfraIamRole",
    "InfraIamRoleProps",
    "PreProductionLambda",
    "PreProductionLambdaProps",
    "ProductionLambda",
    "ProductionLambdaProps",
]

publication.publish()

def _typecheckingstub__8f4b3cedca9c3d8560bb9b34d56b1758c3a3ba17f69dcb6e4844d1cd8257728f(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    bucket_arn: builtins.str,
    preproduction_lambda_arn: builtins.str,
    production_lambda_arn: builtins.str,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c88298ceb251680594e19748f268c88132a53d9230ce141ab38c138f8bc599(
    *,
    bucket_arn: builtins.str,
    preproduction_lambda_arn: builtins.str,
    production_lambda_arn: builtins.str,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8c42e0835720c39be9e5881e6e6fcdf267e0208a259aeb42f0ad40b070d536(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    preproduction_iam_role_arn: builtins.str,
    production_iam_role_arn: builtins.str,
    branch_name: typing.Optional[builtins.str] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    first_stage_artifact_name: typing.Optional[builtins.str] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    repo_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92658886e139cd36492ca37aa02eb2e4ea2d74477ca0c1670c351079f1ff7b4e(
    *,
    preproduction_iam_role_arn: builtins.str,
    production_iam_role_arn: builtins.str,
    branch_name: typing.Optional[builtins.str] = None,
    bucket_name: typing.Optional[builtins.str] = None,
    first_stage_artifact_name: typing.Optional[builtins.str] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    repo_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c94ebf5d0f0646f9bd465f2e48aac6716fbdebb72bc0b4d3dbabf7f7d1661b(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    branch_name: builtins.str,
    code_commit_repo_arn: builtins.str,
    repo_name: builtins.str,
    function_name: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c58e09bbf56172e632a96611953e1ffee8fa846c0c4cb85b70ab890e8bdc43c(
    *,
    branch_name: builtins.str,
    code_commit_repo_arn: builtins.str,
    repo_name: builtins.str,
    function_name: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72cb2011349b8a9e66b3c943c3b2ef730a2065d923d556221587d2ad288d77b8(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    account_id: builtins.str,
    environment: builtins.str,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f03732f915db1d749b6f9404cba16b860ffd31d3f75fd61d697b03a91bc76da4(
    *,
    account_id: builtins.str,
    environment: builtins.str,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b75a148dbd27b9ab3c80a4aa84232b84c5e563450dc4475796ba74b2bb8c448d(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5745e821cbdcdd9e6286b013c8579bd6278273ee512ce50d00572c0d09a8c240(
    *,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efe3608b5814e558117f24f9265534319eaf3e415df05794ab820a21200a7b3(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    bucket_arn: builtins.str,
    preproduction_iam_role_arn: builtins.str,
    function_name: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79502b2a44ad96d989a482171dc7c527e78823de7038a9b13474cb69e4b012aa(
    *,
    bucket_arn: builtins.str,
    preproduction_iam_role_arn: builtins.str,
    function_name: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f76a26b0d61f092ccfd9316a19580d3ee054a24967aadc6607fccb931ac182f(
    scope: _constructs_77d1e7e8.Construct,
    name: builtins.str,
    *,
    bucket_arn: builtins.str,
    production_iam_role_arn: builtins.str,
    function_name: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e2ab50a969fe86bf2f4d34a712c420d3dc55ea2f5882e03f7fdd38731c6ba4(
    *,
    bucket_arn: builtins.str,
    production_iam_role_arn: builtins.str,
    function_name: typing.Optional[builtins.str] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
