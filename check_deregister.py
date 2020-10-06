from sys import argv
import boto3
import logging
script, target_arn, ec2_id = argv

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s:%(levelname)s:%(message)s")
client = boto3.client('elbv2')
waiter = client.get_waiter('target_deregistered')
instance_count= 0
instance_health= {}
healthy_count=0
res = bool()

def deregister(target_arn, ec2_id):
    response = client.deregister_targets(TargetGroupArn=target_arn,Targets=[{'Id': ec2_id,}])    
    waiter.wait(TargetGroupArn=target_arn,Targets=[{'Id': ec2_id},])
    logging.debug("Load Balancer Status after Deregister: {}".format(instance_health))
    k = bool("deregistered")
    return k
  
def target_health(target_arn):
    response = client.describe_target_health(TargetGroupArn=target_arn)
    thd = response["TargetHealthDescriptions"]
    instance_count= len(thd)
    healthy_count = 0
    instance_health= {}
    for key in thd:
        instance_id=key["Target"]["Id"]
        instance_health[instance_id]= key["TargetHealth"]["State"]
        if key["TargetHealth"]["State"] == 'healthy':
            healthy_count= healthy_count+1
            
    logging.debug("Number of instances behind Load Balancer: {}".format(instance_count))
    logging.debug("Count for Healthy Instances: {}".format(healthy_count))
    logging.debug("Current load balancer status: {}".format(instance_health))
    return instance_health, healthy_count

instance_health, healthy_count = target_health(target_arn)
if healthy_count != 1:
    res = deregister(target_arn, ec2_id)
    instance_health = target_health(target_arn)
    logging.debug("Current target group status: {}".format(instance_health))
    print(res)

else:
    if instance_health[ec2_id] == "unhealthy":
        res = deregister(target_arn, ec2_id)
        instance_health = target_health(target_arn)
        logging.debug("Current target group status: {}".format(instance_health))
        print(res)
    else:
        logging.debug("Not enough healthy instances behind Load Balancer")
        print(res)
        exit(0)      
