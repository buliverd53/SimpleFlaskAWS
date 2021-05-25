import urllib, socket, json, re, os
import requests, boto3
from time import time
from botocore.config import Config

def flask_app_latest_status():
    try:
        s3 = boto3.client('s3')
        s3_object = s3.get_object(Bucket='bucket-name', Key='flask-app-status/status.json')
        body = s3_object['Body'].read().decode()
        return body
    except Exception as e:
        return ""

def flask_app_status_on_s3(data):
    client = boto3.client('s3')
    client.put_object(Body=data, Bucket='bucket-name', Key='flask-app-status/status.json')

def main():
    data = { "flask-app-status":[]}
    elb_client = boto3.client('elbv2', region_name='us-east-1')
    tg_list = elb_client.describe_target_groups(LoadBalancerArn='ELB-ARN')
    latest_status = flask_app_latest_status()
    for tg_info in tg_list['TargetGroups']:
        tg_health = elb_client.describe_target_health(TargetGroupArn=tg_info['TargetGroupArn'])
        if tg_health['TargetHealthDescriptions'][0]['TargetHealth']['State'] != 'healthy':
            tg_status = {}
            tg_status['name'] = tg_info['TargetGroupName']
            tg_status['status'] = tg_health['TargetHealthDescriptions'][0]['TargetHealth']['State']
            data['flask-app-status'].append(tg_status)
            print("flask-app *%s* status is *%s*!" % (tg_info['TargetGroupName'], tg_health['TargetHealthDescriptions'][0]['TargetHealth']['State']))
        elif tg_health['TargetHealthDescriptions'][0]['TargetHealth']['State'] == 'healthy':
            if len(latest_status) > 22:
                for flask_app_status in json.loads(latest_status)['flask-app-status']:
                    if tg_info['TargetGroupName'] == flask_app_status['name']:
                        if flask_app_status['status'] != 'healthy':
                            tg_status = {}
                            tg_status['name'] = tg_info['TargetGroupName']
                            tg_status['status'] = tg_health['TargetHealthDescriptions'][0]['TargetHealth']['State']
                            data['flask-app-status'].append(tg_status)
                            print("flask-app *%s* status is *%s*!" % (tg_info['TargetGroupName'], tg_health['TargetHealthDescriptions'][0]['TargetHealth']['State']))
            else:
                print("flask-app *%s* status is *%s*!" % (tg_info['TargetGroupName'], tg_health['TargetHealthDescriptions'][0]['TargetHealth']['State']))
       
    flask_app_status_on_s3(json.dumps(data))

if __name__ == '__main__':
    main()
