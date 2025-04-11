#!/bin/bash

echo "============================================"
echo "Checking EC2 instances in Auto Scaling Group"
echo "============================================"
aws ec2 describe-instances --filters "Name=tag:aws:autoscaling:groupName,Values=*HighAvailabilityApp*" --query "Reservations[].Instances[].{InstanceId:InstanceId,SubnetId:SubnetId,State:State.Name,PrivateIP:PrivateIpAddress,AZ:Placement.AvailabilityZone}"

echo -e "\n============================================"
echo "Verifying Auto Scaling Group status"
echo "============================================"
aws autoscaling describe-auto-scaling-groups --query "AutoScalingGroups[?contains(AutoScalingGroupName, 'HighAvailabilityApp')].[AutoScalingGroupName,MinSize,MaxSize,DesiredCapacity,Instances[*].{InstanceId:InstanceId,HealthStatus:HealthStatus,LifecycleState:LifecycleState}]"

echo -e "\n============================================"
echo "Checking Target Group health"
echo "============================================"
TARGET_GROUP_ARN=$(aws elbv2 describe-target-groups --query "TargetGroups[?contains(TargetGroupName, 'HighAvailabilityApp')].TargetGroupArn" --output text)
echo "Target Group ARN: $TARGET_GROUP_ARN"
aws elbv2 describe-target-health --target-group-arn $TARGET_GROUP_ARN

echo -e "\n============================================"
echo "Verifying ALB Security Group"
echo "============================================"
ALB_SG=$(aws elbv2 describe-load-balancers --query "LoadBalancers[?contains(LoadBalancerName, 'HighAv')].SecurityGroups[0]" --output text)
echo "ALB Security Group: $ALB_SG"
aws ec2 describe-security-groups --group-ids $ALB_SG

echo -e "\n============================================"
echo "Verifying EC2 Instance Security Group"
echo "============================================"
INSTANCE_ID=$(aws ec2 describe-instances --filters "Name=tag:aws:autoscaling:groupName,Values=*HighAvailabilityApp*" --query "Reservations[].Instances[0].InstanceId" --output text)
INSTANCE_SG=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID --query "Reservations[].Instances[].SecurityGroups[0].GroupId" --output text)
echo "Instance ID: $INSTANCE_ID"
echo "Instance Security Group: $INSTANCE_SG"
aws ec2 describe-security-groups --group-ids $INSTANCE_SG

echo -e "\n============================================"
echo "Checking instance system logs"
echo "============================================"
aws ec2 get-console-output --instance-id $INSTANCE_ID

echo -e "\n============================================"
echo "Checking if instance is SSM managed"
echo "============================================"
aws ssm describe-instance-information --filters "Key=InstanceIds,Values=$INSTANCE_ID"

echo -e "\n============================================"
echo "Checking Load Balancer details"
echo "============================================"
aws elbv2 describe-load-balancers --query "LoadBalancers[?contains(LoadBalancerName, 'HighAv')].{DNSName:DNSName,State:State.Code,Scheme:Scheme}"
