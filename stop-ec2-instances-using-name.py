# This Lambda function is STOP the ec2 instances using its different custom Name Tag

import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event,contex):
    
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    for i in response['Reservations']:
        for instance in i['Instances']:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-ssis-ppe01-ec2' and instance['State']['Name'] == 'running':
                    #print(instance['InstanceId'])
                    instance_ids = (instance['InstanceId'])
                    #print(instance_ids)
                    ec2.stop_instances(InstanceIds=[instance_ids])
                    logger.info(f"Stopping {instance_ids}")

                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-idol-ppe02-ec2' and instance['State']['Name'] == 'running':
                    instance_ids = (instance['InstanceId'])
                    ec2.stop_instances(InstanceIds=[instance_ids])
                    logger.info(f"Stopping {instance_ids}")

                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-fileshare-ppe01-ec2' and instance['State']['Name'] == 'running':
                    instance_ids = (instance['InstanceId'])
                    ec2.stop_instances(InstanceIds=[instance_ids])
                    logger.info(f"Stopping {instance_ids}")

                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-app-ppe01-ec2' and instance['State']['Name'] == 'running':
                    instance_ids = (instance['InstanceId'])
                    ec2.stop_instances(InstanceIds=[instance_ids])
                    logger.info(f"Stopping {instance_ids}")

                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-batch-ppe01-ec2' and instance['State']['Name'] == 'running':
                    instance_ids = (instance['InstanceId'])
                    ec2.stop_instances(InstanceIds=[instance_ids])
                    logger.info(f"Stopping {instance_ids}")