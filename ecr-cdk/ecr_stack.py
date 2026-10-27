"""Stack for ECR Repository"""

import os

from constructs import Construct

from aws_cdk import Stack
from aws_cdk import aws_ecr as ecr

class ECRRepositoryStack(Stack):
    """ECR Stack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### ECR
        LAB_IMAGE_NAMES = os.getenv("LAB_IMAGE_NAMES")
        for lab_name in LAB_IMAGE_NAMES:
            ecr.Repository(
                self,
                f"{lab_name}_image",
                repository_name=lab_name,
            )