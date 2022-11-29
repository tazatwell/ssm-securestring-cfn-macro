# ssm-securestring-cfn-macro

Create AWS Systems Manager SecureString Parameters using a Lambda-backed CloudFormation Macro

## Install

- Install python3.9
- Install aws-cli and aws-sam-cli

## Deploy

```
sam build
sam deploy \
  --stack-name ssm-securestring-cfn-macro \
  --template-file .aws-sam/build/template.yaml \
  --s3-bucket SOME_S3_BUCKET \
  --s3-prefix SOME_S3_PREFIX \
  --capabilities CAPABILITY_NAMED_IAM
```

## Delete

```
sam delete \
  --stack-name ssm-securestring-cfn-macro \
  --s3-bucket SOME_S3_BUCKET \
  --s3-prefix SOME_S3_PREFIX \
```
