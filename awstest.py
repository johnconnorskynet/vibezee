import boto3
import json

ec2client = boto3.client('ec2')
# j = json.load()
# print (json.dumps(ec2client.describe_instances(), sort_keys=True, indent=2))
ec2infodict = ec2client.describe_instances()
print(ec2infodict['Reservations'][0]['Instances'][0]['State'])
instanceId = ec2infodict['Reservations'][0]['Instances'][0]['InstanceId']
ec2client.stop_instances(InstanceIds=[instanceId])
print(ec2client.describe_instance_status())
print("it works")
# ec2client.start_instances(InstanceIds=[instanceId])