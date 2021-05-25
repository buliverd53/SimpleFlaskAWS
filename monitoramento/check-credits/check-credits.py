import boto3
from datetime import datetime, timedelta
from time import time

def get_instance_name(inst):
    for t in inst['Tags']:
        if t['Key'] == 'Name':
            return t['Value']
    return ''

def get_t_instances():
    ec2 = boto3.client('ec2')

    filters = [{'Name': 'instance-type', 'Values': ['t*.*']}]
    reservations = ec2.describe_instances(Filters=filters)

    t_instances = []
    for res in reservations['Reservations']:
        for inst in res['Instances']:
            inst_data = {
                'name': get_instance_name(inst),
                'type': inst['InstanceType'],
                'id': inst['InstanceId'],
                'state': inst['State']['Name']
            }

            if inst_data['state'] == 'running':
                t_instances.append(inst_data)

    return t_instances

def get_cpu_credits(instance_id):
    cw = boto3.client('cloudwatch')

    try:
        cpu_credits = cw.get_metric_statistics(
            Namespace='AWS/EC2', MetricName='CPUCreditBalance',
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            Statistics=['Average'], Period=60,
            StartTime=datetime.utcnow() - timedelta(seconds=600),
            EndTime=datetime.utcnow()
        )
        return cpu_credits['Datapoints'][0]['Average']
    except Exception:
        pass

def main():
    instances = get_t_instances()

    for inst in instances:
        if inst['state'] != 'running':
            continue

        cpu_credits = get_cpu_credits(inst['id'])
        inst.update({'credits': cpu_credits})
        print("Instancia: " + inst['name'], cpu_credits)


if __name__ == '__main__':
    main()
