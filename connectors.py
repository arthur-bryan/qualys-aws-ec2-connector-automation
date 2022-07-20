class AWSConnector:
    """
    Class that represents the AWS EC2 Connector on Qualys.

    Attributes:
        id (str): The AWS EC2 connector ID on Qualys.
        name (str): The name for AWS EC2 connector ID on Qualys.
        aws_account_id (str): The AWS Account ID which the connector is related.
        last_sync (str): The datetime of the last sync.
        last_error (str): The description of the last error.
        connector_state (str): The current state of the connector.
        type (str): The cloud provider. In this class, with always be 'AWS'.
        default_tags (str): json string containing the tags set at the connector (if there is some).
        disabled (str): Boolean value as string. Should be 'true' or 'false' depending on the state of the connector.
        is_gov_cloud_configured (str): Boolean value as str. 'true' if the account is governamental, 'false' otherwise.
        is_china_configured (str): Boolean value as str. 'true' if the account is chinese, 'false' otherwise.
        is_deleted (str): Boolean value as string. 'true' if the account was deleted, 'false' otherwise.
        arn (str): The role arn configured on the connector.
        external_id (str): The external ID of the connector, used when setting the Role on AWS.
        qualys_aws_accountid (str): ID for the AWS Account, but inside Qualys view.
        auth_record (str): str(authrecord)
        all_regions (str): Boolean as str. 'true' if the connector was configured to scan all regions, 'false' if not.

    """

    def __init__(self, id, name, awsaccountid, lastsync, lasterror, connectorstate, type, defaulttags, disabled,
                 isgovcloudconfigured, ischinaconfigured, isdeleted, arn, externalid, qualysawsaccountid, authrecord,
                 allregions):
        """
        The constructor method of the class. The arguments are the attributes.
        
        Args:
            id (str): The AWS EC2 connector ID on Qualys.
            name (str):  The name for AWS EC2 connector ID on Qualys.
            awsaccountid (str): The AWS Account ID which the connector is related.
            lastsync (str): The datetime of the last sync.
            lasterror (str): The description of the last error.
            connectorstate (str): The current state of the connector.
            type (str): The cloud provider. In this class, with always be 'AWS'.
            defaulttags (str): json string containing the tags set at the connector (if there is some).
            disabled (str): Boolean value as str. Should be 'true' or 'false' depending on the state of the connector.
            isgovcloudconfigured (str): Boolean value as str. 'true' if the account is governamental, 'false' otherwise.
            ischinaconfigured (str): Boolean value as str. 'true' if the account is chinese, 'false' otherwise.
            isdeleted (str): Boolean value as string. 'true' if the account was deleted, 'false' otherwise.
            arn (str): The role arn configured on the connector.
            externalid (str): The external ID of the connector, used when setting the Role on AWS.
            qualysawsaccountid (str): ID for the AWS Account, but inside Qualys view.
            authrecord (str): str(authrecord)
            allregions (str): Boolean as str. true if the connector was configured to scan all regions, 'false' if not.

        """
        self.id = str(id)
        self.name = str(name)
        self.aws_account_id = str(awsaccountid)
        self.last_sync = str(lastsync)
        self.last_error = str(lasterror)
        self.connector_state = str(connectorstate)
        self.type = str(type)
        self.default_tags = str(defaulttags)
        self.disabled = str(disabled)
        self.is_gov_cloud_configured = str(isgovcloudconfigured)
        self.is_china_configured = str(ischinaconfigured)
        self.is_deleted = str(isdeleted)
        self.arn = str(arn)
        self.external_id = str(externalid)
        self.qualys_aws_accountid = str(qualysawsaccountid)
        self.auth_record = str(authrecord)
        self.all_regions = str(allregions)

    def __repr__(self):
        """
        Real representation of the object.

        Returns:
            (str): The object representation, eg: AWSConnector(id, name, aws_account_id, last_sync, last_error...).

        """
        return f"{self.__class__.__name__}({self.id}, {self.name}, {self.aws_account_id}, {self.last_sync}," \
               f" {self.last_error}, {self.connector_state}, {self.type}, {self.default_tags}, {self.disabled}," \
               f"{self.is_gov_cloud_configured}, {self.is_china_configured}, {self.is_deleted}, {self.arn}," \
               f"{self.external_id}, {self.aws_account_id}, {self.auth_record}, {self.all_regions})"

    def __str__(self):
        """
        Human-readable string of the object. When using print(<connector_object>), the output will look like that.

        Returns:
            (str): A human-readable string, that shows each of the connector attributes better formated.

        """
        colum_width = 30
        fill_char = " "
        ljust = lambda text: text.ljust(colum_width, fill_char)
        return ljust("ID:") + ljust(self.id) + "\n" + \
               ljust("Name:") + ljust(self.name) + "\n" + \
               ljust("AWS account ID:") + ljust(self.aws_account_id) + "\n" + \
               ljust("Last sync:") + ljust(self.last_sync) + "\n" + \
               ljust("Last error:") + ljust(self.last_error) + "\n" + \
               ljust("Connector state:") + ljust(self.connector_state) + "\n" + \
               ljust("Type:") + ljust(self.type) + "\n" + \
               ljust("Default tags:") + ljust(self.default_tags) + "\n" + \
               ljust("Disabled:") + ljust(self.disabled) + "\n" + \
               ljust("Is Gov Cloud configured:") + ljust(self.is_gov_cloud_configured) + "\n" + \
               ljust("Is Chine configured:") + ljust(self.is_china_configured) + "\n" + \
               ljust("Is deleted:") + ljust(self.is_deleted) + "\n" + \
               ljust("ARN:") + ljust(self.arn) + "\n" + \
               ljust("External ID:") + ljust(self.external_id) + "\n" + \
               ljust("Qualys AWS account ID:") + ljust(self.qualys_aws_accountid) + "\n" + \
               ljust("Auth record:") + ljust(self.auth_record) + "\n" + \
               ljust("All regions:") + ljust(self.all_regions)
