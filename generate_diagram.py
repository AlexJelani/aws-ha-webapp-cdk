#!/usr/bin/env python3
import os
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, EC2AutoScaling
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, InternetGateway, NATGateway, ALB
from diagrams.aws.management import Cloudwatch
from diagrams.aws.storage import S3
from diagrams.aws.security import Shield
from diagrams.aws.general import Users

# Create output directory if it doesn't exist
os.makedirs("diagrams", exist_ok=True)

# Create the diagram
with Diagram("High-Availability Web Application Architecture", show=False, filename="diagrams/ha_architecture", outformat="png"):
    
    users = Users("End Users")
    
    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            igw = InternetGateway("Internet Gateway")
            
            with Cluster("Availability Zone 1"):
                public_subnet1 = PublicSubnet("Public Subnet 1")
                private_subnet1 = PrivateSubnet("Private Subnet 1")
                nat1 = NATGateway("NAT Gateway")
                
            with Cluster("Availability Zone 2"):
                public_subnet2 = PublicSubnet("Public Subnet 2")
                private_subnet2 = PrivateSubnet("Private Subnet 2")
            
            alb = ALB("Application Load Balancer")
            
            with Cluster("Auto Scaling Group"):
                asg = EC2AutoScaling("Auto Scaling Group")
                ec2_1 = EC2("Web Server 1")
                ec2_2 = EC2("Web Server 2")
            
            cloudwatch = Cloudwatch("CloudWatch\nAlarms")
            backup = S3("AWS Backup")
            
            # Connect components
            users >> igw >> alb
            alb >> public_subnet1
            alb >> public_subnet2
            
            public_subnet1 >> nat1
            nat1 >> private_subnet1
            
            asg - Edge(color="brown", style="dashed") - cloudwatch
            
            private_subnet1 >> ec2_1
            private_subnet2 >> ec2_2
            
            ec2_1 >> backup
            ec2_2 >> backup
            
            alb >> ec2_1
            alb >> ec2_2

print("Diagram generated successfully at diagrams/ha_architecture.png")
