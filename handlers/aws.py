from connectors.aws import AWSConnector
import xml.etree.ElementTree as ET


class AWSConnectorHanlder:

    def __init__(self):
        pass

    @staticmethod
    def xml_to_dict(connectors_as_xml):
        all_connectors = []
        tree = ET.ElementTree(ET.fromstring(connectors_as_xml))
        root = tree.getroot()
        for connector in root.findall('.//AwsAssetDataConnector'):
            connector_as_dict = {
                "id": connector.find("id").text,
                "name": connector.find("name").text,
                "awsAccountId": connector.find("awsAccountId").text if connector.find("awsAccountId") else None,
                "lastSync": connector.find("lastSync").text if connector.find("lastSync") else None,
                "lastError": connector.find("lastError").text if connector.find("lastError") else None,
                "connectorState": connector.find("connectorState").text,
                "type": connector.find("type").text,
                "defaultTags": {
                    "list": {
                        "TagSimple": {
                            "id": connector.find("defaultTags/list/TagSimple/id").text,
                            "name": connector.find("defaultTags/list/TagSimple/name").text
                        }
                    }
                } if connector.find("defaultTags") else None,
                "disabled": connector.find("disabled").text,
                "isGovCloudConfigured": connector.find("isGovCloudConfigured").text,
                "isChinaConfigured": connector.find("isChinaConfigured").text,
                "isDeleted": connector.find("isDeleted").text if connector.find("isDeleted") else None,
                "arn": connector.find("arn").text if connector.find("arn") else None,
                "externalId": connector.find("externalId").text,
                "qualysAwsAccountId": connector.find("qualysAwsAccountId").text if connector.find("qualysAwsAccountId") else None,
                "authRecord": connector.find("authRecord").text if connector.find("authRecord") else None,
                "allRegions": connector.find("allRegions").text
            }
            all_connectors.append(connector_as_dict)
        return all_connectors

    @staticmethod
    def dict_to_object(connectors_dicts: list):
        all_connectors = []
        for dictionary in connectors_dicts:
            connector = AWSConnector(id=dictionary["id"], name=dictionary["name"],
                                     awsaccountid=dictionary["awsAccountId"],
                                     lastsync=dictionary["lastSync"], lasterror=dictionary["lastError"],
                                     connectorstate=dictionary["connectorState"], type=dictionary["type"],
                                     defaulttags=dictionary["defaultTags"], disabled=dictionary["disabled"],
                                     isgovcloudconfigured=dictionary["isGovCloudConfigured"],
                                     ischinaconfigured=dictionary["isChinaConfigured"],
                                     isdeleted=dictionary["isDeleted"], arn=dictionary["arn"],
                                     externalid=dictionary["externalId"],
                                     qualysawsaccountid=dictionary["qualysAwsAccountId"],
                                     authrecord=dictionary["authRecord"],
                                     allregions=dictionary["allRegions"])
            all_connectors.append(connector)
        return all_connectors

    @staticmethod
    def handle_connector_creation_xml(connector_name):
        creation_xml_file_name = "xml/connectors/create_aws_connector.xml"
        creation_xml_file = open(creation_xml_file_name)
        create_connector_xml_data = str(creation_xml_file.read())
        create_connector_xml_string = create_connector_xml_data.replace("connector_name", connector_name)
        return create_connector_xml_string

    @staticmethod
    def handle_connector_activation_xml(role_arn):
        activation_xml_file_name = "xml/connectors/activate_aws_connector.xml"
        activation_xml_file = open(activation_xml_file_name)
        activate_connector_xml_data = str(activation_xml_file.read())
        activate_connector_xml_string = activate_connector_xml_data.replace("disabled_state", "false")
        activate_connector_xml_string = activate_connector_xml_string.replace("role_arn", role_arn)
        return activate_connector_xml_string

    @staticmethod
    def handle_connector_deletion_xml(connector_name):
        deletion_xml_file_name = "xml/connectors/delete_aws_connector.xml"
        deletion_xml_file = open(deletion_xml_file_name)
        deletion_connector_xml_data = str(deletion_xml_file.read())
        deletion_connector_xml_string = deletion_connector_xml_data.replace("connector_name", connector_name)
        return deletion_connector_xml_string
