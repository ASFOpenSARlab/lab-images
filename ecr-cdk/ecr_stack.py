"""Stack for ECR Repository"""

from constructs import Construct

from aws_cdk import Stack
from aws_cdk import aws_ecr as ecr

ECR_REPOSITORIES = [
    "deployment-opensarlab-container_sar"
    "geos631",
    "geos636",
]

class ECRRepositoryStack(Stack):
    """ECR Stack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### ECR
        for repo in ECR_REPOSITORIES:
            ecr.Repository(
                self,
                f"{repo}_image",
                repository_name=repo,
            )