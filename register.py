from sys import argv
import boto3
client = boto3.client('elbv2')
waiter = client.get_waiter('target_in_service')

script, target, ec2_id = argv

response = client.register_targets(TargetGroupArn=target,Targets=[{'Id': ec2_id,}])    
waiter.wait(TargetGroupArn=target,Targets=[{'Id': ec2_id},])
print("register process completed")

