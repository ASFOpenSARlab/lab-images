# OpenScienceLab custom lab images

* [OpenSARLab](./opensarlab/)
* [GEOS631](./geos631) - Foundations of Geophysics 
* [GEOS636](./geos636) - Programming and Automation for Geosciences

## Running lab images locally

```shell
lab=geos631;

docker \
     run \
     -it \
     -p 8888:8888 \
     --entrypoint bash \
     ghcr.io/asfopensarlab/${lab}:test \
         -c " \
               /etc/user_server_includes/hooks/${lab}.sh &&  \
               tini -g -- start.sh start-notebook.py \
            "
```

## Deploying ECR

1. Create or use an environment with the following **variables** defined
    * AWS_ACCOUNT_NUMBER
    * AWS_DEFAULT_REGION
    * LAB_IMAGE_NAMES
    * OIDC_IAM_ROLE \
    And the following **secrets**
    * OIDC_PROVIDER_ARN
1. Run `Deploy ECR CDK` action with your environment selected
1. Set the GitHub Variable `OIDC_ROLE_ARN` to the Cloudfront output `DeployImageRoleArn`
1. When deploying a lab image, select `Deploy To ECR as Well`