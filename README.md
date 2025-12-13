[![Codacy Badge](https://app.codacy.com/project/badge/Grade/37b7c1b20a32415ba522a79505bdd9bd)](https://www.codacy.com/gh/arthur-bryan/qualys-aws-ec2-connector-automation/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=arthur-bryan/qualys-aws-ec2-connector-automation&amp;utm_campaign=Badge_Grade)
[![Open Source](https://img.shields.io/badge/Open%20Source-05C230?logo=Github&logoColor=white&link=https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation)](https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation)
[![Status Badge](https://img.shields.io/badge/status-development-05C230)](https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation/tree/dev)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/arthur-bryan/qualys-aws-ec2-connector-automation?color=05C230)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/arthur-bryan/qualys-aws-ec2-connector-automation?color=05C230)](https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation/tags)
[![Python Badge](https://img.shields.io/badge/-Python-05C230?logo=Python&logoColor=white&link=https://www.python.org/)](https://github.com/arthur-bryan?tab=repositories&q=&type=&language=python)
![GitHub repo size](https://img.shields.io/github/repo-size/arthur-bryan/qualys-aws-ec2-connector-automation?color=05C230)

# :octocat: qualys-aws-ec2-connector-automation
Code for AWS Lambda Function which is triggered by a Control Tower lifecycle account creation event.
The function creates an AWS EC2 Connector on Qualys, for each created account and enable it on Cloud View.
The lambda must be at your Management Account.

-   :heavy_check_mark: Automatic creation of Qualys AWS EC2 Connector when creating AWS accounts with Control Tower
-   :heavy_check_mark: Receive notifications on Slack

> **Note**: Since 2022, Qualys offers an [Organization connector](https://docs.qualys.com/en/conn/latest/aws/create_aws_org_connectors.htm) that can automatically discover accounts in an AWS Organization and create connectors for new accounts. Consider evaluating if it meets your needs before using this custom solution. This project may still be useful if you need specific Control Tower event triggers, custom filtering logic, Slack notifications, or custom IAM role configurations.

## :information_source: API version

This project uses the Qualys Asset Management API **v2** for connector operations:
- `qps/rest/2.0/create/am/awsassetdataconnector` - Create connector
- `qps/rest/2.0/update/am/awsassetdataconnector` - Activate connector
- `qps/rest/2.0/delete/am/awsassetdataconnector` - Delete connector
- `qps/rest/3.0/search/am/awsassetdataconnector` - List connectors

> **Note**: Qualys has released API v3 with additional features (runFrequency, activation modules, Cloud Perimeter Scan). The v2 APIs may be deprecated in the future. See [Connector APIs (3.0)](https://docs.qualys.com/en/conn/api/aws_3/connector_v3_apis.htm) for more details.

## :gear: Configuration

Before deploying, you must update the following values based on your environment:

### Files to modify

| File | Variable | Description | How to get |
|------|----------|-------------|------------|
| `lambda_function.py` | `api_server_url` | Qualys API server URL | Depends on your Qualys platform location. See [Qualys Platform URLs](https://www.qualys.com/platform-identification/) |
| `xml/connectors/create_aws_connector.xml` | `externalId` | Unique identifier for cross-account access | Generate a unique value or use format `PodID-CustomerId-{random_string}`. Get PodId and CustomerId from Qualys CloudView under 'Create AWS Connector' |
| `role_assignment.py` | `qualysintegrationassumerole` | IAM role name in target accounts | Must match the role name deployed to your AWS accounts via Control Tower |

### External ID

The External ID is used to secure the cross-account IAM role trust relationship. It prevents the [confused deputy problem](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html).

**Format**: `PodID-CustomerId-{random_string_between_1_and_512_characters}`

**How to get PodId and CustomerId**:
1. Log in to your Qualys subscription
2. Go to CloudView > Connectors > Create AWS Connector
3. The PodId and CustomerId are displayed in the connector creation wizard

Alternatively, you can use any unique string, but the new format is recommended for API v3 compatibility.

### Environment variables

| Variable | Description |
|----------|-------------|
| `QUALYS_API_USER` | Username with manager permissions on Qualys |
| `QUALYS_API_PASSWORD` | Password for the Qualys API user |
| `QUALYS_BASE_ACCOUNT_ID` | Qualys AWS account ID (found in Qualys portal when creating a connector manually) |
| `SLACK_TEST_CHANNEL_WEBHOOK_URL` | Webhook URL for posting notifications to your Slack channel |

## :hammer_and_wrench: Setup

1 - Clone the repository.
```sh
git clone https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation
cd qualys-aws-ec2-connector-automation
```

2 - Update configuration files as described in the [Configuration](#gear-configuration) section.

3 - Install the requirements to a folder and zip it.
```sh
pip install --target ./dependencies -r requirements.txt
zip -r dependencies.zip dependencies
```

4 - Create a layer at the AWS management account for your Lambda using the zip file with the requirements.

5 - Zip the source code.
```sh
zip -r qualys-aws-ec2-connector-automation.zip qualys-aws-ec2-connector-automation
```

6 - Create the AWS Lambda function using the zipped source.

7 - At the Lambda configuration, edit the timeout (recommended 1:30 minutes).

8 - Set the required environment variables for the Lambda function (see [Environment variables](#environment-variables) table).

9 - Create a Role to allow your Lambda to assume roles.

## :computer: Usage
1 - Create an account using Control Tower.
- The account must have the following Rule and Policy to allow the Lambda to work:

  - Role:
    ```json
    {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::<management_account_id>:role/service-role/<name_for_service_role_on_management_account>"
            },
            "Action": "sts:AssumeRole",
            "Condition": {}
        }
      ]
    }
    ```
  - Policy:
      ```json
      {
      "Version": "2012-10-17",
      "Statement": [
          {
              "Sid": "VisualEditor0",
              "Effect": "Allow",
              "Action": [
                  "iam:CreatePolicy",
                  "iam:PassRole",
                  "iam:DetachRolePolicy",
                  "iam:AttachGroupPolicy",
                  "iam:CreateRole",
                  "iam:AttachRolePolicy",
                  "iam:UpdateRole",
                  "iam:DetachGroupPolicy",
                  "iam:PutRolePolicy",
                  "iam:PutGroupPolicy"
              ],
              "Resource": "*"
          }
        ]
      }
      ```

2 - The Control Tower lifecycle event for the created account will trigger the Lambda and you will receive a notification on Slack when it's done.

#### You can simulate an account creation event creating a test for you Lambda using a json sample found [here](https://docs.aws.amazon.com/controltower/latest/userguide/lifecycle-events.html).

![Demo](https://user-images.githubusercontent.com/34891953/180902974-afdead4d-5c58-41fb-b59b-49caaec06926.png)
