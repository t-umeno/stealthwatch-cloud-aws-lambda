#!/bin/bash
AWS_ACCOUNT_ID=$1
S3_BUCKET=$2
aws s3 rm s3://${S3_BUCKET}/function.zip
aws s3 cp function.zip s3://${S3_BUCKET}/
aws lambda delete-function --function-name GetFlow
aws lambda create-function --debug --function-name GetFlow --runtime python3.6 --role arn:aws:iam::${AWS_ACCOUNT_ID}:role/lambda-s3fullaceess-role --handler get_flows_lambda.lambda_handler --code S3Bucket=${S3_BUCKET},S3Key=function.zip --timeout 30 --memory-size 128
aws s3 rm s3://${S3_BUCKET}/function.zip
