import datetime
from distutils.util import strtobool
import time
from uuid import uuid4
from loguru import logger
from time import sleep
from typing import Union

import pandas as pd
import sys
import json
import os
import requests
import getpass
import warnings
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import OAuth2Error, BackendApplicationClient

from .fileimport import FileImport
from .automation import Automation
from .schedule import Schedule
from .programming import Programming
from .authorization import Authorization
from .email import Email

from .utils.ut import Utils, Structure, Defaults
from .utils.ut_log import LogUtils
from .utils.DeviceClient import DeviceClient
from .utils.ut_auth import AuthData
from .timeseries import TimeSeries


class TechStack():
    """
    Initializes a Seven2one TechStack client.

    Parameters:
    ----------
    host: str
        The host domain or ip address, e.g. 'app.organisation.com'
    client_id: str = None
        The client id belonging to the apps and specific for the system. If None, it needs to
        be entered interactively.
    service_account_name: str
        A techstack service account name. Leave blank to login interactively with user.
    service_account_secret: str = None
        The service account secret belonging to the service account and specific for the system. If None, it needs to
        be entered interactively.
    proxies: dict = None
        Provide one or more proxy addresses, e.g.: {'https':'159.98.7.123'} 
    usePorts: bool = False
        A developer feature: if True, ports with prefix '8' for a
        developer ComposeStack will be used.
    timeZone: str = None
        A time zone provided in IANA or isoformat (e.g. 'Europe/Berlin' or 'CET').
        Defaults to the local timezone. 
    dateTimeOffset: bool = True
        Choose, if a Timestamp should be displayed as time zone naive (dateTimeOffset = False) 
        or with Offset information. 
    raiseException: bool = False
        In default mode (False) exceptions will be avoided to provide better user experience.
        True is recommended in automated processes to avoid silent failures.
    copyGraphQLString: bool = False
        A developer feature: if True, with each method execution, 
        the graphQL string is copied to the clipboard (Windows only).

    Examples:
    >>> client = TechStack('app.orga.com/', client_id='...')
    >>> client = TechStack('app.orga.com/', client_id='...', service_account_name='my-service', service_account_secret='...')) 
    """

    def __init__(
        self,
        host: str,
        client_id: str = None,
        service_account_name: str = None,
        service_account_secret: str = None,
        proxies: dict = None,
        usePorts: bool = False,
        timeZone: str = None,
        dateTimeOffset: bool = True,
        raiseException: bool = False,
        copyGraphQLString: bool = False
    ) -> object:

        self.raiseException = raiseException
        warnings.filterwarnings(
            'ignore', message="The zone attribute is specific to pytz")

        loglevelLocal = os.getenv("LOGLEVEL", "WARNING")
        loglevelServer = os.getenv("LOGLEVEL_SERVER", "ERROR")
        logToServer = strtobool(os.getenv("LOG_TO_SERVER", 'True').lower())
        sessionId = str(uuid4())

        try:
            logger.remove()

            if loglevelLocal in ['DEBUG', 'TRACE']:
                logger_format = "{level:<10} {time} {module}.{function} {line}: {message}"
                logger_diagnose = True
                logger_backtrace = True
            else:
                logger_format = "{level:<10} {time} {message}"
                logger_diagnose = False
                logger_backtrace = False

            def stdout_log_filter(record):
                return record["level"].no < logger.level('ERROR').no

            logger.add(sys.stdout, format=logger_format, level=loglevelLocal, catch=True,
                       diagnose=logger_diagnose, backtrace=logger_backtrace, filter=stdout_log_filter)
            logger.add(sys.stderr, format=logger_format, level='ERROR',
                       catch=True, diagnose=logger_diagnose, backtrace=logger_backtrace)
        except:
            pass

        if os.name == 'nt':
            logger.debug('Detected Windows, enabling pyperclip')
        else:
            logger.debug(f"Detected platform: {os.name}")

        if usePorts == False:
            idP_url = f'https://authentik.{host}'
            dynEndpoint = f'https://{host}/dynamic-objects/graphql/'
            automationEndpoint = f'https://{host}/automation/graphql/'
            scheduleEndpoint = f'https://{host}/schedule/graphql/'
            programmingEndpoint = f'https://{host}/programming/graphql/'
            tsGatewayEndpoint = f'https://{host}/timeseries/graphql/'
            logEndpoint = f'https://{host}/logging/loki/api/v1/push'
            authzEndpoint = f'https://{host}/authz/graphql/'
            emailEndpoint = f'https://{host}/emailservice/Email'
        else:
            idP_url = f'http://{host}:8044'
            dynEndpoint = f'http://{host}:8050/graphql/'
            automationEndpoint = f'http://{host}:8120/graphql/'
            scheduleEndpoint = f'http://{host}:8130/graphql/'
            programmingEndpoint = f'http://{host}:8140/graphql/'
            tsGatewayEndpoint = f'http://{host}:8195/graphql/'
            logEndpoint = f'http://{host}:8175/loki/api/v1/push'
            authzEndpoint = f'http://{host}:8030/graphql/'
            emailEndpoint = f'http://{host}:8240/Email'

        if os.getenv("IDENDITYPROVIDER_URL") != None:
            idP_url = os.getenv("IDENDITYPROVIDER_URL")
        if os.getenv("DYNAMIC_OBJECTS_ENDPOINT") != None:
            dynEndpoint = os.getenv("DYNAMIC_OBJECTS_ENDPOINT")
        if os.getenv("AUTOMATION_ENDPOINT") != None:
            automationEndpoint = os.getenv("AUTOMATION_ENDPOINT")
        if os.getenv("SCHEDULE_ENDPOINT") != None:
            scheduleEndpoint = os.getenv("SCHEDULE_ENDPOINT")
        if os.getenv("PROGRAMMING_ENDPOINT") != None:
            programmingEndpoint = os.getenv("PROGRAMMING_ENDPOINT")
        if os.getenv("TIMESERIES_ENDPOINT") != None:
            tsGatewayEndpoint = os.getenv("TIMESERIES_ENDPOINT")
        if os.getenv("LOGGING_ENDPOINT") != None:
            logEndpoint = os.getenv("LOGGING_ENDPOINT")
        if os.getenv("AUTHORIZATION_ENDPOINT") != None:
            authzEndpoint = os.getenv("AUTHORIZATION_ENDPOINT")

        if usePorts == True:
            os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        token_endpoint = '/application/o/token/'
        token_url = f'{idP_url}{token_endpoint}'

        if client_id is None:
            client_id = getpass.getpass('Enter client id: ')

        if service_account_name is None and service_account_secret is None:
            device_endpoint = '/application/o/device/'
            response = requests.request("POST", f'{idP_url}{device_endpoint}', data=f'client_id={client_id}', headers={
                                        'Content-Type': 'application/x-www-form-urlencoded'})
            json_response = json.loads(response.text)
            device_code = json_response['device_code']
            print('Please go to %s and authorize access.' %
                json_response['verification_uri_complete'])
            device_client = DeviceClient(client_id=client_id)
            oauth = OAuth2Session(client=device_client)
            while True:
                try:
                    token = oauth.fetch_token(
                        token_url=token_url, code=device_code, include_client_id=True)
                    break
                except OAuth2Error as e:
                    if e.error == 'authorization_pending':
                        time.sleep(json_response['interval'])
                    else:
                        print(f'Authorization failed: {e.error}')
                        raise
        elif service_account_secret is None:
            service_account_secret = getpass.getpass('Enter secret: ')
        else:
            app_client = BackendApplicationClient(client_id=client_id)
            oauth = OAuth2Session(client=app_client)
            token = oauth.fetch_token(token_url=token_url, 
                                      client_id=client_id, 
                                      username=service_account_name, 
                                      password=service_account_secret)

        if token is None:
            raise Exception('Could not get token')

        auth_data = AuthData(client_id, token_url, token, service_account_name, service_account_secret)

        if logToServer:
            if os.getenv("LOG_SERVER") != None:
                logEndpoint = os.getenv("LOG_SERVER")
            LogUtils._init_logging(
                logEndpoint, auth_data, loglevelServer, sessionId)

        def getLocalTimeZone():
            local_now = datetime.datetime.utcnow().astimezone()
            return local_now.tzinfo.tzname(local_now)
        logger.info(json.dumps({
            "SessionId": sessionId,
            "Configuration": {
                "host": host,
                "usePorts": usePorts,
                "timeZone": timeZone,
                "dateTimeOffset": dateTimeOffset,
                "raiseException": raiseException,
                "copyGraphQLString": copyGraphQLString,
                "logLevel": loglevelLocal,
                "logToServer": logToServer,
                "logLevelServer": loglevelServer
            },
            "System": {
                "timeZone": getLocalTimeZone(),
                "pythonVersion": sys.version,
                "machineName": os.getenv("HOSTNAME"),
                "osName": os.name
            }
        }))
        self.endpoint = dynEndpoint
        self.proxies = proxies
        self.client = Utils._create_client(self, auth_data)
        self.scheme = self.client.introspection
        self.host = host
        self.auth_data = auth_data

        # Defaults:
        if timeZone is None:
            timeZone = Utils._timeZone('local')

        self.defaults = Defaults(
            useDateTimeOffset=dateTimeOffset,
            copyGraphQLString=copyGraphQLString,
            timeZone=timeZone
        )

        # Get scheme
        if self.scheme == None:
            graphQLString = Structure._introspectionQueryString()
            self.scheme = Utils._executeGraphQL(self, graphQLString)

        # Structures
        self.structure = Utils._executeGraphQL(self, Structure.queryStructure)
        self.structure = Structure._fullStructureDict(self.structure)
        self.objects = Structure._fullStructureNT(self.structure)
        self.inventory = Structure._inventoryNT(self.structure)
        self.inventoryProperty = Structure._inventoryPropertyNT(self.structure)

        # Initialize further gateways
        try:
            self.TimeSeries = TimeSeries(
                tsGatewayEndpoint, self, auth_data)
        except Exception as err:
            logger.warning(f"Time series gateway not available")
            logger.debug(f"Reason: {err}")

        try:
            self.Automation = Automation(
                automationEndpoint, self, auth_data)
        except Exception as err:
            logger.warning(f"Automation service not available")
            logger.debug(f"Reason: {err}")

        try:
            self.Schedule = Schedule(scheduleEndpoint, self, auth_data)
        except Exception as err:
            logger.warning(f"Schedule service not available")
            logger.debug(f"Reason: {err}")

        try:
            self.Programming = Programming(
                programmingEndpoint, self, auth_data)
        except Exception as err:
            logger.warning(f"Programming service not available")
            logger.debug(f"Reason: {err}")

        self.FileImport = FileImport(self)
        self.Authorization = Authorization(
            authzEndpoint, self, auth_data)
        self.Email = Email(emailEndpoint, self, auth_data)

        def getVersions():
            versions = [
                self.getVersion(),
                self.TimeSeries.getVersion(),
                self.Authorization.getVersion(),
                self.Automation.getVersion(),
                self.Schedule.getVersion(),
                self.Programming.getVersion()
            ]
            return versions
        logger.opt(lazy=True).debug("Service versions: {}", getVersions)

        return

    def getVersion(self):
        """
        Returns name and version of the responsible micro service
        """

        key = 'dynamicObjectsServiceInfo'
        graphQLString = f'''query version {{ 
            {key} {{
                name
                informationalVersion
            }}
        }}'''
        result = Utils._executeGraphQL(self, graphQLString)

        return f'{result[key]["name"]}: {result[key]["informationalVersion"]}'

    def updateClient(self) -> None:
        """
        Updates the client scheme and structures, e.g. after adding inventories
        or new inventory properties.
        """

        self.client = Utils._create_client(self, self.auth_data)
        graphQLString = Structure._introspectionQueryString()
        self.scheme = Utils._executeGraphQL(self, graphQLString)
        self.structure = Utils._executeGraphQL(self, Structure.queryStructure)
        self.structure = Structure._fullStructureDict(self.structure)
        self.objects = Structure._fullStructureNT(self.structure)
        self.inventory = Structure._inventoryNT(self.structure)
        self.inventoryProperty = Structure._inventoryPropertyNT(self.structure)
        # reninit relevant gateways
        self.TimeSeries = TimeSeries(
            self.TimeSeries.endpoint, self, self.auth_data)

        return

    def inventories(
        self,
        fields: list = None,
        where: str = None,
        orderBy: str = None,
        asc: bool = True
    ) -> pd.DataFrame:
        """
        Returns a DataFrame of existing inventories.

        Parameters:
        ----------
        fields: list=None
            The list of fields to be queried, e.g.
            ['name', 'inventoryId, variant.name']
        where: str=None
            Use a string to add where criteria like 'name eq "meterData"'.
            The argument is momentarily very limited.
        orderBy: str=None
            Select one field to sort by.
        asc: bool=True
            Determines the sort order of items. Set to False to apply descending order.

        Examples:
        >>> inventories()
        >>> inventories(fields=['name', 'inventoryId'], 
                where='city eq "Hamburg"', 
                orderBy='variant', asc=True)
        """

        if fields == None:
            fields = ['name', 'inventoryId', 'variant.name',
                      'historyEnabled', 'hasValidityPeriods', 'isDomainUserType']
            _fields = Utils._queryFields(fields, recursive=True)
        else:
            if type(fields) != list:
                fields = [fields]
            try:
                _fields = Utils._queryFields(fields, recursive=True)
            except:
                Utils._error(
                    self, "Fields must be provided as list, e.g. ['name', 'inventoryId, variant.name']")
                return

        topLevelWhere, _ = Utils._handleWhere(self, where)

        if orderBy != None:
            if asc != True:
                _orderBy = f'order: {{ {orderBy}: DESC }}'
            else:
                _orderBy = f'order: {{ {orderBy}: ASC }}'
        else:
            _orderBy = ''

        graphQLString = f'''query inventories {{
        inventories 
            (pageSize:1000 {_orderBy} {topLevelWhere})
            {{
            {_fields}
            }}
        }}
        '''
        result = Utils._executeGraphQL(self, graphQLString)
        if result == None:
            return

        df = pd.json_normalize(result['inventories'])
        return df

    def items(
        self,
        inventoryName:str, 
        references:bool=False, 
        fields:list=None,
        where:Union[list,tuple,str]=None, 
        orderBy:Union[dict,list,str]=None, 
        asc:Union[list,str]=True, 
        pageSize:int=5000, 
        arrayPageSize:int=50,
        top:int=100000,
        validityDate:str=None,
        allValidityPeriods:bool=False,
        includeSysProperties:bool=False,
        maxRecursionDepth=2
    ) -> pd.DataFrame:
        """
        Returns items of an inventory in a DataFrame.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        references: bool = False
            If True, items of referenced inventories will be added to the DataFrame. If
            the fields-parameter is used, this parameter is ignored.
        fields: list | str = None
            A list of all properties to be queried. If None, all properties will be queried.
            For referenced items use a '.' between inventory name and property.
            Optional property 'sys_revision': Returns number of updates of an item.
        where: list | tuple | str = None
            Define arguments critera like  'city eq "Berlin" and use lists for AND-combinations and
            tuples for OR-combinations. For references use the format inventory.property as 
            filter criteria.
        orderBy: dict | list | str = None
            Use a dict in the form of {property:'ASC'|'DESC'} or 
            use a list of properties and the asc-argument for sorting direction
        asc: list | bool = True
            Determines the sort order of items. If set to False, a descending order 
            is applied. Use a list, if more properties are selected in orderBy.
        pageSize: int = 5000
            The page size of items that is used to retrieve a large number of items.
        arrayPageSize: int = 50
            The page size of list items that is used to page list items in an inventory item.
        top: int = None
            Returns a restricted set of items oriented at the latest entries.
        includeSysProperties: bool = False
            If True, all system properties available will be queried. If False, 
            only 'sys_inventoryItemId' will be queried by default. Despite of that, any system 
            property can be passed to the fields argument as well.
        validityDate: str = None
            If the queried inventory has validity periods enabled, only items will be returned, 
            which have the given timestamp between sys_validTo and sys_validFrom. Items without
            validity periods are shown as well.
        allValidityPeriods: bool = False
            If True and if the queried inventory has validity periods enabled, all validity 
            periods will be returned. If False, items with validity dates will not be returned.
        maxRecursionDepth: int = 2
            Maximum recursion level following the references to other inventories.

        Example:
        --------
        >>> items('appartments', references=True)
        >>> items(
                'appartments',
                fields=['address', 'owner', 'sys_revision'],
                where=['city == "Berlin"', 'rooms > 2'],
                orderBy={'size':'DESC', price:'ASC'}
                )
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            if inventoryName not in self.inventory:
                Utils._error(self, f"'{inventoryName}' does not exist.")
                return

            # where
            try:
                topLevelWhere, resolvedFilterDict = Utils._handleWhere(
                    self, where, inventoryName)
            except:
                return

            validityDate = Utils._argNone('validityDate', validityDate)
            allValidityPeriods = Utils._argNone(
                'allValidityPeriods', allValidityPeriods)

            # core
            deleteId = False
            propertyDict = Utils._properties(self.scheme, inventoryName, recursive=True,
                sysProperties=includeSysProperties, maxRecursionDepth=maxRecursionDepth)
            if fields != None:
                if type(fields) != list:
                    fields = [fields]
                if 'sys_inventoryItemId' not in fields:
                    deleteId = True
                    fields += ['sys_inventoryItemId']
                _fields = Utils._queryFields(fields, propertyDict['arrayTypeFields'], arrayPageSize,
                                             filter=resolvedFilterDict, recursive=True)
            else:
                properties = Utils._propertyList(
                    propertyDict['properties'], recursive=references)
                _fields = Utils._queryFields(properties, propertyDict['arrayTypeFields'],
                                             arrayPageSize, filter=resolvedFilterDict, recursive=references)
            logger.debug(f"Fields: {_fields}")

            if len(_fields) == 0:
                Utils._error(self, f"Inventory '{inventoryName}' not found.")
                return

            order = Utils._orderItems(self, orderBy, asc)
            if order == None:
                return

            result = []
            count = 0
            stop = False
            lastId = ''

            while True:

                # Handling top (premature stop)
                if top != None:
                    loadedItems = pageSize * count
                    if top - loadedItems <= pageSize:
                        stop = True
                        pageSize = top - loadedItems

                graphQLString = f''' query getItems {{
                        {inventoryName} (
                                pageSize: {pageSize}
                                {order}
                                {allValidityPeriods}
                                {validityDate}
                                {lastId}
                                {topLevelWhere}
                                ) {{
                            {_fields}
                        }}
                    }}
                    '''

                _result = Utils._executeGraphQL(
                    self, graphQLString, correlationId)

                if _result[inventoryName]:
                    result += _result[inventoryName]
                    count += 1
                try:
                    cursor = _result[inventoryName][-1]['sys_inventoryItemId']
                    lastId = f'lastId: "{cursor}"'
                except:
                    break

                if stop == True:
                    break

            df = pd.json_normalize(result)

            nested_columns = [col for col in df.columns if "." in col]
            if nested_columns:
                base_property_names = [col.split('.')[0] for col in nested_columns]
                subset_columns = [col for col in df.columns if col not in base_property_names]
                df = df[subset_columns]
        
            if fields != None: #sorts dataframe according to given fields
                try: # for array field this does not work
                    df = df[fields]
                except:
                    pass
            if deleteId:
                try:
                    del df['sys_inventoryItemId']
                except:
                    pass

            return df

    def inventoryProperties(
        self,
        inventoryName,
        namesOnly=False
    ) -> pd.DataFrame:
        """
        Returns a DataFrame of a query of properties of an inventory.

        Parameters:
        ----------
        inventoryName : str
            The name of the inventory.
        namesOnly : bool
            If True, only property names will be returned

        Example:
        --------
        >>> inventoryProperties('appartments') 


        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            propertyFields = f'''
                name          
                ... Scalar
                isArray
                nullable
                ... Reference
                type
                propertyId
            '''

            graphQLString = f'''query Inventory {{
            inventory
                (inventoryName: "{inventoryName}")
                {{
                properties {{
                    {propertyFields}
                    }}
                }}
            }}
            fragment Scalar on IScalarProperty {{
                dataType
                }}
            fragment Reference on IReferenceProperty {{
                inventoryId
                inventoryName
            }}
            '''

            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result['inventory'] == None:
                Utils._error(self, f"Inventory '{inventoryName}' not found.")
                return

            df = pd.json_normalize(result['inventory']['properties'])

            if namesOnly == True:
                return list(df['name'])
            else:
                return df

    def propertyList(self, inventoryName, references=False, dataTypes=False, maxRecursionDepth=2):
        """
        Returns a list of properties of an inventory and its referenced inventories
        by reading out the scheme.

        Parameters:
        ----------
        inventoryName : str
            The name of the inventory.
        references : bool
            If True, properties of referenced inventories included.
        dataTypes : bool
            If True, result will be displayed as Series with properties as index and
            dataTypes as values.
        maxRecursionDepth: int = 2
            Maximum recursion level following the references to other inventories.

        Example:
        --------
        >>> propertyList('appartments') 

        """

        propertyDict = Utils._properties(self.scheme, inventoryName=inventoryName, recursive=references, maxRecursionDepth=maxRecursionDepth)

        if dataTypes == False:
            properties = Utils._propertyList(
                propertyDict['properties'], recursive=references)
        else:
            properties = pd.Series(
                Utils._propertyTypes(propertyDict['properties']))

        return properties

    def filterValues(
        self,
        inventoryName: str,
        top: int = 10000
    ) -> pd.DataFrame:
        """
        Returns a DataFrame of values that can be used in a where-string. 
        Only string data types are returned. 

        Parameters:
        ----------
        inventoryName : str
            The name of the inventory.
        top: int = None
            Uses a restricted set of items oriented at the latest entries to 
            provide a value set.

        Example:
        --------
        >>> filterValues('appartments') 

        """
        properties = self.propertyList(inventoryName, dataTypes=True)
        logger.debug(f"Properties: {properties}")

        propertyList = []
        for property, dataType in zip(properties.index, properties):
            if 'sys_' in property:
                continue
            if dataType != 'String':
                continue
            propertyList.append(property)
        logger.debug(f"PropertyList: {propertyList}")

        df = self.items(inventoryName, fields=propertyList, top=top)
        logger.debug(f"Used columns: {df.columns}")

        propertyValues = {}
        for property in propertyList:
            if 'sys_' in property:
                continue
            if len(set(df[property])) == len(df):
                continue
            propertySet = set(df[property])
            logger.debug(f"PropertySet: {propertySet}")
            try:
                propertySet.remove(None)
            except:
                pass
            propertyValues.setdefault(
                df[property].name, sorted(list(propertySet)))

        valuesDf = pd.DataFrame.from_dict(propertyValues, orient='index').T
        valuesDf.fillna(value='-', inplace=True)
        return valuesDf

    def __addItems(
        self,
        inventoryName: str,
        items: list
    ) -> str:
        """
        Adds from a list of dicts new items and returns a list
        of inventoryItemIds.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        items : list
            A list with dictionaries for each item.

        Example:
        --------
        >>> items = [
                {
                'meterId': '86IEDD99',
                'dateTime': '2020-01-01T05:50:59Z'
                },
                {
                'meterId': '45IXZ52',
                'dateTime': '2020-01-07T15:41:14Z'
                }
            ]
        >>> addItems('meterData', items)
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):

            items = Utils._propertiesToString(items)
            key = f'create{inventoryName}'

            graphQLString = f'''mutation addItems {{
                {key} (input: 
                    {items}
                )
                    {{
                        {Utils.errors}           
                    inventoryItems {{
                        sys_inventoryItemId
                    }}
                }}
            }} 
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
            return result[key]['inventoryItems']

    def addItems(
        self,
        inventoryName:str, 
        items:list,
        chunkSize:int = 5000, 
        pause:int = 1
        ) -> str:
        """
        Adds from a list of dicts new items and returns a list
        of inventoryItemIds.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        items : list
            A list with dictionaries for each item.
        chunkSize : int = 5000
            Determines the number of items which are written per chunk. Using chunks
            can be necessary to avoid overloading. Default is 5000 items per chunk.
        pause : int = 1
            Pause in seconds between each chunk upload to avoid overloading.

        Example:
        --------
        >>> items = [
                {
                'meterId': '86IEDD99',
                'dateTime': '2020-01-01T05:50:59Z'
                },
                {
                'meterId': '45IXZ52',
                'dateTime': '2020-01-07T15:41:14Z'
                }
            ]
        >>> addItems('meterData', items)        
        """
        
        correlationId = str(uuid4())
        result = []
        with logger.contextualize(correlation_id=correlationId):
            if len(items) > chunkSize:
                lenResult = 0
                for i in range(0, len(items), chunkSize):
                    result_object = self.__addItems(inventoryName, items[i : i + chunkSize])
                    if result_object != None:
                        result.extend(result_object)
                        lenResult = len(result)
                    logger.info(f"{lenResult} items of {len(items)} added. Waiting {pause} second(s) before continuing...")
                    sleep(pause)
            else:
                result = self.__addItems(inventoryName, items)
                logger.info(f"{len(result)} items added.")
        
        return result

    def __addValidityItemsToParents(
        self, 
        inventoryName:str, 
        items:list
    ) -> str:
        """
        Adds from a list of dicts items with validity periods to an existing parent items. 
        The 'sys_parentInventoryItemId' and either 'sys_validFrom' or 'sys_validFrom' are required
        system properties.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        items : list
            A list with dictionaries for each item.

        Example:
        --------
        >>> items = [
                {
                'meterId': '86IEDD99',
                'userId': 'DlvK5PCm4u',
                'sys_parentInventoryItemId': 'EaM9zHA8Mi',
                'sys_validFrom': '2023-12-31T23:00:00.000Z',
                'sys_validTo': '2024-06-30T23:00:00.000Z',
                },
                {
                'meterId': '86IEDD99',
                'userId': 'DlvK5PCm8i',
                'sys_parentInventoryItemId': 'EaM9zHA8Mi',
                'sys_validFrom': '2024-07-31T23:00:00.000Z',
                'sys_validTo': '2024-09-30T23:00:00.000Z',
                }
            ]
        >>> addValidityItemsToParents('meterData', items)
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            items = Utils._propertiesToString(items)
            key = f'create{inventoryName}ValidityPeriods'

            graphQLString = f'''mutation addValidityPeriodItemsToParents {{
                {key} (input: 
                    {items}
                )
                    {{
                        {Utils.errors}           
                    inventoryItems {{
                        sys_inventoryItemId
                        sys_versionId
                    }}
                }}
            }} 
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
            return result[key]['inventoryItems']

    def addValidityItemsToParents(
        self, 
        inventoryName:str, 
        items:list,
        chunkSize:int = 5000, 
        pause:int = 1
        ) -> str:
        """
        Adds from a list of dicts items with validity periods to an existing parent items. 
        The 'sys_parentInventoryItemId' and either 'sys_validFrom' or 'sys_validFrom' are required
        system properties.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        items : list
            A list with dictionaries for each item.
        chunkSize : int = 5000
            Determines the number of items which are written per chunk. Using chunks
            can be necessary to avoid overloading. Default is 5000 items per chunk.
        pause : int = 1
            Pause in seconds between each chunk upload to avoid overloading.

        Example:
        --------
        >>> items = [
                {
                'meterId': '86IEDD99',
                'userId': 'DlvK5PCm4u',
                'sys_parentInventoryItemId': 'EaM9zHA8Mi',
                'sys_validFrom': '2023-12-31T23:00:00.000Z',
                'sys_validTo': '2024-06-30T23:00:00.000Z',
                },
                {
                'meterId': '86IEDD99',
                'userId': 'DlvK5PCm8i',
                'sys_parentInventoryItemId': 'EaM9zHA8Mi',
                'sys_validFrom': '2024-07-31T23:00:00.000Z',
                'sys_validTo': '2024-09-30T23:00:00.000Z',
                }
            ]
        >>> addValidityItemsToParents('meterData', items)
        """

        correlationId = str(uuid4())
        result = []
        with logger.contextualize(correlation_id=correlationId):
            if len(items) > chunkSize:
                lenResult = 0
                for i in range(0, len(items), chunkSize):
                    result_object = self.__addValidityItemsToParents(inventoryName, items[i : i + chunkSize])
                    if result_object != None:
                        result.extend(result_object)
                        lenResult = len(result)
                    logger.info(f"{lenResult} validity items of {len(items)} added. Waiting {pause} second(s) before continuing...")
                    sleep(pause)
            else:
                result = self.__addValidityItemsToParents(inventoryName, items)
                logger.info(f"{len(result)} validity items added.")
        
        return result

    def updateItems(
        self,
        inventoryName: str,
        items: list
    ) -> None:
        """
        Updates from a list of dicts existing items. The 'sys_inventoryItemId'
        must be passed to each item.

        Parameters:
        -----------
        inventoryName : str
            The name of the inventory.
        items : list
            A list with dictionaries for each item.

        Example:
        --------
        >>> items = [
                {
                'sys_inventoryItemId':'118312438662692864',
                'meterId': '86IEDD99',
                'dateTime': '2020-01-01T05:50:59Z'
                },
                {
                'sys_inventoryItemId':'118312438662692864',
                'meterId': '45IXZ52',
                'dateTime': '2020-01-07T15:41:14Z'
                }
            ]
        >>> updateItems('meterData', items)
        """
        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            items = Utils._propertiesToString(items)
            key = f'update{inventoryName}'

            graphQLString = f'''mutation updateItems {{
                {key} (input: 
                    {items}
                )
                    {{
                        {Utils.errors}           
                        inventoryItems {{
                            sys_inventoryItemId
                    }}
                }}
            }}
            '''
            logger.trace(graphQLString)
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)

            logger.info(
                f"{len(result[key]['inventoryItems'])} item(s) updated.")
            return

    def updateDataFrameItems(
        self,
        inventoryName: str,
        dataFrame: pd.DataFrame,
        columns: list = None
    ) -> None:

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            def convertDfToDict(df: pd.DataFrame, timeSeries: bool, columns: list = None) -> dict:

                def createDict(df: pd.DataFrame) -> dict:
                    items = []
                    for _, row in df.iterrows():
                        item = {}
                        for header, value in zip(df.columns, row):
                            if not pd.isna(value):
                                item.setdefault(header, value)
                        items.append(item)
                    return items

                if timeSeries == True:
                    tsProperties = ['resolution', 'unit']
                    if columns == None:
                        columns = [
                            col for col in df.columns if col not in tsProperties]
                    else:
                        columns = [
                            col for col in columns if col not in tsProperties]

                if columns == None:
                    return createDict(df)
                else:
                    if 'sys_inventoryItemId' not in columns:
                        columns.append('sys_inventoryItemId')
                    return df[columns].to_dict('records', )

            if not 'sys_inventoryItemId' in dataFrame.columns:
                logger.error(
                    "Missing column 'sys_inventoryItemId'. Items cannot be updated without this information.")
                return

            if self.structure[inventoryName]['variant'] == None:
                items = convertDfToDict(dataFrame, False, columns=columns)
            elif self.structure[inventoryName]['variant']['name'] not in ['TimeSeries', 'TimeSeriesGroup']:
                items = convertDfToDict(dataFrame, False, columns=columns)
            else:
                items = convertDfToDict(dataFrame, True, columns=columns)

            logger.debug(f"Items to write {items[:3]}...")

            self.updateItems(inventoryName, items)
            return

    def createInventory(
        self,
        name: str,
        properties: list,
        variant: str = None,
        propertyUniqueness: dict = None,
        historyEnabled: bool = False,
        hasValitityPeriods: bool = False,
        isDomainUserType: bool = False
    ) -> str:
        """
        Creates a new inventory. After creation, access rights must be set to add items.

        Parameters:
        ----------
        name : str
            Name of the new inventory (only alphanumeric characters allowed, 
            may not begin with a number)
        properties : list
            A list of dicts with the following mandatory keys: 
                name: str
                dataType: enum (STRING, BOOLEAN, DECIMAL, INT, LONG, DATE_TIME, 
                DATE_TIME_OFFSET)
            Optional keys:
                isArray: bool (Default = False)
                nullable: bool (Default = True)
                isReference: bool (Default = False)
                inventoryId: str (mandatory if hasReference = True)
        variant : str
            The inventory variant.
        propertyUniqueness : list
            A list of properties that should be unique in its combination. 
        historyEnabled : bool
            If True, changes in properties will be recorded in item history.
        hasValidityPeriods : bool
            If true, a validity period can be added to the item.    

        Example:
        --------
        >>> propertyDefinitions = [
            {
                'name': 'street',
                'dataType': 'STRING',
                'nullable': False,
            },
            {
                'name': 'postCode',
                'dataType': 'STRING',
                'nullable': False,
            },
            ]
            uniqueness = [{'uniqueKey': 'address', 'properties': ['street', 'postCode']}
        >>> createInventory('appartment', 'propertyDefinitions', propertyUniqueness=uniqueness) 
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            _properties = Utils._propertiesToString(properties)

            if variant != None:
                _variantId = f'{Utils._getVariantId(self.variants(), variant)}'
                logger.debug(f"Found variantId: {_variantId}")
                if type(_variantId) != str:
                    Utils._error(self, f"Variant name '{name}' not found")
                    return

                _variant = f'variantId: "{_variantId}"'
            else:
                _variant = ''

            if propertyUniqueness != None:
                _propertyUniqueness = 'propertyUniqueness: ' + \
                    Utils._uniquenessToString(propertyUniqueness)
                logger.debug(_propertyUniqueness)
            else:
                _propertyUniqueness = ''

            _history = 'true' if historyEnabled != False else 'false'
            _validityPeriods = 'true' if hasValitityPeriods != False else 'false'
            _domainUser = 'true' if isDomainUserType != False else 'false'

            graphQLString = f'''
            mutation createInventory {{
                createInventory (input: {{
                    name: "{name}"        
                    properties: {_properties}
                    {_variant}
                    historyEnabled: {_history}
                    hasValidityPeriods: {_validityPeriods}
                    isDomainUserType: {_domainUser}
                    {_propertyUniqueness}
                    }})
                    {{
                    inventory {{
                        inventoryId
                        }}
                    {Utils.errors}           
                }}
            }}
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            if result['createInventory']['errors']:
                Utils._listGraphQlErrors(result, 'createInventory')
                return

            logger.info(f"New inventory {name} created.")

            if variant != None:
                self.TimeSeries.refreshSchema()

            return result['createInventory']['inventory']['inventoryId']

    def deleteInventories(
        self,
        inventoryNames: list,
        deleteWithData: bool = False,
        force: bool = False
    ) -> None:
        """ 
        Deletes one or more inventories with the possibility to delete containing data.

        Parameters:
        -----------
        inventoryNames : list
            A list of inventory names that should be deleted.
        deleteWithData : bool = False
            If True, containing data will be deleted.
        force : bool
            Use True to ignore confirmation.

        Example:
        ---------
        >>> deleteInventories(['meterData'], deleteWithData=True, force=True)
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            inventoryIds = []
            errorNames = []
            for name in inventoryNames:
                if deleteWithData and not self._isInventoryOfValidVariant(name):
                    Utils._error(self, f"TimeSeries inventory {name} cannot be deleted with option 'deleteWithData'.")
                    continue
                try:
                    inventoryIds.append(self.structure[name]['inventoryId'])
                except:
                    errorNames.append(name)

            if errorNames:
                Utils._error(self, f"Unknown inventory names '{errorNames}'.")
                return
            if len(inventoryIds) == 0:
                logger.info(f"No inventories to delete.")
                return

            _inventoryIds = Utils._graphQLList(inventoryIds)

            if force == False:
                confirm = input(f"Press 'y' to delete '{inventoryNames}': ")

            key = 'deleteInventory'
            graphQLString = f'''mutation deleteInventories {{
                {key} (input:
                    {{
                        inventoryIds: {_inventoryIds}
                        ignoreData: {Utils._toGraphQL(deleteWithData)}
                    }}
                )
                    {{
                        {Utils.errors}           
                    }}
                }}
                '''

            if force == True:
                confirm = 'y'
            if confirm == 'y':
                result = Utils._executeGraphQL(
                    self, graphQLString, correlationId)
                if result == None:
                    return
                if result[key]['errors']:
                    Utils._listGraphQlErrors(result, key)
                    return
                else:
                    logger.info(f"Inventories '{inventoryNames}' deleted.")
            else:
                return

    def variants(self) -> pd.DataFrame:
        """
            Returns a dataframe of available variants.
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            key = 'variants'
            graphQLString = f'''query getVariants {{
            {key} {{
                name
                variantId
                }}
            }}
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            df = pd.json_normalize(result[key])
            return df

    def deleteVariant(
        self,
        variantId: str,
        force: bool = False
    ) -> None:
        """Deletes a variant

        Parameters
        -----------
        variantId : str
            The id of the variant.
        force : bool
            Use True to ignore confirmation.
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):

            if force == False:
                confirm = input(
                    f"Press 'y' to delete  variant with Id {variantId}: ")

            key = 'deleteVariant'
            graphQLString = f'''mutation deleteVariant {{
                {key}(input: {{ variantId: "{variantId}" }}) {{
                    errors {{
                    message
                    code
                    }}
                }}
            }}
            '''

            if force == True:
                confirm = 'y'
            if confirm == 'y':
                result = Utils._executeGraphQL(
                    self, graphQLString, correlationId)
                if result == None:
                    return
            else:
                return

            if result[key]['errors'] != None:
                Utils._listGraphQlErrors(result, key)
            else:
                logger.info(f"Variant deleted.")

    def deleteItems(
        self,
        inventoryName: str,
        inventoryItemIds: list = None,
        where: str = None,
        force: bool = False,
        pageSize: int = 500
    ) -> None:
        """
        Deletes inventory items from a list of inventoryItemIds or by where-criteria. 

        Parameters:
        -----------
        inventoryName: str
            The name of the inventory.
        inventoryItemIds: list = None
            A list of inventoryItemIds that should be deleted.
        where: str = None
            Filter criteria to select items that should be deleted.
        force: bool = False
            Use True to ignore confirmation.
        pageSize: int = 500
            Only a limited amount of items can be deleted at once. 500 is default, however, 
            if this size is too, big, choose a lower pageSize.

        Examples:
        ---------
        >>> deleteItems('meterData', where='changeDate gt "2020-12-01"', force=True, pageSize=100)
        >>> deleteItems('meterData', inventoryItemIds=['El5JrMG2xk'])
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            if not self._isInventoryOfValidVariant(inventoryName):
                Utils._error(self, f"Items of a TimeSeries inventory cannot be deleted. Use TimeSeries.deleteItems() instead.")
                return
            def delete(ids, n, m):

                _ids = '['
                for id in ids[n:m]:
                    _ids += f'''{{sys_inventoryItemId: "{id}"}}\n'''
                _ids += ']'

                key = f'delete{inventoryName}'
                graphQLString = f'''
                    mutation deleteItems {{
                        {key} ( input: 
                            {_ids}
                        )
                        {{
                            {Utils.errors}           
                        }}
                    }}
                    '''

                result = Utils._executeGraphQL(
                    self, graphQLString, correlationId)

                if result[key]['errors'] != None:
                    logger.error(Utils._listGraphQlErrors(result, key))
                    return

            if inventoryItemIds == None and where == None:
                Utils._error(
                    self, f"No list of items and no where-criteria were provided.")
                return

            if inventoryItemIds != None and where != None:
                logger.warning(
                    f"List of items and where-criteria has been provided. Item list is used.")

            if where != None:
                _result = self.items(inventoryName, fields=[
                                     'sys_inventoryItemId'], where=where)
                if _result.empty:
                    logger.info(f"No results found for provided filter.")
                    return
                ids = list(_result['sys_inventoryItemId'])
            if inventoryItemIds != None:
                _result = self.items(inventoryName, fields=[
                                     'sys_inventoryItemId'], where=f'sys_inventoryItemId in {inventoryItemIds}')
                if _result.empty:
                    logger.info(f"Provided id(s) could not be found.")
                    return
                ids = list(_result['sys_inventoryItemId'])
                diff = set(inventoryItemIds).difference(set(ids))
                if diff:
                    Utils._error(
                        self, f"The following item id's are not in the inventory: {ids}")
                    return

            logger.debug(f"GraphQL Ids: {ids}")

            if force == False:
                confirm = input(f"Press 'y' to delete  {len(ids)} items: ")

            if force == True:
                confirm = 'y'
            if confirm == 'y':
                n = 0
                m = n + pageSize

                while True:
                    delete(ids, n, m)
                    n += pageSize
                    m += pageSize

                    if len(ids) - m < pageSize:
                        delete(ids, n, len(ids))
                        break
            else:
                return

            logger.info(f"{len(ids)} items deleted.")
            return

    def clearInventory(
        self,
        inventoryName: str,
        force: bool = False,
        pageSize: int = 500
    ) -> None:
        """
        Deletes all items from the inventory

        Parameters
        -----------
        inventoryName : str
            The name of the inventory.
        force : bool
            Use True to ignore confirmation.
        pageSize : str = 500
            The number of items to be deleted in a chunk (the maximum number 
            of items that can be deleted in one mutation is restricted).

        Example:
        ---------
        >>> clearInventory('meterData', force=True)
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            if not self._isInventoryOfValidVariant(inventoryName):
                Utils._error(self, f"Items of a TimeSeries inventory cannot be deleted. Use TimeSeries.deleteItems() instead.")
                return
            if force == False:
                confirm = input(
                    f"Press 'y' to delete all items in inventory {inventoryName}: ")
            if force == True:
                confirm = 'y'
            if confirm != 'y':
                return

            count = 0
            lastId = ''

            while True:
                graphQLString = f''' query getItems {{
                        {inventoryName} (
                                pageSize: {pageSize} 
                                {lastId}
                                ) {{
                            sys_inventoryItemId
                        }}
                    }}
                    '''

                _result = Utils._executeGraphQL(
                    self, graphQLString, correlationId)
                ids = [item['sys_inventoryItemId']
                       for item in _result[inventoryName]]
                count += len(ids)

                _ids = ''
                for id in ids:
                    _ids += f'{{sys_inventoryItemId: "{id}"}}\n'

                try:
                    cursor = _result[inventoryName][-1]['sys_inventoryItemId']
                    lastId = f'lastId: "{cursor}"'

                    key = f'delete{inventoryName}'
                    graphQLString = f'''
                        mutation deleteItems {{
                            {key} ( input: 
                                [{_ids}]
                            )
                            {{
                                {Utils.errors}           
                            }}
                        }}
                    '''
                    result = Utils._executeGraphQL(
                        self, graphQLString, correlationId)
                except:
                    break

            if count == 0:
                logger.info(f"Inventory is empty. No items were deleted.")
                return
            if result[key]['errors'] != None:
                Utils._listGraphQlErrors(result, key)
            else:
                logger.info(f"{count} items deleted.")

    def updateVariant(
        self,
        variantName,
        newName=None,
        icon=None
    ) -> None:
        """Updates a variant"""

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            _variantId = Utils._getVariantId(self.variants(), variantName)
            logger.debug(f"Found variantId: {_variantId}")

            if newName != None:
                _name = f'name: "{newName}"'
            else:
                _name = 'null'

            if icon != None:
                _icon = f'icon: "{icon}"'
            else:
                _icon = 'null'

            key = 'updateVariant'
            graphQLString = f'''mutation updateVariant {{
                {key} (input:{{
                    variantId: "{_variantId}"
                    {_name}
                    {_icon}
                    }})
                    {{
                        {Utils.errors}           
                    }}
                }}
                '''

            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            return

    def updateArrayProperty(
        self,
        inventoryName: str,
        inventoryItemId: str,
        arrayProperty: str,
        operation: str,
        arrayItems: list = None,
        cascadeDelete: bool = False
    ) -> None:
        """
        Updates a single array property of a single inventoryItemId. Arrays with and without 
        references are supported.

        Parameters:
        -----------
        inventoryName: str
            The name of the inventory where the item is located.
        inventoryItemId: str
            The sys_inventoryItemId of the item.
        arrayProperty: str
            The name of the property whose array items are to be updated.
        operation: str
            The update operation to be performed. Options:
            insert: inserts a list of array items.
            removeById: removes array items by a list of given ids.
            removeByIndex: removes array items by a list of given indices.
            removeAll: removes all array items
        arrayItems: list = None
            A list of indices or item Ids
        cascadeDelete: bool = False
            If array items are refencences, True will delete also the reference items. 

        Examples:
        ---------
        >>> client.updateArrayProperty('meterData', 'A5N45hOOmm',
                'timeSeries', action='insert', arrayItems=['A5FdSjehbE'])
        >>> client.updateArrayProperty('meterData', 'A5N45hOOmm',
                'timeSeries', action='removeByIndex', arrayItems=[0,1], cascadeDelete=True)
        """
        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):

            operations = ['insert', 'removeById', 'removeByIndex', 'removeAll']
            if operation not in operations:
                Utils._error(
                    self, f"Action '{operation}' allowed. Possible update operations: {operations}.")
                return

            if operation == 'removeAll':
                try:
                    propertyDf = TechStack.inventoryProperties(
                        self, inventoryName)
                    arrayProps = propertyDf[propertyDf['name']
                                            == arrayProperty]
                    logger.debug(f"Properties of array: {arrayProps}")
                    if arrayProps['type'].item() == 'reference':
                        # arrDf = TechStack.items(self, inventoryName,
                        #     where=f'sys_inventoryItemId eq "{inventoryItemId}"', fields=[f'{arrayProperty}.sys_inventoryItemId'],
                        #     arrayPropertiesToPage=[arrayProperty], arrayPageSize=5000)
                        arrDf = TechStack.items(self, inventoryName,
                                                where=f'sys_inventoryItemId eq "{inventoryItemId}"', fields=[f'{arrayProperty}.sys_inventoryItemId'],
                                                )
                    else:
                        arrDf = TechStack.items(self, inventoryName, fields=[{arrayProperty}],
                                                where=f'sys_inventoryItemId eq "{inventoryItemId}"', arrayPageSize=5000)
                except Exception as err:
                    Utils._error(self, err)
                    return

                countArray = len(arrDf[arrayProperty].item())
                arrayItems = [num for num in range(countArray)]
                logger.debug(f"Array Items: {arrayItems}")
            _arrayItems = Utils._arrayItemsToString(
                arrayItems, operation, cascadeDelete)
            logger.debug(f"Array Items as String: {_arrayItems}")

            key = f'update{inventoryName}ArrayProperties'
            graphQLString = f'''mutation updateArray {{
                {key} (
                    input: {{
                    sys_inventoryItemId: "{inventoryItemId}"
                    {arrayProperty}: {{
                        {_arrayItems}
                        }}
                    }}
                ) 
                {{
                    {Utils.errors}           
                }}
            }}'''

            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            if result[key]['errors'] != None:
                Utils._listGraphQlErrors(result, key)
            else:
                logger.info(
                    f"Array property {arrayProperty} for item {inventoryItemId} updated.")

    def addInventoryProperties(
        self,
        inventoryName: str,
        properties: list
    ) -> None:
        """
        Adds one or more inventory properties to an existing inventory.

        Parameters:
        ----------
        inventoryName: str
            Name of inventory
        properties: list
            A list of dicts with the following mandatory keys: 
                name: str
                dataType: enum (STRING, BOOLEAN, DECIMAL, INT, LONG, DATE_TIME, 
                DATE_TIME_OFFSET)
            Optional keys:
                isArray: bool (Default = False)
                nullable: bool (Default = True)
                isReference: bool (Default = False)
                inventoryId: str (mandatory if hasReference = True)
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            key = 'addProperty'
            inventory = self.inventories(where=f'name eq "{inventoryName}"')

            if inventory.empty:
                Utils._error(self, f"Unknown inventory '{inventoryName}'.")
                return

            inventoryId = inventory.loc[0, 'inventoryId']
            _properties = Utils._propertiesToString(properties)

            graphQLString = f'''
            mutation {key} {{
            {key} (input: {{
                inventoryId: "{inventoryId}"	
                properties: {_properties}
                }}) 
                {{
                    {Utils.errors}           
                }}
            }}
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
                return
            else:
                self.updateClient()
                logger.info(f"New property(ies) added.")

    def updateDisplayValue(
        self,
        inventoryName: str,
        displayValue: str
    ) -> None:

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            inventoryId = self.structure[inventoryName]['inventoryId']

            key = 'updateInventory'
            graphQLString = f'''mutation updateDisplayValue {{
                {key} (input: {{
                    inventoryId: "{inventoryId}"
                    displayValue: "{displayValue}"
                    }}) {{
                    {Utils.errors}
                }}
            }}
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
                return
            else:
                self.updateClient()
                logger.info(f"Display value updated.")
                return

    def updateInventoryName(
        self,
        inventoryName: str,
        newName: str
    ) -> None:

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            inventoryId = self.structure[inventoryName]['inventoryId']
            key = 'updateInventory'

            graphQLString = f'''mutation updateInventoryName {{
                {key} (input: {{
                    name: "{newName}"
                    inventoryId: "{inventoryId}"
                }}) {{
                    {Utils.errors}
                    }}
                }}
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return
            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
                return
            else:
                logger.info(f"Inventory name updated.")
                self.updateClient()
                return

    def removeProperties(
        self,
        inventoryName: str,
        properties: list
    ) -> None:
        """
        Removes a list of properties given as property names. Properties can 
        only be removed if they have no content or are of type 'reference'.

        Parameters:
        -----------
        inventoryName: str
            The name of the inventory where the item is located.
        properties: list
            A list of property names.
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            if type(properties) != list:
                properties = [properties]

            propertyList = '['
            for argProperty in properties:
                try:
                    propertyId = self.structure[inventoryName]['properties'][argProperty]['propertyId']
                    propertyList += f'"{propertyId}",'
                except:
                    logger.warning(
                        f"Property '{argProperty}' not found in inventory '{inventoryName}'.")
            propertyList += ']'

            inventoryId = self.structure[inventoryName]['inventoryId']

            key = 'removeProperty'
            graphQLString = f'''mutation removeProperty {{
                {key} (input: {{
                        inventoryId: "{inventoryId}"
                        propertyIds: {propertyList}
                }}) {{
                    {Utils.errors}
                    }}
                }}
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return
            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
                return
            else:
                self.updateClient()
                logger.info(f"Properties have been removed.")
                return

    def updateProperty(
        self,
        inventoryName: str,
        propertyName: str,
        newPropertyName: str = None,
        nullable: bool = None
    ) -> None:

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            inventoryId = self.structure[inventoryName]['inventoryId']
            newPropertyName = Utils._argNone('name', newPropertyName)
            nullable = Utils._argNone('nullable', nullable)

            try:
                propertyId = self.structure[inventoryName]['properties'][propertyName]['propertyId']
            except:
                Utils._error(
                    self, f"Property '{propertyName}' not found in inventory '{inventoryName}'.")
                return

            key = 'updateInventory'
            graphQLString = f'''mutation removeProperty {{
                {key} (input: {{
                        inventoryId: "{inventoryId}"
                        properties: [{{
                            propertyId: "{propertyId}"
                            {newPropertyName}
                            {nullable}
                        }}]
                }}) {{
                    {Utils.errors}
                    }}
                }}
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return
            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
                return
            else:
                self.updateClient()
                logger.info(f"Property updated.")
                return

    def resync(self) -> None:
        """Resynchronizes read databases"""

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            key = 'reSyncReadDatabase'
            graphQLString = f'''mutation resync{{
                {key}
                }}
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return
            self.updateClient()

            return

    def defaultDataFrame(
        self,
        maxRows,
        maxColumns
    ) -> None:
        """Sets default sizes for a DataFrame for the current session"""
        pd.options.display.max_rows = maxRows
        pd.options.display.max_columns = maxColumns
        return

    def _convertId(
        self,
        sys_inventoryItemId: str
    ) -> str:
        """Convers a sys_inventoryItemId into a HAKOM name"""

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            graphQLString = f'''mutation convert{{
                convertId(id: "{sys_inventoryItemId}")
                }}
            '''
            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            if result == None:
                return

            return result['convertId']

    def _isInventoryOfValidVariant(
        self,
        inventoryName: str,
        variantName: str = None
    ) -> bool:
        """Checks if an inventory is of a valid variant"""

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):
            inventory = self.inventories(
                where=f'name eq "{inventoryName}"', fields=['variant.name'])
            if inventory.empty:
                Utils._error(self, f"Unknown inventory '{inventoryName}'.")
                return

            # in case of inventory without variant there is a column 'variant' with None
            if variantName == None:
                return 'variant' in inventory
            else:
                return not 'variant' in inventory and inventory.iloc[0]['variant.name'] == variantName