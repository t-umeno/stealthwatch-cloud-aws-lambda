import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
import urllib.request

import requests
import json
import datetime

# LINE notify's API
LINE_TOKEN = os.environ['LINE_TOKEN']
LINE_NOTIFY_URL = "https://notify-api.line.me/api/notify"
line_msg = os.environ['LINE_MSG']

# Read environment variable
stealthwatch_cloud_portal_url = os.environ['STEALTHWATCH_CLOUD_PORTAL_URL']
stealthwatch_cloud_api_user = os.environ['STEALTHWATCH_CLOUD_API_USER']
stealthwatch_cloud_api_key = os.environ['STEALTHWATCH_CLOUD_API_KEY']
stealthwatch_cloud_minites = int(os.environ['STEALTHWATCH_CLOUD_MINITES'])
stealthwatch_cloud_min_flows = int(os.environ['STEALTHWATCH_CLOUD_MIN_FLOWS'])

s3_client = boto3.client('s3')

def send_info(msg):
    method = "POST"
    headers = {"Authorization": "Bearer %s" % LINE_TOKEN}
    payload = {"message": msg}
    try:
        payload = urllib.parse.urlencode(payload).encode("utf-8")
        req = urllib.request.Request(
            url=LINE_NOTIFY_URL, data=payload, method=method, headers=headers)
        urllib.request.urlopen(req)
    except Exception as e:
        print ("Exception Error: ", e)
        sys.exit(1)

def get_flows(upload_path):
    try:
        requests.packages.urllib3.disable_warnings()
    except:
        pass

    # Set the URL
    url = "https://" + stealthwatch_cloud_portal_url + "/api/v3/snapshots/session-data/"

    # Set the authorization string
    authorization = "ApiKey " + stealthwatch_cloud_api_user + ":" + stealthwatch_cloud_api_key

    # Create the request headers with authorization
    request_headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json",
        "Authorization" : authorization
    }

    # Set the timestamps for the filters, in the correct format, for last 60 minutes
    end_datetime = datetime.datetime.utcnow()
    start_datetime = end_datetime - datetime.timedelta(minutes=stealthwatch_cloud_minites)
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

        # write file
        with open(upload_path, 'w') as f:
            json.dump(flows, f, indent=4)

        # print len json
        flows_len = len(flows)
        print('flows_len = %d, stealthwatch_cloud_min_flows = %d, stealthwatch_cloud_minites = %d' % (flows_len, stealthwatch_cloud_min_flows, stealthwatch_cloud_minites))
        if (flows_len <= stealthwatch_cloud_min_flows):
            print('flows_len <= stealthwatch_cloud_min_flows, line_msg: %s' % line_msg)
            send_info(line_msg)

    # If unable to fetch list of alerts
    else:
        print("An error has ocurred, while fetching flows, with the following code {}".format(response.status_code))

def lambda_handler(event, context):
    isoformat_utc = datetime.datetime.utcnow().isoformat()

    bucket = 'stealthwatch-cloud-getflow'
    key = 'get_flows.' + isoformat_utc + 'Z.json'
    upload_path = '/tmp/' + key
    get_flows(upload_path)
    s3_client.upload_file(upload_path, bucket, key)
