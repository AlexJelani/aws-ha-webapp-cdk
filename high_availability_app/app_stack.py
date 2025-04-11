from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_autoscaling as autoscaling,
    aws_cloudwatch as cloudwatch,
    aws_backup as backup,
    aws_events as events,
    Duration,
    Tags
)
from constructs import Construct


class AppStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Read user data script
        with open("init_script/init_script.sh", "r") as file:
            user_data = file.read()

        # Create security group for EC2 instances
        instance_sg = ec2.SecurityGroup(
            self, "InstanceSG",
            vpc=vpc,
            description="Security group for EC2 instances",
            allow_all_outbound=True
        )

        # Create security group for ALB
        alb_sg = ec2.SecurityGroup(
            self, "ALBSG",
            vpc=vpc,
            description="Security group for ALB",
            allow_all_outbound=True
        )

        # Allow HTTP traffic from ALB to instances
        instance_sg.add_ingress_rule(
            alb_sg,
            ec2.Port.tcp(80),
            "Allow HTTP traffic from ALB"
        )

        # Allow HTTP traffic from anywhere to ALB
        alb_sg.add_ingress_rule(
            ec2.Peer.any_ipv4(),
            ec2.Port.tcp(80),
            "Allow HTTP traffic from anywhere"
        )

        # Create launch template
        launch_template = ec2.LaunchTemplate(
            self, "LaunchTemplate",
            machine_image=ec2.AmazonLinuxImage(
                generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
            ),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE3,
                ec2.InstanceSize.MICRO
            ),
            security_group=instance_sg,
            user_data=ec2.UserData.custom(user_data)
        )

        # Create Auto Scaling Group
        asg = autoscaling.AutoScalingGroup(
            self, "ASG",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            mixed_instances_policy=autoscaling.MixedInstancesPolicy(
                instances_distribution=autoscaling.InstancesDistribution(
                    on_demand_percentage_above_base_capacity=0,
                ),
                launch_template=launch_template,
                launch_template_overrides=[
                    autoscaling.LaunchTemplateOverrides(
                        instance_type=ec2.InstanceType.of(
                            ec2.InstanceClass.BURSTABLE3,
                            ec2.InstanceSize.MICRO
                        )
                    )
                ]
            ),
            min_capacity=1,
            max_capacity=4,
            desired_capacity=2
        )

        # Add this line to acknowledge the warning
        Tags.of(asg).add("aws-cdk:auto-scaling-group:desired-capacity", "true")

        # Create ALB
        alb = elbv2.ApplicationLoadBalancer(
            self, "ALB",
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            security_group=alb_sg,
            internet_facing=True
        )

        # Add listener to ALB
        listener = alb.add_listener(
            "Listener",
            port=80,
            open=True
        )

        # Add target group to listener
        listener.add_targets(
            "Targets",
            port=80,
            targets=[asg]
        )

        # Create CloudWatch alarm for high CPU
        alarm = cloudwatch.Alarm(
            self, "HighCPUAlarm",
            metric=cloudwatch.Metric(
                namespace="AWS/EC2",
                metric_name="CPUUtilization",
                dimensions_map={
                    "AutoScalingGroupName": asg.auto_scaling_group_name
                },
                statistic="Average",
                period=Duration.minutes(5)
            ),
            threshold=80,
            evaluation_periods=2,
            datapoints_to_alarm=2,
            alarm_description="Alarm if CPU exceeds 80%"
        )

        # Create AWS Backup plan with explicit vault name
        backup_plan = backup.BackupPlan(
            self, "BackupPlan",
            backup_vault=backup.BackupVault(
                self, "BackupVault",
                backup_vault_name=f"HighAvailabilityAppVault-{self.stack_name}"
            )
        )

        # Add backup resources
        backup_plan.add_selection(
            "Selection",
            resources=[
                backup.BackupResource.from_tag("Name", "HighAvailabilityApp")
            ]
        )

        # Add daily backup rule
        backup_plan.add_rule(
            backup.BackupPlanRule(
                delete_after=Duration.days(7),
                schedule_expression=events.Schedule.cron(
                    hour="3",
                    minute="0"
                )
            )
        )