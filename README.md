# Safeguard your environment and reduce reputational risk using Amazon Connect attachment scanning

## Introduction
This project deploys an attachment scanning solution based on Amazon Rekognition to identify inappropriate, unwanted, or offensive content in images based on general or business-specific standards and practices.

## Architecture
![Architecture Diagram](./architecture.jpg)

1. Customer initiates a chat from your website using the [communications widget](https://docs.aws.amazon.com/connect/latest/adminguide/add-chat-to-website.html#customize-chat-widget) hosted by Amazon Connect or mobile application using the [Amazon Connect Chat SDK](https://github.com/amazon-connect/amazon-connect-chat-ui-examples/)
2. The chat is routed to an available agent based on your [Amazon Connect Flow](https://docs.aws.amazon.com/connect/latest/adminguide/connect-contact-flows.html) configuration.
3. The customer or agent sends a [chat attachment](https://docs.aws.amazon.com/connect/latest/adminguide/enable-attachments.html) and the file is uploaded to Amazon S3 bucket
4. Amazon Connect instance invokes the attachment scanner AWS Lambda function that handles scanning files
5. Scanner Lambda function retrieves the file from S3 bucket
6. Scanner Lambda function calls Amazon Rekognition DetectModetationLabel API
7. Amazon Connect marks the attachment APPROVED or REJECTED based on the Lambda status response. If the result is REJECTED, the attachment files in S3 are automatically deleted from both staging and final locations


## Prerequisties
- An [AWS account](https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fportal.aws.amazon.com%2Fbilling%2Fsignup%2Fresume&client_id=signup)
- An [IAM User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) with programmatic access
- An existing [Amazon Connect instance](https://docs.aws.amazon.com/connect/latest/adminguide/amazon-connect-instances.html) with attachments enabled
- AWS IAM with access to create users, policies and roles
- Local installation of [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) and experience using the AWS CLI
- Amazon S3 bucket name where chat attachments are stored. For more information, see [Update data storage](https://docs.aws.amazon.com/connect/latest/adminguide/update-instance-settings.html#update-data-storage-options) in the Amazon Connect Administrator Guide

## Deploy the solution

1.	Using Git, clone the repository from GitHub
```
git clone https://github.com/aws-samples/safeguard-your-environment-and-reduce-reputational-risk-using-amazon-connect-attachment-scanning
```
2.	Browse to the directory where the repository is downloaded
```
cd safeguard-your-environment-and-reduce-reputational-risk-using-amazon-connect-attachment-scanning
```
3.	Build the solution with SAM
```
sam build
```
4.	Deploy the solution
```
sam deploy --g
```

## Usage
After the SAM application is deployed, please follow the steps outlined in blog post [**Safeguard your environment and reduce reputational risk using Amazon Connect attachment scanning**](https://aws.amazon.com/blogs/contact-center/safeguard-your-environment-and-reduce-reputational-risk-using-amazon-connect-attachment-scanning)

## Useful commands
* `sam build`  creates .aws-sam directory that structures your application
* `sam deploy --g` deploys serverless application to the AWS Cloud

## Security
See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License
This project is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.
