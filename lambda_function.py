from qualys import QualysClient
from handlers.aws import AWSConnectorHanlder
from notification.slack import SlackNotifier
from role_assignment import setup_iam
from botocore.exceptions import ClientError
import json

slack_notifier = SlackNotifier()
aws_connector_handler = AWSConnectorHanlder()
qualys_client = QualysClient(api_server_url="qualysapi.qg3.apps.qualys.com", notifier=slack_notifier)


def check_account_production(account_name):
    sufixes = ["prd", "prod", "production", "producao"]
    return account_name.split("-")[-1].lower() in sufixes


def lambda_handler(event, context):
    if event['detail']['serviceEventDetails']['createManagedAccountStatus']['state'] == 'SUCCEEDED':

        account_name = event['detail']['serviceEventDetails']['createManagedAccountStatus']['account']['accountName']
        account_id = event['detail']['serviceEventDetails']['createManagedAccountStatus']['account']['accountId']

        if not check_account_production(account_name):
            return

        try:
            response, connector_creation_status = qualys_client.create_aws_connector(account_name)

            if connector_creation_status:
                connector_as_dict = AWSConnectorHanlder.xml_to_dict(response.text)
                connector = AWSConnectorHanlder.dict_to_object(connector_as_dict)
                if len(connector) < 1:
                    qualys_client.delete_aws_connector(account_name)
                    lambda_handler(event, context)
                    return
                connector = connector[0]
                role_arn = setup_iam(
                    qualys_base_account_id=qualys_client.base_account_id,
                    external_id=connector.external_id,
                    account_id=account_id
                )
                response, connector_activation_status = qualys_client.activate_aws_connector(
                    connector_id=connector.id,
                    role_arn=role_arn
                )
                connector = qualys_client.get_aws_connector_by_name(connector.name)
                if connector_activation_status:
                    connector.arn = role_arn
                    print(role_arn)
                    qualys_client.notifier.send_message(
                        on_success=True,
                        account_name=account_name,
                        account_id=account_id,
                        connector=connector,
                        creation_result=connector_creation_status,
                        activation_result=connector_activation_status
                    )
                else:
                    qualys_client.delete_aws_connector(connector.name)
                    print(f"Not activated! {connector.name} connector was deleted.")
        except Exception as err:
            print(err)
            qualys_client.notifier.send_message(
                on_success=False,
                account_name=account_name,
                account_id=account_id,
                error_message=err
            )
