"""Application to deploy ECR repository"""

#!/usr/bin/env python3
import os

import aws_cdk as cdk

# from user_audit.user_audit_stack import UserAuditStack
from ecr_stack import ECRRepositoryStack

# User Stack Name
project_name = os.getenv("PROJECT_NAME")
stack_name = project_name if project_name else "ecr-repository"

app = cdk.App()
ECRRepositoryStack(
    app,
    stack_name,
    env=cdk.Environment(
        account=os.getenv("CDK_DEFAULT_ACCOUNT"),
        region=os.getenv("CDK_DEFAULT_REGION"),
    ),
)
app.synth()
