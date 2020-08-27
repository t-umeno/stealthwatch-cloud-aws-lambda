#!/bin/bash
aws s3 rm s3://stealthwatch-cloud-getflow/function.zip
aws s3 cp function.zip s3://stealthwatch-cloud-getflow/
aws lambda delete-function --function-name GetFlow
aws lambda create-function --debug --function-name GetFlow --runtime python3.6 --role arn:aws:iam::633906190213:role/lambda-s3fullaceess-role --handler get_flows_lambda.lambda_handler --code S3Bucket=stealthwatch-cloud-getflow,S3Key=function.zip --timeout 30 --memory-size 128
