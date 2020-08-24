import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus

import requests
import json
import datetime
import configparser

def get_flows(image_path, resized_path):
    try:
        requests.packages.urllib3.disable_warnings()
    except:
        pass


    # Read the config file
    config = configparser.ConfigParser()
    config.read("env.conf")

    # Set the URL
    url = "https://" + config["StealthwatchCloud"]["PORTAL_URL"] + "/api/v3/snapshots/session-data/"

    # Set the authorization string
    authorization = "ApiKey " + config["StealthwatchCloud"]["API_USER"] + ":" + config["StealthwatchCloud"]["API_KEY"]

    # Create the request headers with authorization
    request_headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "Authorization" : authorization
    }

    # Set the timestamps for the filters, in the correct format, for last 60 minutes
    end_datetime = datetime.datetime.utcnow()
    start_datetime = end_datetime - datetime.timedelta(minutes=60)
    end_timestamp = end_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    start_timestamp = start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

    request_parameters = {
        "start_timestamp_utc__gte" : start_timestamp,
        "start_timestamp_utc__lt" : end_timestamp
    }

    # Initialize the requests session
    api_session = requests.Session()

    # Get the list of flows from Stealthwatch Cloud
    response = api_session.request("GET", url, headers=request_headers, params=request_parameters, verify=False)

    # If successfully able to get list of flows
    if (response.status_code == 200):

        # Loop through the list and print each flows
        flows = json.loads(response.content)["objects"]
        for flow in flows:
            #print(json.dumps(flow, indent=4)) # formatted print
            print(flow)

    # If unable to fetch list of alerts
    else:
        print("An error has ocurred, while fetching flows, with the following code {}".format(response.status_code))

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = unquote_plus(record['s3']['object']['key'])
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/resized-{}'.format(tmpkey)
        s3_client.download_file(bucket, key, download_path)
        resize_image(download_path, upload_path)
        s3_client.upload_file(upload_path, '{}-resized'.format(bucket), key)
