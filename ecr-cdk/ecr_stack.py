"""Stack for ECR Repository"""

import os

from constructs import Construct

from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    aws_iam as iam,
)

class ECRRepositoryStack(Stack):
    """ECR Stack"""

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ecr_policy = iam.PolicyStatement(
            sid="AllowPullFromOtherAccount",
            effect=iam.Effect.ALLOW,
            # principals=[iam.ArnPrincipal(f"arn:aws:*:{self.region}:*")], # replace first * with ec2 if possible
            principals=[iam.ArnPrincipal("*")],
            actions=[
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ]
        )

        ### ECR
        LAB_IMAGE_NAMES = os.getenv("LAB_IMAGE_NAMES").split()
        for lab_name in LAB_IMAGE_NAMES:
            ECR = ecr.Repository(
                self,
                f"{lab_name}_image",
                repository_name=lab_name,
            )

            ECR.add_to_resource_policy(ecr_policy)


        ### OIDC DEPLOY ROLE
        oidc_provider = iam.OidcProviderNative(
            self,
            "GitHubProvider",
            url="https://token.actions.githubusercontent.com",
            client_ids=["https://github.com"],
        )

        deploy_image_role = iam.Role(
            self,
            "DeployImageRole",
            assumed_by=iam.OpenIdConnectPrincipal(
                oidc_provider,
                {
                    "StringEquals":{
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                    },
                    "StringLike": {
                        "token.actions.githubusercontent.com:sub" "repo:ASFOpenSARlab@83985517/lab-images@1338528871:*"
                    },
                },
            ),
        )