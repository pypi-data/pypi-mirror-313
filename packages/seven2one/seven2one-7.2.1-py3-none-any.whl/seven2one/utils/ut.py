import datetime
from typing import (
    Any,
    Dict,
)
from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Union
import pytz
import os
import base64
import math
import pandas as pd
from gql import Client, gql
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient
from tzlocal import get_localzone
from loguru import logger
from collections import namedtuple
from gql.transport.requests import RequestsHTTPTransport
from .ut_auth import AuthData


if os.name == 'nt':  # only if the platform is Windows, pyperclip will be imported
    import pyperclip


@dataclass
class Defaults():
    timeZone: str = 'UTC'
    useDateTimeOffset: bool = True
    copyGraphQLString: bool = False


class Structure():
    queryStructure = f'''query inventories {{
    inventories (pageSize:1000) {{
        name
        inventoryId
        displayValue
        isDomainUserType
        hasValidityPeriods
        historyEnabled
        propertyUniqueness {{
            uniqueKey
            properties
            }}
        variant {{
            name
            properties {{
                name
                type
                isArray
                nullable
                }}
            }}
        properties {{
            name
            ...Scalar
            type
            isArray
            nullable
            propertyId
            ... Reference 
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

    def _introspectionQueryString():
        introspectionQueryString = r'''
            query IntrospectionQuery { __schema { queryType { name } mutationType 
                { name } subscriptionType { name } types { ...FullType } directives
                { name description locations args { ...InputValue } } } }

            fragment FullType on __Type { kind name description fields(includeDeprecated: true) { name description args 
                { ...InputValue } type { ...TypeRef } isDeprecated deprecationReason } inputFields { ...InputValue } interfaces 
                { ...TypeRef } enumValues(includeDeprecated: true) { name  } possibleTypes { ...TypeRef } } 

            fragment InputValue on __InputValue { name description type { ...TypeRef } defaultValue } 
            fragment TypeRef on __Type { kind name ofType { kind name ofType { kind name ofType 
                    { kind name ofType { kind name ofType { kind name ofType { kind name ofType { kind name } } } } } } } }
        '''
        return introspectionQueryString

    def _fullStructureDict(structure) -> dict:
        """Converts the query of all inventories with all fields into a pure dict"""

        def subdict(inputObject, name):
            itemDict = {}
            for item in inputObject:
                itemDict.setdefault(item[name], {})
                for k, v in item.items():
                    itemDict[item[name]].setdefault(k, v)
            return itemDict

        structureDict = {}
        for inventory in structure['inventories']:
            inventoryName = inventory['name']
            structureDict.setdefault(inventoryName, {})
            for definitionKey, definitionValue in inventory.items():
                if not isinstance(definitionValue, (list, dict)):
                    structureDict[inventoryName].setdefault(
                        definitionKey, definitionValue)
                else:
                    if definitionKey == 'properties':
                        subDict = subdict(inventory[definitionKey], 'name')
                        structureDict[inventoryName].setdefault(
                            definitionKey, subDict)
                    if definitionKey == 'propertyUniqueness':
                        subDict = subdict(
                            inventory[definitionKey], 'uniqueKey')
                        structureDict[inventoryName].setdefault(
                            definitionKey, subDict)
                    if definitionKey == 'variant':
                        structureDict[inventoryName].setdefault(
                            definitionKey, {})
                        structureDict[inventoryName][definitionKey].setdefault(
                            'name', definitionValue['name'])
                        subDict = subdict(
                            inventory[definitionKey]['properties'], 'name')
                        structureDict[inventoryName][definitionKey].setdefault(
                            'properties', subDict)
        return structureDict

    def _fullStructureNT(structure: dict) -> namedtuple:
        """
        Provides the complete data structure of dynamic objects as named tuple. 
        Needs structureDict first
        """
        def _subItem(object: dict):
            Item = namedtuple('Item', object.keys())
            itemDict = {}
            for key, value in object.items():
                if isinstance(value, dict):
                    subItem = _subItem(value)
                    itemDict.setdefault(key, subItem)
                else:
                    itemDict.setdefault(key, value)
            item = Item(**itemDict)
            return item

        Item = namedtuple('Item', structure.keys())
        itemDict = {}
        for key, value in structure.items():
            if isinstance(value, dict):
                subItem = _subItem(value)
                itemDict.setdefault(key, subItem)
            else:
                itemDict.setdefault(key, value)
        return Item(**itemDict)

    def _inventoryNT(structure) -> namedtuple:
        """
        Provides a simplified namedtuple of dynamic objects for interactive usage
        """
        inventoryDict = {key: key for key in structure.keys()}
        Inventories = namedtuple('Inventories', inventoryDict.keys())
        return Inventories(**inventoryDict)

    def _inventoryPropertyNT(structure) -> namedtuple:
        """
        Provides a simplified namedtuple of inventory properties for interactive usage
        """
        Inventory = namedtuple('Inventories', structure.keys())
        inventoryDict = {}

        for inventory in structure.keys():
            propertyDict = {}
            for key in structure[inventory]['properties'].keys():
                propertyDict.setdefault(key, key)
                Properties = namedtuple('Properties', propertyDict.keys())
                properties = Properties(**propertyDict)
            inventoryDict.setdefault(inventory, properties)
        return Inventory(**inventoryDict)


class Utils():
    errors = f'''errors {{
                    message
                    code
                }}'''

    def _error(self, msg: str):
        if self.raiseException:
            raise Exception(msg)
        else:
            logger.error(msg)
            return

    def _timeZone(timeZone):
        if timeZone == None or timeZone == 'local':
            try:
                localTimeZone = get_localzone().zone
                return str(pytz.timezone(localTimeZone))
            except AttributeError:
                return str(get_localzone())
        else:
            return str(pytz.timezone(timeZone))

    def _graphQLList(itemList: list) -> str:
        """Converts a list to a graphQL list"""

        def is_number(n):
            try:
                float(n)
            except ValueError:
                return False
            return True

        result = '['
        for item in itemList:
            if is_number(item):
                result += f'{item},'
            else:
                result += f'"{item}",'
        result += ']'
        return result

    def _queryFields(fieldList: list, arrayTypeFields: list = None, arrayPageSize: int = None, filter: dict = None, recursive=False) -> str:
        """
        Transforms a Python list of fields into graphQL String of fields
        including fields of referenced inventories        
        """

        def nestedItem(item):
            nonlocal fields
            line = ''
            for i in range(itemLength - 1):
                if arrayTypeFields != None and item[i] in arrayTypeFields:
                    if filter != None and item[i] in filter.keys():
                        line += f'{item[i]} (pageSize: {arrayPageSize}, where: {filter[item[i]]}) {{ '
                    else:
                        line += f'{item[i]} (pageSize: {arrayPageSize}) {{ '
                else:
                    line += f'{item[i]} {{ '
            line += f'{item[-1]} '
            for _ in range(itemLength - 1):
                line += '}'
            line += ' \n'
            fields += line

        fields = ''
        splitList = [item.split('.') for item in fieldList]
        logger.debug(f"intermediate step - splitted list: {splitList}")

        for item in splitList:
            if len(item) == 1:
                fields += f'{item[0]}  \n'
            else:
                itemLength = len(item)
                if recursive == False:
                    if item[-1] == '_displayValue':
                        nestedItem(item)
                    if item[-1] == 'sys_inventoryItemId':
                        nestedItem(item)
                else:
                    nestedItem(item)
        return fields

    def _handleWhere(self, where, inventoryName: str = None) -> str:
        """Handles the where argument if any"""
        if where != None:
            resolvedFilter = Utils._resolveWhere(self, where, inventoryName)
            logger.debug(f"Resolved filter: {resolvedFilter}")
            if 'topLevel' in resolvedFilter.keys():
                topLevelFilter = resolvedFilter['topLevel']
                if topLevelFilter == None:
                    return
        else:
            topLevelFilter = ''
            resolvedFilter = None
        if '[]' in topLevelFilter:
            Utils._error(self, "Filter is not resolvable.")
            return ''
        return topLevelFilter, resolvedFilter

    def _toGraphQL(value) -> Union[str, int, float, bool]:
        """
        Escapes a value for usage in GraphQL. Surrounding " will be added automatically.

        Parameters
            value
                The value which should be escaped for GraphQL.

        Returns
            Escaped value. Includes surrounding " for strings.

        Raises
            ValueError
                If value is NaN.

        Examples:
        * string ABC becomes string "ABC"
        * string A"BC becomes string "A\\"BC"
        * string "ABC" becomes string "\\"ABC\\""
        * int 123 becomes 123
        * float 12.34 becomes 12.34
        * None becomes string null
        * True becomes string true
        * False becomes string false
        * [1, 2, 3] becomes [1, 2, 3]
        """
        if (value == None):
            return 'null'
        if (isinstance(value, bool)):
            return 'true' if value else 'false'
        if (isinstance(value, int)):
            return str(value)
        if (isinstance(value, float)):
            if (math.isnan(value)):
                raise ValueError('Value is NaN.')
            return str(value)
        if type(value) == list:
            escapedList = ', '.join(Utils._toGraphQL(item) for item in value)
            return f'[{escapedList}]'
        escapedValue = str(value).replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escapedValue}"'

    def _resolveWhere(self, filterArg, inventoryName=None):
        """
        How does this work:
        A list of lists is created, where 'or terms' are the elements of the parent list and 
        'and terms' are elements of a child list of an or (or single) element.
        For each 'and' in a child list, the string will be closed with an extra '}'

        Lists (as string) are treated seperately, but work the same as a single or an 'and' element.
        """

        def mapOperator(operator):
            operators = {
                '==': 'eq',
                'eq': 'eq',
                'in': 'in',
                '<': 'lt',
                '>': 'gt',
                '<=': 'lte',
                '>=': 'gte',
                'lt': 'lt',
                'gt': 'gt',
                'lte': 'lte',
                'gte': 'gte',
                'contains': 'contains',
                '!=': 'neq',
                'ne': 'neq',
                'neq': 'neq',
                'not in': 'not in',
                'startsWith': 'startsWith',
                'startswith': 'startsWith',
                'endsWith': 'endsWith',
                'endswith': 'endsWith',
                '=': 'eq'
            }
            if operator in operators:
                return operators[operator]
            else:
                logger.error(f"Unknown operator '{operator}'")

        def _split(itemToSplit: str) -> list:
            "Splits a string by spaces and strips all blanks"
            splitted = itemToSplit.split(' ')
            for item in reversed(splitted):
                if item == '':
                    splitted.remove(item)

            if len(splitted) > 3:
                Utils._error(
                    self, f'''Invalid filter criteria {itemToSplit}. Did you miss to put the search string in double quotes ("")?''')
            return splitted

        def _secondLevelFilter(el: namedtuple, inventoryName: str, resultDict: dict):
            """Builds the filter part for second level"""

            subProperty = el.property.split('.')[0]
            subFilterProperty = el.property.split('.')[1]
            try:
                subInventory = self.structure[inventoryName]['properties'][subProperty]['inventoryName']
            except:
                Utils._error(
                    self, f"Unknown property '{subProperty}' in '{el.property}'.")
                return

            df = self.items(subInventory, fields=['sys_inventoryItemId'],
                            where=[f'{subFilterProperty} {el.operator} {el.searchItem}'])

            try:
                itemIds = list(df['sys_inventoryItemId'])
            except:
                logger.warning(
                    f"'{subFilterProperty} {el.operator} {el.searchItem}' does not lead to a result.")
                return ''
            if len(itemIds) == 0:
                logger.error(f"{el.property} is not a valid filter criteria.")
                return ''

            # Check, if filter compund is of array type (treated differently)
            subFilterPropertyIsArray = self.structure[inventoryName]['properties'][subProperty]['isArray']
            if subFilterPropertyIsArray:
                if len(itemIds) == 1:
                    whereString = f'{{sys_inventoryItemId: {{ eq: "{itemIds[0]}" }} }}'
                else: # if it is a list
                    itemIds = Utils._graphQLList(itemIds)
                    whereString = f'{{sys_inventoryItemId: {{ in: {itemIds} }} }}'
            else:
                if len(itemIds) == 1:
                    whereString = f'{{{subProperty}: {{sys_inventoryItemId: {{ eq: "{itemIds[0]}" }} }} }}'
                else: # if it is a list
                    itemIds = Utils._graphQLList(itemIds)
                    whereString = f'{{{subProperty}: {{sys_inventoryItemId: {{ in: {itemIds} }} }} }}'

            # subFilterPropertyIsArray = self.structure[inventoryName]['properties'][subProperty]['isArray']
            if subFilterPropertyIsArray:
                resultDict.setdefault(subProperty, whereString)
                logger.warning("Test")
                Utils._error(
                    self, f"Array properties are not yet supported in filters: '{subProperty}'")
                return resultDict.setdefault(subProperty, whereString)

            else:
                return whereString

        def createFilterPart(subElement) -> namedtuple:
            SubElement = namedtuple(
                'SubElement', ['property', 'operator', 'searchItem'])
            if '[' in subElement:  # if it is a list
                x = subElement.find('[')
                sub = subElement[:x].split(' ')
                sub_last = subElement[x:]
                if sub_last.count('"') == 0:  # if it is a real list put in by {}
                    sub_last = sub_last[1:-1].split(',')
                    sub_last = [item.lstrip() for item in sub_last]
                    sub_last = [item.replace("'", "") for item in sub_last]
                    sub_last = Utils._graphQLList(sub_last)
                el = SubElement(
                    property=sub[0], operator=sub[1], searchItem=sub_last)
                if el.property.count('.') == 1:
                    whereString = _secondLevelFilter(
                        el, inventoryName, resultDict)
                else:
                    whereString = f'{{ {el.property}: {{ {mapOperator(el.operator)}: {el.searchItem} }} }}'
                return whereString
            else:
                if subElement.count('"') == 2:  # search item is a string
                    x = subElement.find('"')
                    sItem = subElement[x:]
                    sub = _split(subElement[:x])
                # search item is not a string (but valid)
                elif subElement.count('"') == 0:
                    sub = _split(subElement)
                    sItem = sub[2]
                else:  # invalid sub elements with 1 or more than 3 double quotes
                    Utils._error(self, f"Invalid filter criteria {subElement}")

                el = SubElement(property=sub[0],
                                operator=sub[1], searchItem=sItem)
                if el.property.count('.') == 1:
                    whereString = _secondLevelFilter(
                        el, inventoryName, resultDict)
                else:
                    whereString = f'{{ {el.property}: {{ {mapOperator(el.operator)}: {el.searchItem} }} }}'
                return whereString

        def filterPart(arg):
            if type(arg) == str:
                return createFilterPart(arg)
            elif type(arg) == list:
                whereString = '{and: ['
                for i, subArg in enumerate(arg):
                    whereString += filterPart(subArg)
                    if i != len(arg) - 1:
                        whereString += ', '
                whereString += ']} '
                return whereString
            elif type(arg) == tuple:
                whereString = '{or: ['
                for i, subArg in enumerate(arg):
                    whereString += filterPart(subArg)
                    if i != len(arg) - 1:
                        whereString += ', '
                whereString += ']} '
                return whereString
            elif type(arg) == bool:
                Utils._error(self, f"Wrong syntax of filter '{filterArg}'.")
                return

        resultDict = {}

        if type(filterArg) in [list, tuple]:
            whereString = filterPart(filterArg)
        else:
            if ' or ' in filterArg:
                Utils._error(
                    self, f"'or' is not supported in string type filters.")
            filterArg = filterArg.split(' and ')
            whereString = filterPart(filterArg)
            resultDict.setdefault('topLevel', 'where: ' + whereString)

        if whereString:
            resultDict.setdefault('topLevel', 'where: ' + whereString)

        logger.debug(f"ResultDict: {resultDict}")
        return resultDict

    def _propertiesToString(properties: list) -> str:
        """ Converts a list of property dicts for many items into a string """
        if type(properties) == list:
            _properties = '[\n'
            for property in properties:
                _properties += '{\n'
                for key, value in property.items():
                    _properties += Utils._customProperties(key, value)

                _properties += '}\n'
            _properties += ']'
            return _properties
        if type(properties) == dict:
            _properties = '{\n'
            for key, value in properties.items():
                _properties += Utils._customProperties(key, value)
            _properties += '}\n'
            return _properties
        else:
            logger.error(
                f"Type of property items has to be either list ord dict.")
            return

    def _tsPropertiesToString(properties: list) -> str:
        """ Converts a list of property dicts for many items into a string """
        timeUnit, factor = 'timeUnit', 'factor'
        _properties = '[\n'
        for property in properties:
            _properties += '{\n'
            for key, value in property.items():
                if key == 'resolution':
                    try:
                        _properties += f'{key}: {{\n'
                        _properties += f'timeUnit: {value[timeUnit]}\n'
                        _properties += f'factor: {value[factor]}\n'
                        _properties += f'}}\n'
                    except KeyError:
                        logger.error(
                            "Missing 'timeUnit' and/or 'factor' for Timeseries resolution")
                        return
                else:
                    _properties += Utils._customProperties(key, value)

            _properties += '}\n'
        _properties += ']'
        return _properties

    def _addToGroupPropertiesToString(groupItemId: str, properties: list) -> str:
        """ Converts a list of property dicts for many items into a string """

        _properties = '[\n'
        for property in properties:
            _properties += f'{{sys_groupInventoryItemId: "{groupItemId}"\n'
            for key, value in property.items():
                _properties += Utils._customProperties(key, value)

            _properties += '}\n'
        _properties += ']'
        return _properties

    def _uniquenessToString(propertyUniqueness: list):
        """
        Converts a list of unique keys into a string
        """

        _uniqueKeys = '[\n'
        for item in propertyUniqueness:
            key = item['uniqueKey']
            _uniqueKeys += f'{{uniqueKey: "{key}" properties: ['
            for value in item['properties']:
                _uniqueKeys += f'"{value}",'

            _uniqueKeys += ']}\n'
        _uniqueKeys += ']'
        return _uniqueKeys

    def _customProperties(key: str, value: object) -> str:
        """
        Used internally (in Utils) as helper function
        """

        if key == 'dataType':
            return f'{key}: {value}\n'
        return  f'{key}: {Utils._toGraphQL(value)}\n'

    def _properties(scheme, inventoryName:str, recursive:bool=True, sysProperties:bool=False, maxRecursionDepth:int=2) -> dict:
        """
        Creates a nested (or unnested) dict with properties and array 
        type fields for further usage out of the scheme
        """

        propertyDict = {'properties': {}, 'arrayTypeFields': []}
        properties = propertyDict['properties']
        arrayTypeFields = propertyDict['arrayTypeFields']

        def _getInventoryObject(scheme, inventoryName):
            for item in scheme['__schema']['types']:
                if item != None and item['name'] == inventoryName:
                    return item['fields']

        def _createSubDict(subInv, currentRecursionLevel=0):
            subDict = {}
            inventoryObject = _getInventoryObject(scheme, subInv)
            for item in inventoryObject:
                if sysProperties == False:
                    if item['name'].startswith('sys_'):
                        if item['name'] == 'sys_inventoryItemId':
                            pass
                        else:
                            continue
                if item['type']['kind'] == 'SCALAR':
                    subDict.setdefault(item['name'], item['type']['name'])
                if item['type']['kind'] == 'LIST':
                    if item['name'] == 'sys_permissions':
                        pass
                    elif item['type']['ofType']['kind'] == 'OBJECT':
                        arrayTypeFields.append(item['name'])
                        if recursive == False or currentRecursionLevel > maxRecursionDepth:
                            subDict.setdefault(
                                item['name'], item['type']['name'])
                        else:
                            subDict.setdefault(item['name'], _createSubDict(
                                item['type']['ofType']['name'], currentRecursionLevel + 1))
                    else:
                        arrayTypeFields.append(item['name'])
                        subDict.setdefault(item['name'], item['type']['name'])
                if item['type']['kind'] == 'OBJECT':
                    if recursive == False or currentRecursionLevel > maxRecursionDepth:
                        subDict.setdefault(item['name'], item['type']['name'])
                    else:
                        subDict.setdefault(item['name'], _createSubDict(
                            item['type']['name'], currentRecursionLevel + 1))

            return subDict

        inventoryObject = _getInventoryObject(scheme, inventoryName)
        for item in inventoryObject:
            if sysProperties == False:
                if item['name'].startswith('sys_'):
                    if item['name'] == 'sys_inventoryItemId':
                        pass
                    else:
                        continue
            if item['type']['kind'] == 'SCALAR':
                properties.setdefault(item['name'], item['type']['name'])
            if item['type']['kind'] == 'LIST':
                if item['name'] == 'sys_permissions':
                    pass
                elif item['type']['ofType']['kind'] == 'OBJECT':
                    arrayTypeFields.append(item['name'])
                    if recursive == False:
                        properties.setdefault(
                            item['name'], item['type']['name'])
                    else:
                        properties.setdefault(item['name'], _createSubDict(
                            item['type']['ofType']['name']))
                else:
                    arrayTypeFields.append(item['name'])
                    properties.setdefault(item['name'], item['type']['name'])
            if item['type']['kind'] == 'OBJECT':
                if recursive == False:
                    properties.setdefault(item['name'], item['type']['name'])
                else:
                    properties.setdefault(
                        item['name'], _createSubDict(item['type']['name']))

        logger.debug(f"returned property dict: {propertyDict}")

        return propertyDict

    def _propertyList(propertyDict: dict, recursive: bool = False) -> list:
        """Uses _properties() to create a flat list of properties"""

        propertyList = []

        def instDict(subDict, path):
            if recursive == True:
                for k, v in subDict.items():
                    if isinstance(v, dict):
                        path = f'{path}.{k}'
                        instDict(subDict[k], path)
                    else:
                        propertyList.append(f'{path}.{k}')
            else:
                if '_displayValue' in subDict.keys():  # if it is not an array
                    propertyList.append(f'{path}._displayValue')
                else:  # if it is an array
                    propertyList.append(f'{path}.sys_inventoryItemId')

        for k, v in propertyDict.items():
            if isinstance(v, dict):
                instDict(propertyDict[k], k)
            else:
                propertyList.append(k)

        logger.debug(f'returend property list: {propertyList}')
        return propertyList

    def _propertyTypes(propertyDict: dict) -> dict:
        """Uses _properties() o create a flat dictionary of properties"""

        propertyTypes = {}

        def instDict(subDict, path):
            for k, v in subDict.items():
                if isinstance(v, dict):
                    path = f'{path}.{k}'
                    instDict(subDict[k], path)
                else:
                    propertyTypes.setdefault(f'{path}.{k}', v)

        for k, v in propertyDict.items():
            if isinstance(v, dict):
                instDict(propertyDict[k], k)
            else:
                propertyTypes.setdefault(k, v)

        logger.debug(f"returned property types: {propertyTypes}")
        return propertyTypes

    def _orderItems(self, orderBy: Union[dict, list, str], asc: Union[list, str] = None) -> str:

        def _orderDictToString(orderBy: dict) -> str:

            order = 'order: ['
            for key, value in orderBy.items():
                if value not in ['ASC', 'DESC']:
                    Utils._error(
                        self, f"Invalid value '{value}' for property '{key}'. Use 'ASC' or 'DESC' instead.")
                    return
                order += f'{{{key}: {value}}}'
            order += ']'
            return order

        mapping = {False: 'DESC', True: 'ASC', None: 'ASC'}
        if orderBy != None:
            if type(orderBy) == dict:
                order = _orderDictToString(orderBy)
            if type(orderBy) == list:
                if type(asc) == bool:
                    _orderBy = {property: mapping[asc] for property in orderBy}
                elif type(asc) == list:
                    _asc = [mapping[item] for item in asc]
                    _orderBy = dict(zip(orderBy, _asc))
                elif asc == None:
                    _orderBy = {property: 'ASC' for property in orderBy}
                else:
                    Utils._error(
                        self, f"Invalid type '{asc}' for order direction. Use bool or list of bools.")
                order = _orderDictToString(_orderBy)
            if type(orderBy) == str:
                if type(asc) == bool:
                    _orderBy = {orderBy: mapping[asc]}
                elif type(asc) == list:
                    _orderBy = {orderBy: mapping[asc[0]]}
                elif asc == None:
                    _orderBy = {orderBy: 'ASC'}
                else:
                    Utils._error(
                        self, f"Invalid type '{asc}' for order direction. Use bool instead.")
                order = _orderDictToString(_orderBy)
        else:
            order = ''

        return order

    def _copyGraphQLString(graphQLString: str, copyGraphQLString: bool = False) -> None:
        """Can be applied to any core function to get the GraphQL string which is stored in the clipboard"""
        if copyGraphQLString == True and os.name == 'nt':
            return pyperclip.copy(graphQLString)

    def _getVariantId(variants: pd.DataFrame, name: str) -> str:
        """ Gets the variant Id from a given name"""
        variants.set_index('name', inplace=True)
        return variants.loc[name][0]

    def _listGraphQlErrors(result: dict, key: str) -> None:
        """Print errors from GraphQL Query to log"""

        for i in result[key]['errors']:
            logger.error(i['message'])

    def _encodeBase64(file: str):
        with open(file) as file:
            content = file.read()
            content = base64.b64encode(content.encode('ascii'))
            return content.decode('UTF8')

    # deprecated:
    def _getInventoryId(self, inventoryName):
        inventory = self.inventories(where=f'name eq "{inventoryName}"')

        if inventory.empty:
            msg = f"Unknown inventory '{inventoryName}'."
            if self.raiseException:
                raise Exception(msg)
            else:
                logger.error(msg)
                return

        inventoryId = inventory.loc[0, 'inventoryId']
        logger.debug(f'returned inventory id: {inventoryId}')
        return inventoryId

    def _arrayItemsToString(arrayItems: list, operation: str, cascadeDelete: bool) -> str:
        """Converts a list of array items to a graphQL string"""

        cDelValue = 'true' if cascadeDelete == True else 'false'

        if operation == 'insert':
            _arrayItems = 'insert: [\n'
            for item in arrayItems:
                _arrayItems += f'{{value: "{item}"}}\n'
            _arrayItems += ']'
            return _arrayItems
        if operation == 'removeByIndex':
            _arrayItems = f'cascadeDelete: {cDelValue}\n'
            _arrayItems += 'removeByIndex: ['
            for item in arrayItems:
                _arrayItems += f'{item}, '
            _arrayItems += ']'
            return _arrayItems
        if operation == 'removeById':
            _arrayItems = f'cascadeDelete: {cDelValue}\n'
            _arrayItems += 'removeById: ['
            for item in arrayItems:
                _arrayItems += f'"{item}", '
            _arrayItems += ']'
            return _arrayItems
        if operation == 'removeAll':
            _arrayItems = f'cascadeDelete: {cDelValue}\n'
            _arrayItems += 'removeByIndex: ['
            for item in arrayItems:
                _arrayItems += f'{item}, '
            _arrayItems += ']'
            return _arrayItems

    def _executeGraphQL(
            self,
            graphQLString,
            correlationId: str = None,
            params: Dict[str, Any] = None):
        """Executes GraphQl, this code is used in every main function"""

        cid = correlationId or str(uuid4())
        context_logger = logger.bind(correlationId=str(cid))

        Utils._copyGraphQLString(
            graphQLString, self.defaults.copyGraphQLString)
        context_logger.trace(f"GraphQLString: {graphQLString}")
        try:
            query = gql(graphQLString)
        except Exception as err:
            if self.raiseException:
                raise Exception(err)
            else:
                context_logger.error(err)
                return

        try:
            auth_data = self.auth_data
            if auth_data.token is None:
                raise Exception('No valid token available. Please login first.')
            # refresh token if necessary
            expires_at = datetime.fromtimestamp(auth_data.token['expires_at'])
            if expires_at - timedelta(minutes=1) < datetime.now():
                logger.debug(f'Access token expiring in less than 1 minute')
                if auth_data.service_account_secret is None:
                    extra = { 'client_id': auth_data.client_id }
                    logger.debug(f'Refreshing token')
                    self.auth_data.token = OAuth2Session(auth_data.client_id, token=auth_data.token).refresh_token(
                        auth_data.token_url, **extra)
                else:
                    # login with service account returns no refresh token so we need a new login
                    logger.debug(f'Get new token with service account')
                    app_client = BackendApplicationClient(client_id=auth_data.client_id)
                    oauth = OAuth2Session(client=app_client)
                    self.auth_data.token = oauth.fetch_token(token_url=auth_data.token_url, 
                                                            client_id=auth_data.client_id, 
                                                            username=auth_data.service_account_name, 
                                                            password=auth_data.service_account_secret)

            headers = {
                'Authorization': 'Bearer ' + self.auth_data.token['access_token'],
                'X-Correlation-Id': cid,
            }
            transport = RequestsHTTPTransport(
                url=self.endpoint, headers=headers, verify=True, proxies=self.proxies)
            with Client(transport=transport, fetch_schema_from_transport=False) as session:
                result = session.execute(query, variable_values=params)
        except Exception as err:
            if self.raiseException:
                raise Exception(err)
            else:
                context_logger.error(err)
                return

        return result

    def _create_client(self, auth_data: AuthData):
        headers = {
            'authorization': 'Bearer ' + auth_data.token['access_token']
        }
        transport = RequestsHTTPTransport(
            url=self.endpoint, headers=headers, verify=True, proxies=self.proxies)
        return Client(transport=transport, fetch_schema_from_transport=False)

    def _argNone(arg, value, enum=False) -> str:
        """
        Creates a simple string (to be embedded in graphQlString) 
        for arguments that are None by default.
        """
        if value == None:
            return ''
        else:
            if enum == True:
                return f'{arg}: {value}'
            else:
                if type(value) == str:
                    return f'{arg}: "{value}"'
                elif type(value) == float:
                    return f'{arg}: {value}'
                elif type(value) == int:
                    return f'{arg}: {value}'
                elif type(value) == bool:
                    if value == True:
                        return f'{arg}: true'
                    else:
                        return f'{arg}: false'
                else:
                    return f'{arg}: "{str(value)}"'

    def _getServiceVersion(self, service: str):
        """
        Returns name and version of the responsible micro service
        """

        key = f'{service}ServiceInfo'
        graphQLString = f'''query version {{ 
            {key} {{
                name
                informationalVersion
            }}
        }}'''
        result = Utils._executeGraphQL(self, graphQLString)

        return f'{result[key]["name"]}: {result[key]["informationalVersion"]}'
