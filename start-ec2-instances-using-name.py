# This Lambda function is START the ec2 instances using its different custom Name Tag


import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances()
    for i in response['Reservations']:
        for instance in i['Instances']:
            for tag in instance['Tags']:

                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-ssis-ppe01-ec2' and instance['State']['Name'] == 'stopped':
                    #print(instance['InstanceId'])
                    instance_ids = (instance['InstanceId'])
                    #print(instance_ids)
                    ec2.start_instances(InstanceIds=[instance_ids])
                    logger.info(f"Starting {instance_ids}")

                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-idol-ppe02-ec2' and instance['State']['Name'] == 'stopped':
                    instance_ids = (instance['InstanceId'])
                    ec2.start_instances(InstanceIds=[instance_ids])
                    logger.info(f"Starting {instance_ids}")

                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-fileshare-ppe01-ec2' and instance['State']['Name'] == 'stopped':
                    instance_ids = (instance['InstanceId'])
                    ec2.start_instances(InstanceIds=[instance_ids])
                    logger.info(f"Starting {instance_ids}")

                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-app-ppe01-ec2' and instance['State']['Name'] == 'stopped':
                    instance_ids = (instance['InstanceId'])
                    ec2.start_instances(InstanceIds=[instance_ids])
                    logger.info(f"Starting {instance_ids}")


                if tag['Key'] == 'Name' and tag['Value'] == 'a205965-dante-batch-ppe01-ec2' and instance['State']['Name'] == 'stopped':
                    instance_ids = (instance['InstanceId'])
                    ec2.start_instances(InstanceIds=[instance_ids])
                    logger.info(f"Starting {instance_ids}")