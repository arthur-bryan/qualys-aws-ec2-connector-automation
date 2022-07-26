from botocore.vendored import requests
import os
import json


class SlackNotifier:

    def __init__(self):
        self.__webhook_url = os.environ["SLACK_TEST_CHANNEL_WEBHOOK_URL"]

    def send_message(self, **kwargs):
        """
        Calls a function passing the name and ID for the created account and the related connector.
        The function will format the Slack mesage contet, then, the result will be sent to the Slack webhook url.

        Args:
            kwargs (dict): Arguments used to format the message that will be sent to Slack.
        """

        request_headers = {
            "Content-Type": "application/json",
        }

        slack_message = self.assemble_message(kwargs)
        data = json.dumps(slack_message)
        requests.post(url=self.__webhook_url, headers=request_headers, data=data)

    @staticmethod
    def assemble_message(kwargs):
        """
        This method prepares the message to be sent to Slack.

        Args:
            **kwargs: The arguments that will be used to format the Slack message.

        Returns:

        """
        status_map = {
            True: "Success",
            False: "Failed"
        }

        if not kwargs['on_success']:
            message_body = {
                "text": "Qualys AWS EC2 Creation",
                "blocks":
                [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": ":qualys-logo: Qualys AWS EC2 Connector creation"
                        }
                    }
                ],
                "attachments":
                [
                    {
                        "color": "#3b9cff",
                        "blocks":
                            [
                                {
                                    "type": "section",
                                    "fields": [
                                        {
                                            "type": "mrkdwn",
                                            "text": f"*Account Name:*\n{kwargs['account_name']}"
                                        },
                                        {
                                            "type": "mrkdwn",
                                            "text": f"*Account ID:*\n{kwargs['account_id']}"
                                        }
                                    ]
                                },
                                {
                                    "type": "section",
                                    "fields": [
                                        {
                                            "type": "mrkdwn",
                                            "text": "*Error message:*"
                                        },
                                        {
                                            "type": "mrkdwn",
                                            "text": f"{kwargs['error_message']}"
                                        }
                                    ]
                                }
                            ]
                    }
                ]
            }
        else:
            message_body = {
                "text": "Qualys AWS EC2 Creation",
                "blocks":
                    [
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": ":qualys-logo: Qualys AWS EC2 Connector creation"
                            }
                        }
                    ],
                "attachments":
                    [
                        {
                            "color": "#3b9cff",
                            "blocks":
                                [
                                    {
                                        "type": "section",
                                        "fields": [
                                            {
                                                "type": "mrkdwn",
                                                "text": f"*Account Name:*\n{kwargs['account_name']}"
                                            },
                                            {
                                                "type": "mrkdwn",
                                                "text": f"*Account ID:*\n{kwargs['account_id']}"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "section",
                                        "fields": [
                                            {
                                                "type": "mrkdwn",
                                                "text": f"*Connector Name:*\n{kwargs['connector'].name}"
                                            },
                                            {
                                                "type": "mrkdwn",
                                                "text": f"*Connector State:*\n{kwargs['connector'].connector_state}"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "section",
                                        "fields": [
                                            {
                                                "type": "mrkdwn",
                                                "text": f"*Creation Result:*\n{status_map[kwargs['creation_result']]}"
                                            },
                                            {
                                                "type": "mrkdwn",
                                                "text": f"*Activation Result:*\n{status_map[kwargs['activation_result']]}"
                                            }
                                        ]
                                    }
                                ]
                        }
                    ]
            }
        return message_body
