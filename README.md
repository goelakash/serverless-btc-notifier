# Serverless Daily Bitcoin Price Checker

This is an [AWS Lambda](https://aws.amazon.com/lambda/) function that fetches the daily price of bitcoin from [Coindesk](https://www.coindesk.com). Using [Amazon Simple Notification Service](https://aws.amazon.com/sns/), it is able to send an SMS each day to a pre-configured phone number.

Note: [SNS only supports SMS messaging in a subset of regions](http://docs.aws.amazon.com/sns/latest/dg/sms_supported-countries.html). Please see the linked support document to ensure you deploy this application in a supported region.

### Pre-requisites

1. Install [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)
2. Create an [S3](https://aws.amazon.com/s3/) bucket in your default region.

### Deployment

Deploying this serverless app to your AWS account is quick and easy using [AWS CloudFormation](https://aws.amazon.com/cloudformation/).

### Packaging

With the [AWS CLI](https://aws.amazon.com/cli/) installed, run the following command to upload the code to S3. Set `DEPLOYMENT_S3_BUCKET` to bucket you own; CloudFormation will copy the code function into a ZIP file in this S3 bucket, which can be deployed to AWS Lambda in the following steps.

```sh
DEPLOYMENT_S3_BUCKET="YOUR_S3_BUCKET"
aws cloudformation package --template-file cloudformation.yaml --s3-bucket $DEPLOYMENT_S3_BUCKET \
  --output-template-file cloudformation-packaged.yaml
```


### Configuration

1. You can set the following parameters:

 * `STACK_NAME` is the name of the CloudFormation stack that you'll create to manage all the resources (Lambda functions, CloudWatch Events) associated with this app. You can set this to a new value to create a new instance with different parameters in your account, or use the same value when re-running to update parameters of an existing deployment.
 * `PHONE_NUMBER` is the recipient of the daily headline. Use [E.164](https://en.wikipedia.org/wiki/E.164) (e.g. +919987123456) format.
 * `UTC_HOUR` is the UTC hour at which to send the price.

```sh
STACK_NAME="serverless-daily-bitcoin-checker"
PHONE_NUMBER="+919987123456"
UTC_HOUR="3"
```

2. With the configuration parameters defined, we can call `cloudformation deploy` to create the necessary resources in your AWS account:

```sh
aws cloudformation deploy --template-file cloudformation-packaged.yaml \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides "PhoneNumber=$PHONE_NUMBER" "UTCHour=$UTC_HOUR" \
  --stack-name $STACK_NAME
````

If all went well, your stack has now been created.

3. The previous step creates an SNS topic to publish the price updates. Update the SNS topic ARN in your Lambda function. Refer [this](http://docs.aws.amazon.com/lambda/latest/dg/env_variables.html) to add the SNS_TOPIC environment variable to the lambda function created by cloudformation.


4. We're almost done. The SMS subscription that you've setup may not send the SMS in a timely or a reliable manner. To change that, update your Text Messaging preferences in SNS to ```Transactional```. You can read more [here](http://docs.aws.amazon.com/sns/latest/dg/sms_publish-to-phone.html).


That's it. You're daily bitcoin price ticker should be up and running smoothly.

*(Please open an issue thread if things do not seem to work out for you)*