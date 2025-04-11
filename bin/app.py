
#!/usr/bin/env python3

import aws_cdk as cdk
from high_availability_app.vpc_stack import VPCStack
from high_availability_app.app_stack import AppStack

app = cdk.App()

# Create VPC stack
vpc_stack = VPCStack(app, "HighAvailabilityVPC")

# Create App stack that depends on the VPC stack
app_stack = AppStack(app, "HighAvailabilityApp", vpc=vpc_stack.vpc)

app.synth()
