class AWSConnector:
    def __init__(self, id, name, awsaccountid, lastsync, lasterror, connectorstate, type, defaulttags, disabled,
                 isgovcloudconfigured, ischinaconfigured, isdeleted, arn, externalid, qualysawsaccountid, authrecord,
                 allregions):
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
        return f"{self.__class__.__name__}({self.id}, {self.name}, {self.aws_account_id}, {self.last_sync}," \
               f" {self.last_error}, {self.connector_state}, {self.type}, {self.default_tags}, {self.disabled}," \
               f"{self.is_gov_cloud_configured}, {self.is_china_configured}, {self.is_deleted}, {self.arn}," \
               f"{self.external_id}, {self.aws_account_id}, {self.auth_record}, {self.all_regions})"

    def __str__(self):
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
