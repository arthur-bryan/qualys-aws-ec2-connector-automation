import json, boto3
from botocore.exceptions import ClientError


def do_work(account_id, external_id):

    iam_client = boto3.client('iam')

    role_name = "Role_For_QualysEC2Connector"


    trust_relationship_policy_another_iam_user = {
        "Version": "2012-10-17",
          "Statement": [
            {
              "Sid": "",
              "Effect": "Allow",
              "Principal": {
                "AWS": f"arn:aws:iam::{account_id}:root"
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
            return 'Role already exists!'
        else:
            return 'Unexpected error occurred! Role could not be created.', error
    else:
        role_arn = role_res['Role']['Arn']

    policy_json = {
        "PolicyDocument": {
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
        },
    }


    policy_name = "IAM_Policy_For_EC2Connector"
    policy_arn = ''

    try:
        policy_res = iam_client.create_policy(
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_json)
        )
        policy_arn = policy_res['Policy']['Arn']
    except ClientError as error:
        if error.response['Error']['Code'] == 'EntityAlreadyExists':
            print('Policy already exists... hence using the same policy')
            policy_arn = f'arn:aws:iam::{account_id}:policy/{policy_name}'
        else:
            print('Unexpected error occurred... hence cleaning up', error)
            iam_client.delete_role(
                RoleName= role_name
            )
            return 'Role could not be created...', error

    
    
    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
    except ClientError as error:
        print('Unexpected error occurred... hence cleaning up')
        iam_client.delete_role(
            RoleName= role_name
        )
        return 'Role could not be created...', error

    return role_arn