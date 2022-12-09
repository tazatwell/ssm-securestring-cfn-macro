# Description

Please include a summary of the changes and the related issue. Please also include relevant motivation and context. List any dependencies that are required for this change.

Fixes # (issue)

## Type of change

Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update
- [ ] Update to `.github/` files

# How Has This Been Tested?

Please describe the tests that you ran to verify your changes. Provide instructions so we can reproduce. Please also list any relevant details for your test configuration

- [ ] `sam validate`
- [ ] `cfn-lint`
- [ ] `sam build`
- [ ] `sam deploy`
- [ ] Invoked the lambda with a sample payload and verified the result
- [ ] This change does not warrant testing (Documentation or `.github/` files change.

## Testing Docs

- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html)
- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint)
- [Sample CloudFormation Provider Payload for Lambda](https://docs.aws.amazon.com/lambda/latest/dg/services-cloudformation.html)


# Checklist:

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings or errors
- [ ] For application code changes I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing tests pass locally with my changes
- [ ] I have deployed the cloudformation stack and verified the lambda works by invoking it.
- [ ] Any related commit status checks pass

