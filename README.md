# ssm-securestring-cfn-macro

Create AWS Systems Manager SecureString Parameters using a Lambda-backed CloudFormation Macro

## Install

- [Install python3.9](https://www.python.org/downloads/release/python-390/)
- [Install aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Install sam-cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- Make sure that your IAM role has the appropriate permissions to deploy this resource. This includes being able to create IAM Roles, Lambda Functions, Lambda Layers, CloudFormation Macros, and CloudFormation stacks.

## Deploy

There are two steps: building the lambda layer locally, then deploying the CloudFormation stack.
 
```
make build
make deploy
```

## Delete

```
make delete
```

## Example CloudFormation Invocation

After the lambda is deployed, the following CloudFormation template will create a SSM SecureString Parameter:

```
AWSTemplateFormatVersion: '2010-09-09'

Resources:
  SSMSecureStringParam:
    Type: Custom::SSMSecureStringParam
    Properties:
      ServiceToken:
        Fn::ImportValue: "ssm-securestring-cfn-macro-function-arn"
      Name: string
      Description: string
      Value: string
      Type: "String|StringList|SecureString"
      KeyId: string
      Overwrite: "True|False"
      AllowedPattern: string
      Tier: "Standard|Advanced|Intelligent-Tiering"
      Policies: string
      DataType: string
      Tags: string
      Debug: "True|False"
      IgnoreParamNotFound: "True|False"
```

Most of these parameters are optional. To see the full list of required parameters, see the documentation for the [`aws ssm put-parameter ...`](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/put-parameter.html) and [`aws ssm delete-parameter ...`](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ssm/delete-parameter.html) api functions. The macro does not accept the `--cli-input...`, `--generate-cli-skeleton`, or any of the global aws api flags.

The lambda accepts two operational flags: `Debug` and `IgnoreParamNotFound`. The `Debug` flag will print additional runtime information in the lambda's CloudWatch logs. The `IgnoreParamNotFound` flag will cause the lambda to not fail if it attemps to delete a parameter that does not exist. This is useful if a parameter is modified/deleted through the console outside of CloudFormation stack updates.

The `parameter.yaml` is an example of a fully parameterized CloudFormation template that can be used to create any SSM Parameter using this macro.

## Considerations

- If you use a custom KMS Key to encrypt SSM SecureString Parameters, the lambda's IAM Role must have the `kms:Encrypt` action permission defined for it. You must include that permission in the `template.yaml`.
- If you create a SecureString Parameter from a CloudFormation template that invokes the macro, then pass the value of the parameter as a CloudFormation parameter with the `NoEcho` property to prevent sensitive information from being visible in the template or parameters. See the [AWS CloudFormation Parameters Warnings](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html#parameters-section-structure-properties) for more information.

