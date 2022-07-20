from qualys import QualysClient
from connectors_handlers import AWSConnectorHanlder
from role_assignment import do_work


qualys_client = QualysClient("qualysapi.qg3.apps.qualys.com")
aws_connector_handler = AWSConnectorHanlder()


def check_account_production(account_name):
    sufixes = ["prd", "prod", "production", "producao"]
    return account_name.split("-")[-1] in sufixes

def lambda_handler(event, context):
    
    try:
        if event['detail']['serviceEventDetails']['createManagedAccountStatus']['state'] == 'SUCCEEDED':
            
            account_name = event['detail']['serviceEventDetails']['createManagedAccountStatus']['account']['accountName']
            account_id = event['detail']['serviceEventDetails']['createManagedAccountStatus']['account']['accountId']
            # if not check_account_production(account_name):
            #     return
            response, connector_creation_status = qualys_client.create_aws_connector(account_name.replace(' ', ' - '))
            if connector_creation_status:
                connector_as_dict = AWSConnectorHanlder.xml_to_dict(response.text)
                connector = AWSConnectorHanlder.dict_to_object(connector_as_dict)[0]
                role_arn = do_work(account_id, connector.external_id)
                qualys_client.activate_aws_connector(connector.id, role_arn)
                # qualys_client.send_to_slack(connector_name=connector.name,
                #                             connector_id=connector.id,
                #                             account_name=account_name,
                #                             account_id=account_id)
    except Exception as err:
        print(err)
        #qualys_client.send_to_slack(connector_name="ERROR",
        #                            connector_id = "ERROR",
        #                            account_name="ERROR",
        #                            account_id="ERROR")