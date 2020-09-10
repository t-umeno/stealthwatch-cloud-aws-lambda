#!/bin/bash
aws lambda update-function-configuration --function-name GetFlow --environment "Variables={$1}"
