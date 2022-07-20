import json


def assemble_slack_message(connector_name, connector_id, account_name, account_id):
    mention_user = "<@U02744RQFTN>"
    message_body = {
        "text": "Assets Without Qualys",
        "blocks":
            [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": f":qualys-logo: {connector_name} - Qualys EC2 Connector was created"
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
                                    "text": f"*Account Name:*\n{account_name}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f'*Account ID:*\n{account_id}'
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Connector Name:*\n{connector_name}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Connector ID:*\n{connector_id}"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "fields": [
                                {
                                    "type": "mrkdwn",
                                    "text": f"*Notify:*\n{mention_user}"
                                },
                                {
                                    "type": "mrkdwn",
                                    "text": "*Observation:*\nPlease, validate if connector was activated"
                                }
                            ]
                        }
                    ]
                }
            ]
    }
    return message_body
