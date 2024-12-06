from uuid import uuid4
import pandas as pd
from loguru import logger
import json

from .utils.ut import Utils
from .utils.ut_auth import AuthData

class Authorization:

    def __init__(self, endpoint:str, client:object, auth_data: AuthData) -> None:
        self.client = client

        self.raiseException = client.raiseException
        self.defaults = client.defaults

        self.auth_data = auth_data
        self.endpoint = endpoint
        self.proxies = client.proxies
        self.structure = client.structure
        self.scheme = client.scheme

    def getVersion(self):
        """
        Returns name and version of the responsible micro service
        """

        return Utils._getServiceVersion(self, 'authorization')

    def _resolve_where(self, where:str):
        resolvedFilter = ''
        if where != None: 
            resolvedFilter = f'({Utils._resolveWhere(self, where)["topLevel"]})'
        
        return resolvedFilter

    def roles(self, nameFilter: str = None) -> pd.DataFrame:
        """
        Returns a DataFrame of available roles.

        Parameters:
        -----------
        nameFilter : str, optional
            Filters the roles by role name.
        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame with name, id and revision of the role.
        """
        key = 'roles'

        _fields = '''
            id
            name
            revision
        '''

        where_string = "" 
        if nameFilter is not None:
            where_string = f'(where:{{name:{{eq:"{nameFilter}"}}}})'

        graphQLString = f'''query roles {{
            {key} {where_string}
            {{ 
                {_fields}
            }}
        }}'''

        result = Utils._executeGraphQL(self, graphQLString)

        df = pd.json_normalize(result[key])

        return df

    def rules(
        self,
        fields:list=None, 
        where:str=None
        ) -> pd.DataFrame:
        """
        Returns a DataFrame of available rules
        """

        key = 'rules'

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                id
                filter
                revision
                role {{
                    id
                    name
                }}
                accountReference {{
                    ...on GroupReference {{
                        group {{
                            id
                            name
                        }}
                    }}
                    ...on ServiceAccountReference {{
                        serviceAccount {{
                            id
                            name
                        }}
                    }}
                }}
            ''' 

        resolvedFilter = self._resolve_where(where)
        graphQLString = f'''query Rules {{
            {key}{resolvedFilter}  {{
                {_fields}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result[key])
        return df
    
    def addUsers(self, provider_user_ids: list, fields: list = None) -> pd.DataFrame:
        """
        Adds a list of users from Authentik via the provider_users_id to the Authorization-Service users list and returns a data frame with user information.
        Fields defines the values that are returned. By default id, providerSubject, providerUserId and userId are returned.

        Parameters:
        -----------
        provider_user_ids : list
            A list of provider user IDs to add.
        fields: list, optional
            A list of fields to include in the returned DataFrame. If not specified, the default fields will be included.

        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame with user information (Default: id, providerSubject, providerUserId, userId).
        """

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                id
                providerSubject
                providerUserId
                userId
            ''' 

        correlation_id = str(uuid4())
        with logger.contextualize(correlation_id = correlation_id):
            key = 'addUsers'
            graphQLString = f'''mutation {key} {{
                {key}(input: {{
                    providerUserIds: ["{'", "'.join(provider_user_ids)}"]
                }}) {{
                    users {{
                        {_fields}
                    }}
                }}
            }}'''
            result = Utils._executeGraphQL(self, graphQLString, correlation_id)
            if result is None:
                return
            
            df = pd.json_normalize(result[key]['users'])

            return df
        

    
    def addUsersToGroups(self, user_ids: list, group_ids: list, fields: list =  None) -> pd.DataFrame:
        """
        Adds one or more users to one or more groups and returns a pandas DataFrame with user information.
        Fields defines the values that are returned. By default userId and groupIds are returned.

        Parameters:
        -----------
        user_ids : list
            A list of user IDs to add to the groups.
        group_ids : list
            A list of group IDs to add the users to.
        fields : list, optional
            A list of fields to include in the returned DataFrame. If not specified, the default fields will be included.

        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame with user and group information (Default:userId, groupIds).
        """
        correlation_id = str(uuid4())

        if fields is not None:
            if not isinstance(fields, list):
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)
        else:
            _fields = '''
                userId
                groupIds
            '''

        with logger.contextualize(correlation_id=correlation_id):
            key = 'addUsersToGroups'

            user_inputs = []
            for user_id in user_ids:
                for group_id in group_ids:
                    user_inputs.append(f'{{ userId: "{user_id}", groupIds: "{group_id}" }}')
            user_inputs_str = ', '.join(user_inputs)

            graphQLString = f'''mutation {{
                {key}(input: {{users: [{user_inputs_str}], }}) {{
                    users {{
                        {_fields}
                    }}
                }}
            }}'''
            result = Utils._executeGraphQL(self, graphQLString, correlation_id)

            if result is None:
                return pd.DataFrame()

            users = result[key]['users']
            df = pd.DataFrame(users)

        return df


    def getAvailableUsers(self, usernames: list = None, fields: list = None ) -> pd.DataFrame:
        """
        Retrieves available users, including all Users in Authentik, and returns a list with user information. Users can be filtered via the 'usernames' parameter.
        Fields defines the values that are returned. By default providerUserId, eMail and username are returned.
        The username will always be returned.

        Parameters:
        -----------
        usernames : list, optional
            A list of usernames to filter the results by.
        fields : list, optional
            A list of fields to include in the returned DataFrame. If not specified, the default fields will be included.

        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame with user and group information (Default:providerUserId, eMail).
        """

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                providerUserId
                eMail
            ''' 

        correlation_id = str(uuid4())

        with logger.contextualize(correlation_id=correlation_id):
            key = 'availableUsers'
            graphQLString = f'''query {key} {{
                {key} {{
                    username
                    {_fields}
                }}
            }}'''
            result = Utils._executeGraphQL(self, graphQLString, correlation_id)

            if result is None:
                return []

            users = result[key]

            if usernames is not None:
                filtered_users = []
                for user in users:
                    if user['username'] in usernames:
                        filtered_users.append(user)
            users = filtered_users

            df = pd.json_normalize(users)

            return df
        
  
    def addGroups(self, group_names: list, fields: list = None) -> pd.DataFrame:
        """
        Adds a list of groups and returns a pandas DataFrame with group information.
        Fields defines the values that are returned. By default name and id are returned

        Parameters:
        -----------
        group_names : list
            A list of group names to add.
        fields : list, optional
            A list of fields to include in the results. If not specified, the default fields will be included.

        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame with group information (Default:name, id).
        """
        if fields is not None:
            if not isinstance(fields, list):
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)
        else:
            _fields = '''
                name
                id
            '''

        correlation_id = str(uuid4())

        with logger.contextualize(correlation_id=correlation_id):
            key = 'addGroups'
            graphQLString = f'''mutation {{
                {key}(input: {{names: ["{'", "'.join(group_names)}"] }}) {{
                    groups {{
                        {_fields}
                    }}
                }}
            }}'''
            result = Utils._executeGraphQL(self, graphQLString, correlation_id)

            if result is None:
                return pd.DataFrame()

            groups = result[key]['groups']
            df = pd.DataFrame(groups)

            return df


    def users(
        self,
        fields:list=None, 
        where:str=None) -> pd.DataFrame:
        """
        Returns a DataFrame of available users
        """

        key = 'users'

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                id
                name
                username
                providerName
                providerUserId
                revision
            ''' 

        resolvedFilter = self._resolve_where(where)
        graphQLString = f'''query Users {{
            {key}{resolvedFilter}  {{
                {_fields}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result[key])
        return df


    def userGroups(self, filter: str = None) -> pd.DataFrame:
        """
        Returns a DataFrame of available user groups. User Groups can be filtered by name

        Parameters:
        -----------
        filter : str, optional
            Filters the user groups by name.

        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame with user group information. Returns id and name. 
        """
        key = 'groups'

        _fields = '''
            id
            name
        '''
        where_string = "" 
        if filter is not None:
            where_string = f'(where:{{name:{{eq:"{filter}"}}}})'

        graphQLString = f'''query userGroups {{
            {key}{where_string} {{
                {_fields}
            }}
        }}'''

        result = Utils._executeGraphQL(self, graphQLString)

        if result is None:
            return pd.DataFrame()

        df = pd.json_normalize(result[key])

        return df
    

    def updatePermissions(self, group: str, permissions: list, permissionType: str) -> pd.DataFrame:
        
        """
        Updates permissions of a group and returns a pandas DataFrame with permission information.

        Parameters:
        -----------
        group : str
            The name of the group to update the permissions of.
        permissions : list
            A list of permissions to update. Permission are ["ADD","DELETE","READ","UPDATE"]
        permissionType : str
            The type of permission to update. PermissionTypes are "USERS", "USERS_GROUPS", "RULES", "ROLES", "DYNAMIC_OBJECT_TYPES", "SERVICE_ACCOUNTS", "EXTERNAL_RIGHTS" and "PERMISSIONS".

        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame with permission information. Returns groupId, type and id.
        """
        correlation_id = str(uuid4())

       
        _fields = '''
            groupId
            type
            id
        '''

        permission_df = self.getPermissionsOfGroups(filter = group) 
        permissionId = permission_df[permission_df["permissions.type"] == permissionType]["permissions.id"].iloc[0]
        groupId = permission_df["id"].iloc[0]

        with logger.contextualize(correlation_id=correlation_id):
            key = 'updatePermissions'

            graphQLString = f'''mutation {{
                {key}(input: {{permissions: {{groupId:"{groupId}", id:"{permissionId}", permissions: {permissions}, type: {permissionType}}}, }}) {{
                    permissions {{
                        {_fields}
                    }}
                }}
            }}'''
            result = Utils._executeGraphQL(self, graphQLString, correlation_id)
            df = pd.json_normalize(result[key]['permissions'], meta =  ['groupId', 'type', 'id'])
            return df


    def addPermissions(self, group: str, permissions: list, permissionType: str) -> pd.DataFrame:
        """
        Adds one or more permissions to a group and returns a pandas DataFrame with permission information.

        Parameters:
        -----------
        group : str
            The name of the group to add the permissions to.
        permissions : list
            A list of permissions to add to the group. Permission are ["ADD","DELETE","READ","UPDATE"]
        permissionType : str
            The type of permission to add to the group. PermissionTypes are "USERS", "USERS_GROUPS", "RULES", "ROLES", "DYNAMIC_OBJECT_TYPES", "SERVICE_ACCOUNTS", "EXTERNAL_RIGHTS" and "PERMISSIONS".

        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame with permission information. Returns groupId, type and id.
        """
        correlation_id = str(uuid4())

    
        _fields = '''
            groupId
            type
            id
        '''

        groupId = self.userGroups(filter = group )["id"].iloc[0]

        with logger.contextualize(correlation_id=correlation_id):
            
            key = 'addPermissions'
            graphQLString = f'''mutation {{
                {key}(input: {{permissions: {{groupId:"{groupId}", permissions: {permissions}, type: {permissionType}}}}}) {{
                    permissions {{
                        {_fields}
                    }}
                }}
            }}'''
            result = Utils._executeGraphQL(self, graphQLString, correlation_id)
            df = pd.json_normalize(result[key]['permissions'], meta =  ['groupId', 'type', 'id'])
           

        return df


    def getPermissionsOfGroups(self, filter: str = None) -> pd.DataFrame:
        """
        Retrieves all groups and their permissions, permissions can be filtered by group.

        Parameters:
        -----------
        filter : list, optional
            A list of group names to filter the results by.

        Returns:
        --------
        pd.DataFrame
            A pandas DataFrame about permissions and which user group they belong to. 
            Returns name and id of the group, as well as id, permissions, type and revision of the perimissions of each group
        """

       
        _fields =f'''
            name
            id
            permissions{{
                id
                permissions
                type
                revision
            }}
        ''' 

        correlation_id = str(uuid4())
        where_string = "" 
        if filter is not None:
            where_string = f'(where:{{name:{{eq:"{filter}"}}}})'
       
        with logger.contextualize(correlation_id=correlation_id):
            key = 'permissionsOfGroups'
            graphQLString = f'''query {key} 
            {{groups {where_string}
                {{
                    {_fields}
                }}
            }}'''
            result = Utils._executeGraphQL(self, graphQLString, correlation_id)
            df = pd.json_normalize(result["groups"], 'permissions', ["name", "id"], record_prefix="permissions.")
            return df
    
    def serviceAccounts(
        self,
        fields:list=None, 
        where:str=None
        ) -> pd.DataFrame:
        """
        Returns a DataFrame of available service accounts.
        """

        key = 'serviceAccounts'

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                id
                name
            ''' 

        resolvedFilter = self._resolve_where(where)
        graphQLString = f'''query ServiceAccounts {{
            {key}{resolvedFilter}  {{
                {_fields}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result[key])
        return df

    def createRole(
        self,
        inventoryName:str, 
        roleName:str,
        userGroups:list=None, 
        objectPermissions:list=['Create', 'Delete'], 
        propertiesPermissions:list=['Read', 'Update']
        ) -> None:

        """
        Creates a role and sets all rights to all properties

        Parameters:
        ----------
        inventoryName : str
            The name of the inventory for which the new role authorizes rights.
        roleName : str
            Name of the new role.
        userGroup : list = None
            List of user group names. If None, the role will be created without attaching user groups.
        objectPermissions : list = ['Create', 'Delete']
            Default is 'Create' and 'Delete' to allow creating and deleting items of the specified inventory.
            Other entries are not allowed.
        propertiesPermissions : list = ['Read', 'Update']
            Default is 'Read' and 'Update'. All properties will receive 
            the specified rights. Other entries are not allowed.
            Permissions are not extended on referenced inventories!
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):

            # Parameter validation
            try:
                self.client.structure[inventoryName]
            except:
                Utils._error(self, f"Unknown inventory '{inventoryName}'")
                return
            
            try:
                roles = self.roles()
                if roleName in list(roles['name']):
                    Utils._error(self, f"Role '{roleName}' already exists.")
                    return
            except:
                pass

            if isinstance(userGroups, str):
                userGroups = [userGroups]

            if userGroups != None:
                # 'in' is not supported therefore load all groups
                dfUserGroups = self.userGroups()
                falseUserGroups = []
                for group in userGroups:
                    if group not in list(dfUserGroups['name']):
                        falseUserGroups.append(group)
                
                if falseUserGroups:
                    Utils._error(self, f"Unknown user group(s) {falseUserGroups}")
                    return

            # Create role
            properties = self.client.structure[inventoryName]['properties']

            ppstring = '[' + ','.join(map(str.upper, propertiesPermissions)) + ']'
            props = '[\n'
            refProps = '[\n'
            for _, value in properties.items():
                if value["type"] == 'scalar':
                    props += f'{{ propertyId: {Utils._toGraphQL(value["propertyId"])}\n permissions: {ppstring} }}\n'
                elif value["type"] == 'reference':
                    refProps += f'{{ propertyId: {Utils._toGraphQL(value["propertyId"])}\n inventoryId: {Utils._toGraphQL(value["inventoryId"])}\n propertyPermissions: {ppstring}\n inventoryPermissions: [NONE]\n properties: []\n referencedProperties: []\n }}'
            props += ']'
            refProps += ']'
            
            graphQLString= f'''
            mutation AddRole($roleName: String!, $inventoryId: String!, $inventoryPermissions: [ObjectPermission!]!) {{ 
                addRoles (input: {{
                    roles: {{
                        name: $roleName
                        rootInventoryPermission: {{
                            inventoryId: $inventoryId
                            inventoryPermissions: $inventoryPermissions
                            properties: {props}
                            referencedProperties: {refProps}
                            }}
                        }}
                    }})
                    {{
                    roles {{
                        id
                    }}
                }}
            }}
            '''
            params = {
                "roleName": roleName,
                "inventoryId": self.client.structure[inventoryName]['inventoryId'],
                "inventoryPermissions": list(map(str.upper, objectPermissions)),
            }

            result = Utils._executeGraphQL(self, graphQLString, correlationId, params=params)
            if result == None: return

            # if result['addRole']['errors']:
            #     Utils._listGraphQlErrors(result, 'createInventory')
            #     return

            logger.info(f"Role {roleName} created.")

            roleId = result['addRoles']['roles'][0]['id']

            # Create rules
            if userGroups != None:
                for groupname in userGroups:
                    groupId = dfUserGroups.set_index('name').to_dict(orient='index')[groupname]['id']
                    createRuleGqlString= f'''
                    mutation AddRule($roleId: String!, $groupId: String!) {{
                        addRules (input: {{
                            rules: {{
                                roleId: $roleId
                                groupId: $groupId
                                filter: ""
                                filterFormat: EXPRESSION
                                }}
                            }})
                            {{
                            rules {{
                                ruleId
                            }}
                        }}
                    }}
                    '''
                    result = Utils._executeGraphQL(self, createRuleGqlString, correlationId, params={"roleId": roleId, "groupId": groupId})
                    if result != None:
                        logger.info(f"Rule for {roleName} and user group {group} created.")
                    else:
                        logger.error(f"Rule for {roleName} and user group {group} could not be created.")

            return

    def deleteRole(self, role:str) -> None:
        """
        Deletes a role and all related rules.
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):

            # Get Ids of roles and rules
            roles = self.roles().set_index('name')
            roleId = roles.loc[role,'id']

            rules = self.rules()
            rules = rules.set_index('role.name')
            try:
                ruleIds = rules.loc[role,'id']
            except:
                ruleIds = []
            if not isinstance(ruleIds, str):
                ruleIds = list(ruleIds)
            else:
                ruleIds = [ruleIds]

            # First delete rules
            if ruleIds:
                deleteRuleGraphQLString = f'''
                mutation deleteRule($ruleId: String!) {{
                    removeRule(input: {{
                        ruleId: $ruleId
                    }}) {{
                        ruleId
                    }}
                }}
                '''
                for ruleId in ruleIds:
                    result = Utils._executeGraphQL(self, deleteRuleGraphQLString, correlationId, {"ruleId": ruleId})
                    if result != None:
                        logger.info(f"Rule {ruleId} of role {role} with id {ruleId} has been deleted.")
                    else:
                        Utils._error(self, f"Rule {ruleId} of role {roleId} could not be deleted.")
                        return

            # After all rules have been deleted, delete the role
            deleteRoleGraphQLString = f'''
            mutation deleteRole($roleId: String!) {{
                removeRole(input: {{
                    roleId: $roleId
                }}) {{
                    roleId
                }}
            }}
            '''
            result = Utils._executeGraphQL(self, deleteRoleGraphQLString, correlationId, {"roleId": roleId})
            if result != None:
                logger.info(f"Role {role} with id {roleId} has been deleted.")
            else:
                Utils._error(self, f"Role {roleId} could not be deleted.")
            
            return
        

    def addRule(self, role: str, group: str, filter: str) -> str:
        """
        Adds a rule connecting role with usergroup and adds a filter to this rule.

        Parameters:
        -----------
        role : str
            The name of the role associated with the rule.
        group : str
            The name of the group to add the rule to.
        filter : str
            The filter to apply to the rule. The format must be:"Object.porpertyID=filter_value" 

        Returns:
        --------
        str
            The ID of the created rule.
        """
        roleId = self.roles(nameFilter =f'{role}')['id'].iloc[0]
        groupId = self.userGroups(filter =f'{group}')['id'].iloc[0]

        graphqlString = '''
            mutation AddRule($roleId: String!, $groupId: String!, $filter: String!) {
                addRules(input: {
                    rules: {
                        roleId: $roleId
                        groupId: $groupId
                        filter: $filter
                        filterFormat: EXPRESSION
                    }
                }) {
                    rules {
                        ruleId
                    }
                }
            }
        '''

        params = {
            "roleId": roleId,
            "groupId": groupId,
            "filter": filter
        }

        result = Utils._executeGraphQL(self, graphqlString, params=params)

        if result is not None:
            rule_id = result['addRules']['rules'][0]['ruleId']
            logger.info(f"Rule for {role} and user group {groupId} created with ID {rule_id}.")
            return rule_id
        else:
            Utils._error(self, f"Rule could not be created.")
            return ''
