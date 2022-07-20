from connectors_handlers import AWSConnectorHanlder
from botocore.vendored import requests
from slack_handler import assemble_slack_message
import base64
import json
import os


class QualysClientError(Exception):
    pass


class QualysClient:
    """
    Class that represents the Qualys client.

    Attributes:
        __user_name (str): username used to consume Qualys API.
        __user_pass (str): password used by user to login.
        auth_credentials (str): base64 formated user+password used to consume Qualys API.
        vm_api_endpoint (str): URL for Qualys VM/PC module API.
        knowledge_base_api_endpoint (str): URL for Qualys the knowledge base API.
        asset_management_endpoint (str): URL for Qualys the asset management API.
    """

    def __init__(self, api_server_url, protocol="https"):
        """
        Constructor method of class Qualys.

        Args:
            api_server_url (str):  The API server URL that you should use for API requests. Depends on the platform
             where your Qualys account is located.
            protocol (str): WEB protocol used in the communication. Defaults to 'https'.
        """
        # self.vm_api_endpoint = "/api/2.0/fo/asset/host/vm/detection/"
        # self.knowledge_base_api_endpoint = "/api/2.0/fo/knowledge_base/vuln/"
        # self.asset_management_endpoint = "/qps/rest/2.0/search/am/hostasset"
        try:
            self.__user_name = os.environ["QUALYS_API_USER"]
            self.__user_pass = os.environ["QUALYS_API_PASSWORD"]
            self.__slack_webhook_url = os.environ["SLACK_TEST_CHANNEL_WEBHOOK_URL"]
            self.auth_credentials = base64.b64encode(f"{self.__user_name}:{self.__user_pass}".encode()).decode()
        except KeyError:
            raise QualysClientError("API credentials was not set on environment variables!")
        self.__api_server_url = api_server_url
        self.__protocol = protocol
        self.vm_api_endpoint = "api/2.0/fo/asset/host/vm"
        self.knowledge_base_api_endpoint = "api/2.0/fo/knowledge_base"
        self.asset_management_endpoint = "qps/rest/3.0/search/am"
        self.cloud_view_endpoint = "cloudviewapi/rest/v1"

    def __make_get_request(self, payload: dict, endpoint: str, object_category: str):
        """
        Makes a GET request to the API endpoint, passing the payload as parameter, then return the response.

        Args:
            payload: dict containing the query data used to make the request.
            endpoint: the API URL that will receive de request.
            object_category (str): the category of the item, eg: 'assetdataconnector' or 'hostasset'.

        Returns:
             response: request response XML data.
        """
        request_headers = {
            "Content-Type": "text/xml",
            "X-Requested-With": "DockQualysAPIClient",
            "Authorization": "Basic " + self.auth_credentials
        }
        response = requests.request("GET", endpoint, headers=request_headers, data=payload)
        return response

    def __make_basic_get_request(self, endpoint: str, params, object_category: str):
        """
        Makes a GET request to the API endpoint, passing the payload as parameter, then return the response.

        Args:
            endpoint: the API URL that will receive de request.
            params: dict containing the get paremeters
            object_category (str): the category of the item, eg: 'assetdataconnector' or 'hostasset'.

        Returns:
             response: request response XML data.
        """
        full_url = f"{self.__protocol}://{self.__api_server_url}/{endpoint}/{object_category}"
        response = requests.get(url=full_url,
                                params=params,
                                verify=False,
                                auth=(self.__user_name, self.__user_pass))
        return response

    def __make_post_request(self, payload: dict, endpoint: str):
        """
        Makes a POST request to the API endpoint, passing the payload as parameter, then return the response.

        Args:
            payload: dict containing the query data used to make the request.
            endpoint: the API URL that will receive de request.

        Returns:
             response: request response XML data.
        """
        request_headers = {
            "Content-Type": "text/xml",
            "X-Requested-With": "DockQualysAPIClient",
            "Authorization": "Basic " + self.auth_credentials
        }
        response = requests.request("POST", endpoint, headers=request_headers, data=payload)
        return response

    def __make_basic_post_request(self, endpoint: str, object_category: str, headers: dict, data):
        """
        Makes a POST request to the API endpoint, passing the payload as parameter, then return the response.

        Args:
            endpoint: the API URL that will receive de request.
            object_category: the category of the item, eg: 'assetdataconnector' or 'hostasset'.

        Returns:
             response: request response XML data.
        """
        full_url = f"{self.__protocol}://{self.__api_server_url}/{endpoint}/{object_category}"
        response = requests.post(url=full_url,
                                 data=data,
                                 headers=headers,
                                 auth=(self.__user_name, self.__user_pass))
        return response

    def get_vuln_info_by_qid(self, qids: list):
        """
        Consume the API to get information about vulnerabilities using its QIDs.

        Args:
            qids: list containing the QIDs to get the info.

        Returns:
             response: request response XML data.
        """
        payload = {
            'action': 'list',
            'show_disabled_flag': '1',
            'details': 'All',
            'ids': ",".join(qids) if len(qids) > 1 else qids,
            'show_qid_change_log': '1',
            'show_supported_modules_info': '1',
            'show_pci_reasons': '1'
        }
        response = self.__make_post_request(payload, self.knowledge_base_api_endpoint)
        return response

    def get_vm_detections(self, query_payload: dict):
        """
        Consume the API to get vulnerability detections based on specifc queries.

        Args:
            query_payload: dictionary containing the data to use on the detection query.

        Returns:
             response: request response XML data.
        """
        response = self.__make_post_request(query_payload, self.vm_api_endpoint)
        return response

    def get_assets_by_tags(self):
        xml_filter = open("filter.xml", "r").read()
        data = {"data": xml_filter}
        response = self.__make_post_request(xml_filter, self.asset_management_endpoint)
        return response

    def get_aws_connectors(self):
        headers = {
            'content-type': 'text/xml',
        }
        data = ""
        object_category = "awsassetdataconnector"
        response = self.__make_basic_post_request(self.asset_management_endpoint, object_category, headers, data)
        return response
        
    def get_aws_connector_by_name(self, name):
        all_connectors = self.get_aws_connectors().text
        connectors_as_dict = AWSConnectorHanlder.xml_to_dict(all_connectors)
        connectors_as_object = AWSConnectorHanlder.dict_to_object(connectors_as_dict)
        for connector in connectors_as_object:
            if connector.name == name:
                return connector


    def create_aws_connector(self, name):
        headers = {
            'Content-type': 'text/xml',
        }

        api_endpoint = "qps/rest/2.0/create/am"
        object_category = "awsassetdataconnector"
        creation_xml = AWSConnectorHanlder.handle_connector_creation_xml(name)
        response = self.__make_basic_post_request(api_endpoint,
                                                  object_category,
                                                  headers,
                                                  data=creation_xml)
        status = True if response.status_code == 200 else False
        return response, status

    def activate_aws_connector(self, connector_id, role_arn):
        headers = {
            'Content-type': 'text/xml',
        }

        api_endpoint = "qps/rest/2.0/update/am"
        object_category = "awsassetdataconnector"
        activation_xml = AWSConnectorHanlder.handle_connector_activation_xml(role_arn)
        response = self.__make_basic_post_request(api_endpoint,
                                                  f"{object_category}/{connector_id}",
                                                  headers,
                                                  data=activation_xml)
        status = True if response.status_code == 200 else False
        return response, status

    def delete_aws_connector(self, connector_name):
        headers = {
            'Content-type': 'text/xml',
        }

        deletion_xml = AWSConnectorHanlder.handle_connector_deletion_xml(connector_name)
        api_endpoint = "qps/rest/2.0/delete/am"
        object_category = "awsassetdataconnector"
        response = self.__make_basic_post_request(api_endpoint,
                                                  object_category,
                                                  headers,
                                                  data=deletion_xml)
        return response

    def send_to_slack(self, connector_name, connector_id, account_name, account_id):
        request_headers = {
            "Content-Type": "application/json",
        }

        slack_message = assemble_slack_message(connector_name, connector_id,
                                               account_name, account_id)

        data = json.dumps(slack_message)
        response = requests.post(url=self.__slack_webhook_url, headers=request_headers, data=data)