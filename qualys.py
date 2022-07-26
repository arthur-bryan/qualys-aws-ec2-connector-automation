from handlers.aws import AWSConnectorHanlder
from botocore.vendored import requests
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
        __auth_credentials (str): base64 formated user+password used to consume Qualys API.
        __asset_management_endpoint (str): URL for Qualys the asset management API.
    """

    def __init__(self, api_server_url, notifier, protocol="https"):
        """
        Constructor method of class Qualys.

        Args:
            api_server_url (str):  The API server URL that you should use for API requests. Depends on the platform
             where your Qualys account is located.
            protocol (str): WEB protocol used in the communication. Defaults to 'https'.
        """
        try:
            self.__user_name = os.environ["QUALYS_API_USER"]
            self.__user_pass = os.environ["QUALYS_API_PASSWORD"]
            self.__base_account_id = os.environ["QUALYS_BASE_ACCOUNT_ID"]
            self.__auth_credentials = base64.b64encode(f"{self.__user_name}:{self.__user_pass}".encode()).decode()
        except KeyError:
            raise QualysClientError("API credentials was not set on environment variables!")
        self.__api_server_url = api_server_url
        self.__protocol = protocol
        self.__notifier = notifier
        self.__asset_management_endpoint = "qps/rest/3.0/search/am"

    @property
    def base_account_id(self):
        """
        Read-only property. Returns the Qualys Base Account ID, used to create the Role on the created account.

        Returns:
            self.__base_account_id (str): Qualys Base Account ID
        """
        return self.__base_account_id

    @property
    def notifier(self):
        """
        Read-only property. Returns the Notifier object, used to send notifications.

        Returns:
            self.__base_account_id (str): Qualys Base Account ID
        """
        return self.__notifier

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

    def get_aws_connectors(self):
        """
        Get all the created connectors.

        Returns:
            response (request.Response): XML containing the data of the all created connectors.
        """
        headers = {
            'content-type': 'text/xml',
        }
        data = ""
        object_category = "awsassetdataconnector"
        response = self.__make_basic_post_request(self.__asset_management_endpoint, object_category, headers, data)
        return response

    def get_aws_connector_by_name(self, connector_name):
        """
        Get an AWS EC2 Connector by its name. The method first get all connectors then iterate over them till find the
         requested and returns it.

        Args:
            connector_name: The name of the Connector.

        Returns:
            connector (request.Response): XML containing the data about the found connector. None if no connector with
             especified name was found.
        """
        all_connectors = self.get_aws_connectors().text
        connectors_as_dict = AWSConnectorHanlder.xml_to_dict(all_connectors)
        connectors_as_object = AWSConnectorHanlder.dict_to_object(connectors_as_dict)
        for connector in connectors_as_object:
            if connector.name == connector_name:
                return connector
        return None

    def create_aws_connector(self, connector_name):
        """
        Create an AWS EC2 Connector. By default, the connector will be in disabled state. To active, call the
         activate_aws_connector method.

        Args:
            connector_name (str): The name of the connector to be created.

        Returns:
            (response (response.Response), status (bool)) (tuple): Tuple containing the response object of the request
              and a boolean value based on the status code (true if 200, false otherwise).
        """
        headers = {
            'Content-type': 'text/xml',
        }

        api_endpoint = "qps/rest/2.0/create/am"
        object_category = "awsassetdataconnector"
        connector_creation_xml_data = AWSConnectorHanlder.handle_connector_creation_xml(connector_name)
        response = self.__make_basic_post_request(endpoint=api_endpoint,
                                                  object_category=object_category,
                                                  headers=headers,
                                                  data=connector_creation_xml_data)
        status = True if response.status_code == 200 else False
        return response, status

    def activate_aws_connector(self, connector_id, role_arn):
        """
        Activate the Connector and sets the use for Cloud View. The connector must be created already.

        Args:
            connector_id (str): ID for the created connector.
            role_arn (str): ARN for the role existing in the created accout for Qualys to assume.

        Returns:
            (response (response.Response), status (bool)) (tuple): Tuple containing the response object of the request
              and a boolean value based on the status code (true if 200, false otherwise).

        """
        headers = {
            'Content-type': 'text/xml',
        }

        api_endpoint = "qps/rest/2.0/update/am"
        object_category = "awsassetdataconnector"
        activation_xml = AWSConnectorHanlder.handle_connector_activation_xml(role_arn)
        response = self.__make_basic_post_request(endpoint=api_endpoint,
                                                  object_category=f"{object_category}/{connector_id}",
                                                  headers=headers,
                                                  data=activation_xml)
        status = True if response.status_code == 200 else False
        return response, status

    def delete_aws_connector(self, connector_name):
        """Deletes a Qualys AWS EC2 connector by name.

        Args:
            connector_name (str): Name of the connector to be removed.

        Returns:
            response.Response: the response object of the request.

        """

        headers = {
            'Content-type': 'text/xml',
        }

        deletion_xml = AWSConnectorHanlder.handle_connector_deletion_xml(connector_name)
        api_endpoint = "qps/rest/2.0/delete/am"
        object_category = "awsassetdataconnector"
        response = self.__make_basic_post_request(endpoint=api_endpoint,
                                                  object_category=object_category,
                                                  headers=headers,
                                                  data=deletion_xml)
        return response
