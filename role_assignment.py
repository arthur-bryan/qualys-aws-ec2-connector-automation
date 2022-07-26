from botocore.exceptions import ClientError
import boto3
import json


def setup_iam(qualys_base_account_id, external_id, account_id):

    boto_sts = boto3.client('sts')

    stsresponse = boto_sts.assume_role(
        RoleArn=f"arn:aws:iam::{account_id}:role/qualysintegrationassumerole",
        RoleSessionName='newsession'
    )

    newsession_id = stsresponse["Credentials"]["AccessKeyId"]
    newsession_key = stsresponse["Credentials"]["SecretAccessKey"]
    newsession_token = stsresponse["Credentials"]["SessionToken"]

    iam_client = boto3.client(
        'iam',
        aws_access_key_id=newsession_id,
        aws_secret_access_key=newsession_key,
        aws_session_token=newsession_token
    )

    role_name = "Role_For_QualysEC2Connector"

    trust_relationship_policy_another_iam_user = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Principal": {
                    "AWS": f"arn:aws:iam::{qualys_base_account_id}:root"
                },
                "Action": "sts:AssumeRole",
                "Condition": {
                    "StringEquals": {
                        "sts:ExternalId": external_id
                    }
                }
            }
        ]
    }

    try:
        role_res = iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_relationship_policy_another_iam_user),
            Description="The ARN of the role that can be assumed by the Qualys EC2 Connector"
        )
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Role already exists!')
            role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
            pass
        else:
            print(f'Unexpected error occurred! Role could not be created. {error}')
            return
    else:
        role_arn = role_res['Role']['Arn']

    policy_json = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "",
                "Effect": "Allow",
                "Action": [
                    "ec2:DescribeInstances",
                    "ec2:DescribeAddresses",
                    "ec2:DescribeImages"
                ],
                "Resource": "*"
            }
        ]
    }

    policy_name = "IAM_Policy_For_EC2Connector"

    try:
        policy_res = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_json)
        )
        policy_arn = policy_res['Policy']['Arn']
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
        else:
            print('Unexpected error occurred', error.response['Error']['Code'])
            return 'Role could not be created...'

    try:

        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
    except ClientError as error:
        print(f"Fail on attachment {error}")
    return role_arn
    