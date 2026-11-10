"""Stack for ECR Repository"""

import os

from constructs import Construct

from aws_cdk import (
    Stack,
    aws_ecr as ecr,
    aws_iam as iam,
    CfnOutput,
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
        # Get or create OIDC provider
        if os.getenv("OIDC_PROVIDER_ARN"):
            oidc_provider = iam.OidcProviderNative.from_oidc_provider_arn(
                self,
                "GitHubProvider",
                os.getenv("OIDC_PROVIDER_ARN"),
            )
        else:
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
                open_id_connect_provider=oidc_provider,
                conditions={
                    "StringEquals":{
                        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
                    },
                    "StringLike": { # This must be parameterized
                        "token.actions.githubusercontent.com:sub": "repo:ASFOpenSARlab@83985517/lab-images@1338528871:*"
                    },
                },
            ),
        )

        lab_image_names = os.getenv("LAB_IMAGE_NAMES").split()

        deploy_image_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "ecr:CompleteLayerUpload",
                    "ecr:UploadLayerPart",
                    "ecr:InitiateLayerUpload",
                    "ecr:BatchCheckLayerAvailability",
                    "ecr:PutImage",
                    "ecr:BatchGetImage",
                ],
                resources=[
                    f"arn:aws:{self.account}:{self.region}:repository/{name}"
                    for name in lab_image_names
                ]
            )
        )

        deploy_image_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "ecr:GetAuthorizationToken"
                ],
                resources=["*"]
            )
        )

        CfnOutput(
            self,
            "DeployImageRoleArn",
            value=deploy_image_role.role_arn,
            description="Arn for Image Deployment Role",
        )