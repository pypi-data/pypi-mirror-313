from uuid import uuid4
import pandas as pd
from loguru import logger

from .utils.ut import Utils
from .utils.ut_autprog import AutProgUtils
from .utils.ut_auth import AuthData


class Automation():

    def __init__(self, endpoint: str, client: object, auth_data: AuthData) -> None:

        self.raiseException = client.raiseException
        self.defaults = client.defaults

        self.endpoint = endpoint
        self.proxies = client.proxies
        self.auth_data = auth_data

    def getVersion(self):
        """
        Returns name and version of the responsible micro service
        """

        return Utils._getServiceVersion(self, 'automation')

    def _resolve_where(self, where: str):
        resolvedFilter = ''
        if where != None:
            resolvedFilter = Utils._resolveWhere(self, where)["topLevel"]

        return resolvedFilter

    def workflows(self) -> pd.DataFrame:
        """Returns a DataFrame of all Workflows"""

        graphQLString = f'''query workflows {{
            workflows {{
                id
                name
                description
                }}
            }}
            '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None:
            return

        df = pd.json_normalize(result['workflows'])
        return df

    def workflowInstances(self, workflowId: str = None, fromTimepoint: str = None, toTimepoint: str = None,
                          fields: list = None, where: str = None, showTasks=False, skip=0, maxResults=50) -> pd.DataFrame:
        """Shows Instances of a workflow. If workflowId=None, all Instances of all workflows will be returned.

        Parameters:
        -----------
        workflowId : str
            The id of the workflow.
        fromTimepoint : str
            Filter on instances started after this timepoint (format: "%Y-%m-%dT%H:%M:%S.%fZ").
        toTimepoint : str
            Filter on instances ended before this timepoint (format: "%Y-%m-%dT%H:%M:%S.%fZ").
        fields : list
            A list of all properties to be queried. If None, all properties will be queried.
        where : str
            Filter based on query string. Examples: 'state eq COMPLETED', 
        showTasks : bool
            If True, the tasks of the workflow instances will be shown.
        skip : int
            Offset pagination: skip the first n instances.
        maxResults : int
            Offset pagination: take up to the first n instances.
        """

        meta = ['id', 'name', 'businessKey',
                'version', 'startTime', 'endTime', 'state']
        key = 'workflowInstances'

        if workflowId != None:
            _workflowId = f'workflowId: "{workflowId}"'
        else:
            _workflowId = ''

        if fromTimepoint != None:
            _fromTimepoint = f'from: "{fromTimepoint}"'
        else:
            _fromTimepoint = ''

        if toTimepoint != None:
            _toTimepoint = f'to: "{toTimepoint}"'
        else:
            _toTimepoint = ''

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)
        else:
            _fields = f'''
                id
                workflowId
                name
                businessKey
                version
                startTime
                endTime
                duration
                state
                variables {{
                    name
                    value
                    time
                }}'''

        resolvedFilter = ''
        if where != None:
            resolvedFilter = self._resolve_where(where)

        if showTasks != False:
            _tasks = f'''tasks {{
                            id
                            topic
                            workerId
                            timestamp
                            state
                            retries
                            errorMessage
                        }}'''
        else:
            _tasks = ''

        graphQLString = f'''query Instances {{
            {key}(skip: {skip} take: {maxResults} {_workflowId} {_fromTimepoint} {_toTimepoint} {resolvedFilter}) {{
            items {{
                {_fields}
                {_tasks}
                }}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None:
            return

        if showTasks != False:
            df = pd.json_normalize(result[key]['items'], meta=meta, record_path=[
                                   'tasks'], record_prefix='task.', errors='ignore')
            if 'startTime' in df.columns:
                df = df.sort_values(by='startTime', ascending=False)
        else:
            df = pd.json_normalize(result[key]['items'])
            if 'startTime' in df.columns:
                df = df.sort_values(by='startTime', ascending=False)
        return df

    def createWorkflow(self, id, name, description: str = None):

        correlationId = str(uuid4())
        context_logger = logger.bind(correlation_id=correlationId)

        graphQLString = f'''mutation createWorkflow {{
            createWorkflow(
                input: {{
                    id: "{id}"
                    name: "{name}"
                    description: "{description}"
                }}
                ) {{
                    ...on CreateWorkflowError {{
                    message
                    }}
                    ... on WorkflowCreated {{
                        workflow {{
                            id
                        }}
                    }}
                }}
            }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None:
            return

        context_logger.info(f"New workflow {id} created.")

        return result

    def deployWorkflow(self, workflowId: str, filePath: str) -> None:
        """Deploys a Camunda XML to an existing workflow"""

        correlationId = str(uuid4())
        context_logger = logger.bind(correlation_id=correlationId)

        fileContent = Utils._encodeBase64(filePath)
        context_logger.debug(f"fileContent: {fileContent[:10]}")

        graphQLString = f'''mutation deployWorkflow {{
            deployWorkflow(
                input: {{
                    fileContentBase64: "{fileContent}"
                    workflowId: "{workflowId}"
                }}
            ) {{
                ... on DeployWorkflowError {{
                    message
                }}
                ... on InvalidWorkflowProcessId {{
                    processId
                    workflowId
                    message
                }}
                ... on WorkflowDeployed {{
                    version
                }}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None:
            return

        context_logger.info(f"Workflow '{workflowId}' deployed.")
        return result

    def startWorkflow(self, workflowId: str, businessKey: str, inputVariables: dict = None):
        """Starts a workflow"""

        correlationId = str(uuid4())
        context_logger = logger.bind(correlation_id=correlationId)

        if inputVariables == None:
            _vars = ''
        else:
            _vars = AutProgUtils._varsToString(inputVariables, 'input')

        graphQLString = f'''
            mutation ExecuteWF {{
                startWorkflow(input: {{ 
                    businessKey: "{businessKey}"
                    workflowId: "{workflowId}" 
                    {_vars}
                    }}
                ) {{
                    ... on ProcessDefinitionNotFound {{
                        workflowId
                        message
                        }}
                    ... on StartWorkflowError {{
                            message
                            }}
                    ... on WorkflowStarted {{
                        workflowInstanceId
                        }}
                    }}
                }}
            '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None:
            return

        context_logger.info(f"Workflow {workflowId} started.")

        return result

    def deleteWorkflow(self, workflowId: str):
        """Deletes a workflow"""

        correlationId = str(uuid4())
        context_logger = logger.bind(correlation_id=correlationId)

        graphQLString = f'''mutation deleteWorkflow {{
            deleteWorkflow (id: "{workflowId}")
            {{
                ... on DeleteWorkflowError {{
                    message
                    }}
                ...on WorkflowDeleted {{
                    success
                    }}
                ... on WorkflowNotFound {{
                    workflowId
                    message
                    }}
                
                }}
            }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        context_logger.info(f"Workflow {workflowId} deleted.")
        return result

    def terminateWorkflowInstance(self, workflowInstanceId):
        """Terminates a workflow instance"""

        correlationId = str(uuid4())
        context_logger = logger.bind(correlation_id=correlationId)

        graphQLString = f'''mutation terminateWorkflowInstance {{
            terminateWorkflowInstance(
                workflowInstanceId:"{workflowInstanceId}") {{
                ...on TerminateWorkflowInstanceError {{
                    message
                    }}
                ...on WorkflowInstanceNotFound {{
                    workflowInstanceId
                    message
                    }}
                ...on WorkflowInstanceTerminated {{
                    success
                    }}
                }}
            }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        context_logger.info(f"Workflow instance {workflowInstanceId} started.")
        return result

    def updateWorkflow(self, workflowId: str, name: str = None, description: str = None):
        """Updates a workflow (name and description can be changed)"""

        correlationId = str(uuid4())
        context_logger = logger.bind(correlation_id=correlationId)

        name = Utils._argNone('name', name)
        description = Utils._argNone('description', description)

        key = 'updateWorkflow'
        graphQLString = f'''mutation updateWorkflow {{
            {key}(workflowId: "{workflowId}", properties: {{
                {description}
                {name}
                }}) {{
                    ... on UpdateWorkflowError {{
                    message
                    }}
                    ... on WorkflowNotFound {{
                    workflowId
                    message
                    }}
                    ... on WorkflowUpdated {{
                    workflow {{
                        id
                        name
                        description
                        }}
                    }}
                }}
            }}
            '''

        result = Utils._executeGraphQL(self, graphQLString)
        context_logger.info(f"Workflow {workflowId} updated.")
        return result

    def retryTasks(self, externalTaskIds: list):
        """
        Retries task instances of a workflow instance.

        Parameters:
        ----------
        externalTaskIds: list
            External task ids of the tasks to be retried.
        
        Remark: Get ids from instances in state INCIDENT like this:
        >>> ids = workflowInstances(workflow_id, where='state eq INCIDENT', fields='tasks.id')
        >>> retryTasks(['2fb2bd12-9b61-11ee-81c2-7eb9c6d765ed', '52e9c8b9-9b61-11ee-81c2-7eb9c6d765ed'])
        """
        key = 'retryTasks'

        correlationId = str(uuid4())
        context_logger = logger.bind(correlation_id=correlationId)

        graphQLString = f'''mutation retryTasks($ids: [String]!) {{
            {key}(externalTaskIds: $ids) {{
                ... on RetryTasksError {{
                    message
                }}
                ...on TasksNotFound {{
                    message
                }}
                ... on TasksRetried {{
                    success
                }}
            }}
        }}
        '''
        params = {
            "ids": externalTaskIds
        }

        result = Utils._executeGraphQL(self, graphQLString, correlationId=correlationId, params=params)
        context_logger.info(f"Tasks {','.join(externalTaskIds)} retried.")
        return result

    def retryTask(self, externalTaskId):
        """
        Retries a task instance of a workflow instance.

        Parameters:
        ----------
        externalTaskId: str
            External task id of the task to be retried.
        
        Example:
        >>> retryTask('2fb2bd12-9b61-11ee-81c2-7eb9c6d765ed')
        """
        return self.retryTasks([externalTaskId])
