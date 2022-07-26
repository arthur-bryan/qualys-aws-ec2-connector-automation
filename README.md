[![Codacy Badge](https://app.codacy.com/project/badge/Grade/37b7c1b20a32415ba522a79505bdd9bd)](https://www.codacy.com/gh/arthur-bryan/qualys-aws-ec2-connector-automation/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=arthur-bryan/qualys-aws-ec2-connector-automation&amp;utm_campaign=Badge_Grade)
[![Open Source](https://img.shields.io/badge/Open%20Source-05C230?logo=Github&logoColor=white&link=https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation)](https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation)
[![Status Badge](https://img.shields.io/badge/status-development-05C230)](https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation/tree/dev)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/arthur-bryan/qualys-aws-ec2-connector-automation?color=05C230)
[![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/arthur-bryan/qualys-aws-ec2-connector-automation?color=05C230)](https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation/tags)
[![Python Badge](https://img.shields.io/badge/-Python-05C230?logo=Python&logoColor=white&link=https://www.python.org/)](https://github.com/arthur-bryan?tab=repositories&q=&type=&language=python)
![GitHub repo size](https://img.shields.io/github/repo-size/arthur-bryan/qualys-aws-ec2-connector-automation?color=05C230)

# :octocat: qualys-aws-ec2-connector-automation
Code for AWS Lambda Function which is triggered by a Control Tower lifecycle acount creation event.
The function creates an AWS EC2 Connector on Qualys, for each created account and enble it on Cloud View.
The lambda must be at your Management Account.

-   :heavy_check_mark: Automatic creation of Qualys AWS EC2 Connector when creating AWS accounts with Control Tower
-   :heavy_check_mark: Receive notifications on Slack

## :hammer_and_wrench: Setup
1 - Clone the repository.
```sh
git clone https://github.com/arthur-bryan/qualys-aws-ec2-connector-automation
cd qualys-aws-ec2-connector-automation
```

2 - Install the requirements to a folder and zip it.
```sh
pip install --target ./dependencies -r requirements.txt
zip -r dependencies.zip dependencies
```

3 - Create a layer at the AWS management account for you Lambda using the zip file with de requirements.

4 - Zip the source code.
```sh
zip -r qualys-aws-ec2-connector-automation.zip qualys-aws-ec2-connector-automation
```

5 - Create the AWS Lambda function using the zipped source.

6 - At the Lambda configuration, edit the timeout (recomended 1:30 minutes).

7 - Set the required environment variables for the Lambda Function.
- QUALYS_API_PASSWORD   # User with manager permissions on Qualys
- QUALYS_API_USER  # Password for the manager use to use the API
- QUALYS_BASE_ACCOUNT_ID   # Can be found at the portal if you have created a connector already
- SLACK_TEST_CHANNEL_WEBHOOK_URL # Webhook URL for posting notifications to your Slack channel

8 - Create a Role to allow your Lambda to assume roles.

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

2 - The Control Tower lifecycle event for the created accout will trigger the Lambda and you will receive a notification on Slack when it's done.

#### You can simulate an account creation event creating a test for you Lambda using a json sample found [here](https://docs.aws.amazon.com/controltower/latest/userguide/lifecycle-events.html).

![Demo](https://user-images.githubusercontent.com/34891953/180902974-afdead4d-5c58-41fb-b59b-49caaec06926.png)
