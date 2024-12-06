import datetime
import json

class DataLoadJobHelper:
    dataLoadJobId = None  # Class variable, assuming it's the same for all rows

    def __init__(self, config={}):
        """
        Initializes the DataLoadJob instance with configuration settings for attribute processing.

        :param config: Dictionary specifying which attribute are loop-specific, all other attributes are considered global.
                       Also any custom data type handling (optional) needed for particular attributes. Normally, attribute_datatype is used here.
                       Example:
                       config = {
                            "loopAttributes": ["0000Y"],
                            "dataTypeHandling": {
                                "0000X": int
                            }
                        }
        """
        self.globalAttributes = []  # List to store global attributes without specifiers
        self.loopAttributes = {}    # Dictionary to store loop-specific attributes by attribute_no and specifier
        self.config = config  # Store configuration for attribute handling

    def init(self, dataLoadJob):
        """Processes each item in dataLoadJob based on the configuration provided at initialization.
        
        Populates globalAttributes and loopAttributes based on attribute types and configurations.
        
        :param dataLoadJob: List of dictionaries, each representing a row from the database query.
        """
        # Check if dataLoadJob is empty and exit if so
        if len(dataLoadJob) == 0:
            print("Empty list")
            return

        # Set dataLoadJobId as a class variable if it's not already set
        if DataLoadJobHelper.dataLoadJobId is None:
            DataLoadJobHelper.dataLoadJobId = dataLoadJob[0]['data_load_job_id']
        
        for item in dataLoadJob:
            attributeNo = item['attribute_no']
            attributeSpecifier = item['attribute_specifier']
            attributeValue = item['attribute_value']
            attributeDataType = item['attribute_datatype']
            # Use version_valid_from if available, otherwise set a default timestamp
            versionValidFrom = item.get('version_valid_from', datetime.datetime(1970, 1, 1, 0, 0, 0))
            
            # Apply data type conversion if specified in config
            if attributeNo in self.config.get("dataTypeHandling", {}):
                attributeValue = self.config["dataTypeHandling"][attributeNo](attributeValue)
            else:
                attributeValue = self.__datatypeConverter(attributeDataType,attributeValue)

            # Determine if this attribute_no is global or loop-specific based on config
            if attributeNo not in self.config.get("loopAttributes", []) and attributeSpecifier is None:
                # Global attribute
                self.globalAttributes.append({
                    'data_load_job_id': DataLoadJobHelper.dataLoadJobId,
                    'attribute_no': attributeNo,
                    'attribute_specifier': attributeSpecifier,
                    'attribute_value': attributeValue
                })

            elif attributeNo in self.config.get("loopAttributes", []) and attributeSpecifier is not None:
                if attributeNo not in self.loopAttributes:
                    self.loopAttributes[attributeNo] = {}
                
                # Loop-specific attribute, organized by attributeSpecifier
                if attributeSpecifier not in self.loopAttributes:
                    self.loopAttributes[attributeNo][attributeSpecifier] = {
                        'data_load_job_id': DataLoadJobHelper.dataLoadJobId,
                        'attribute_no': attributeNo,
                        'attribute_specifier': attributeSpecifier,
                        'attribute_value': attributeValue,
                        'version_valid_from': versionValidFrom,
                        'data_load_job_still_open': True
                    }
        # Sort entries within each loop attribute by version_valid_from
        for attributeNo in self.loopAttributes:
            self.loopAttributes[attributeNo] = dict(sorted(
                self.loopAttributes[attributeNo].items(),
                key=lambda x: x[1]['version_valid_from']
            ))

    def __datatypeConverter(self,datatype,value):
        if datatype in ('int2','int4','int8'):
            return int(value)
        elif datatype in ('numeric'):
            return float(value)
        elif datatype in ('date'):
            return datetime.datetime.strptime(value,'%Y-%m-%d')
        elif datatype in ('timestamp'):
            return datetime.datetime.strptime(value,'%Y-%m-%dT%H:%M:%S.%f')
        elif datatype in ('timestamptz'):
            return datetime.datetime.strptime(value,'%Y-%m-%dT%H:%M:%S.%f%z')
        return str(value)
    def getValueFromGlobalAttributes(self, attributeNo, default=None):
        """
        Retrieves the value of a specific global attribute based on attributeNo.
        
        :param attributeNo: The attribute_no to search for in globalAttributes.
        :return: The attribute value if found; otherwise, None.
        """
        for attribute in self.globalAttributes:
            if attribute['attribute_no'] == attributeNo:
                return attribute['attribute_value']
        return default
    
    def getValuesFromLoopAttributes(self, attributeNo, default=None):
        """
        Retrieves a dictionary of all specifiers and their values for a given loop attribute.
        
        :param attributeNo: The attribute_no to search for in loopAttributes.
        :return: A dictionary mapping each attribute_specifier to its corresponding attribute_value.
        """
        for no, specifiers in self.loopAttributes.items():
            if no == attributeNo:
                res = {}
                for specifier, value in specifiers.items():
                    res[specifier] = value['attribute_value']
                return res
        return default
    
    def markAsOpen(self, attributeNo, attributeSpecifier, newAttributeValue):
        """
        Updates a loop attribute's value and marks it as open.

        :param attributeNo: The attribute number in loopAttributes.
        :param attributeSpecifier: The specific identifier for the loop attribute.
        :param newAttributeValue: The new value to set for the attribute.
        """
        self.loopAttributes[attributeNo][attributeSpecifier]['data_load_job_still_open'] = True
        self.loopAttributes[attributeNo][attributeSpecifier]['attribute_value'] = newAttributeValue

    def markAsDone(self, attributeNo, attributeSpecifier):
        """
        Marks a loop attribute's job part as closed.

        :param attributeNo: The attribute number in loopAttributes.
        :param attributeSpecifier: The specific identifier for the loop attribute.
        """
        self.loopAttributes[attributeNo][attributeSpecifier]['data_load_job_still_open'] = False

    def getOpenJobParts(self):
        """
        Retrieves a JSON list of all currently open job parts, including any global attributes.
        
        :return: A JSON string of open job parts.
        """
        openJobParts = []
        for attributeNo in self.loopAttributes.keys():
            for attributeSpecifier in self.loopAttributes[attributeNo].keys():
                if self.loopAttributes[attributeNo][attributeSpecifier]['data_load_job_still_open']:
                    openJobParts.append({
                        'data_load_job_id': DataLoadJobHelper.dataLoadJobId,
                        'attribute_no': attributeNo,
                        'attribute_specifier': attributeSpecifier,
                        'attribute_value': self.loopAttributes[attributeNo][attributeSpecifier]['attribute_value']
                    })
        if len(openJobParts) > 0:
            openJobParts = openJobParts + self.globalAttributes
        return json.dumps(openJobParts)
