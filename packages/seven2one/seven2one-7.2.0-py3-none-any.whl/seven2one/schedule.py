from uuid import uuid4
import pandas as pd
from datetime import datetime, timedelta
from loguru import logger

from .utils.ut import Utils
from .utils.ut_auth import AuthData


class Schedule():
    def __init__(self, endpoint: str, client: object, auth_data: AuthData) -> None:

        self.raiseException = client.raiseException
        self.defaults = client.defaults
        self.auth_data = auth_data
        self.endpoint = endpoint
        self.proxies = client.proxies

    def getVersion(self):
        """
        Returns name and version of the responsible micro service
        """

        return Utils._getServiceVersion(self, 'schedule')

    def _resolve_where(self, where: str):
        resolvedFilter = ''
        if where != None:
            resolvedFilter = f'({Utils._resolveWhere(self, where)["topLevel"]})'

        return resolvedFilter

    def schedules(
            self,
            fields: list = None,
            where: str = None) -> pd.DataFrame:
        """
        Returns schedules in a DataFrame

        Parameters:
        -----------
        fields: list | str = None
            A list of all properties to be queried. If None, all properties will be queried.
        where: str = None
            Use a string to add where criteria like
            ''workflowId eq "meteoData"'.

        Example:
        --------
        >>> Schedule.schedules(
                where='workflowId == "meteoData"', 
                fields=['name', 'cron', 'timeZone']
            )   
        """

        key = 'schedules'

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)
        else:
            _fields = f'''scheduleId
                name
                description
                workflowId
                businessKey
                cron
                timeZone
                isActive
                nextFireTime
                variables {{
                    key
                    value
                }}'''

        resolvedFilter = ''
        if where != None:
            resolvedFilter = self._resolve_where(where)

        graphQLString = f'''query schedules {{
            {key}{resolvedFilter}  {{
                {_fields}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None:
            return

        df = pd.json_normalize(result[key])
        return df

    def createSchedule(self, name: str, workflowId: str, businessKey: str, cron: str,
                       isActive: bool = True, description: str = None, variables: dict = None, timeZone: str = None) -> str:
        """Creates a schedule and returns the schedule Id"""

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):

            if isActive == True:
                isActive = 'true'
            else:
                isActive = 'false'

            if description != None:
                description = description
            else:
                description = ''

            if timeZone == None:
                timeZone = ''

            if variables != None:
                _variables = 'variables: [\n'
                for k, v in variables.items():
                    _variables += f'{{key: "{k}", value: "{v}"}}\n'
                _variables += ']'
            else:
                _variables = ''

            graphQLString = f'''mutation createSchedule {{
                createSchedule(input:{{
                    name: "{name}"
                    workflowId: "{workflowId}"
                    businessKey: "{businessKey}"
                    cron: "{cron}"
                    timeZone: "{timeZone}"
                    description: "{description}"
                    isActive: {isActive}
                    {_variables}      
                }})
                {{
                    schedule {{
                        scheduleId
                    }}
                    errors {{
                        message
                    }}
                }}
            }}'''

            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            logger.debug(graphQLString)
            if result == None:
                return

            key = 'createSchedule'
            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
            else:
                scheduleId = result[key]['schedule']['scheduleId']
                logger.info(f"New schedule {scheduleId} created.")

            return scheduleId

    def updateSchedule(self, scheduleId, name: str = None, workflowId: str = None, businessKey: str = None,
                       cron: str = None, isActive: bool = None, description: str = None, variables: dict = None, timeZone: str = None) -> None:
        """
        Updates a schedule. Only arguments that ar not None will overwrite respective fields.

        Parameters:
        -----------
        scheduleId : str
            The Id of the schedule that is to be updated.
        name : str
            The name of the schedule.
        workflowId : str
            The Id of the workflow that shall be executed with this schedule.
        cron : str
            The cron expression. For detailed information loop up
            http://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html
        isActive : bool
            Determines, if the schedule should execute the workflow or not.
        description : str
            A description of the schedule.
        variables : dict
            A dictionary of variables that are used by tasks in the workflow.
        timeZone : str
            IANA time zone Id the schedule cron is evaluated in. If empty the installed default is used.
            e.g. 'Europe/Berlin', 'UTC'

        Example:
        --------
        >>> vars = {
                'var1': 99,
                'var2': "AnyString"
            }
        >>> client.Scheduler.updateSchedule('112880211090997248', name='test_schedule',
                isActive=True, variables=vars)

        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):

            updateScheduleArgs = ''

            if name != None:
                updateScheduleArgs += f'name: "{name}"\n'
            if workflowId != None:
                updateScheduleArgs += f'workflowId: "{workflowId}"\n'
            if businessKey != None:
                updateScheduleArgs += f'businessKey: "{businessKey}"\n'
            if cron != None:
                updateScheduleArgs += f'cron: "{cron}"\n'
            if isActive != None:
                updateScheduleArgs += f'isActive: {str(isActive).lower()}\n'
            if description != None:
                updateScheduleArgs += f'description: "{description}"\n'
            if timeZone != None:
                updateScheduleArgs += f'timeZone: "{timeZone}"\n'

            if variables != None:
                _variables = 'variables: [\n'
                for k, v in variables.items():
                    _variables += f'{{key: "{k}", value: "{v}"}}\n'
                _variables += ']'
                updateScheduleArgs += _variables

            graphQLString = f'''mutation updateSchedule {{
                updateSchedule(
                    scheduleId: "{scheduleId}"
                    input:{{
                        {updateScheduleArgs}
                }})
                {{
                    errors {{
                        message
                    }}
                }}
            }}'''

            result = Utils._executeGraphQL(self, graphQLString, correlationId)
            logger.debug(graphQLString)
            if result == None:
                return

            key = 'updateSchedule'
            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
            else:
                logger.info(f"Schedule {scheduleId} updated.")

            return

    def deleteSchedule(self, scheduleId: str, force: bool = False):
        """Deletes a schedule"""

        if force == False:
            confirm = input(f"Press 'y' to delete schedule '{scheduleId}': ")

        graphQLString = f'''mutation deleteSchedule {{
            deleteSchedule (scheduleId: "{scheduleId}")
            {{
                errors {{
                message
                }}
            }}
        }}
        '''

        if force == True:
            confirm = 'y'
        if confirm == 'y':
            result = Utils._executeGraphQL(self, graphQLString)
            if result == None:
                return

            key = 'deleteSchedule'
            if result[key]['errors']:
                Utils._listGraphQlErrors(result, key)
            else:
                logger.info(f"Schedule {scheduleId} deleted")
                return None

    def nextFireTimes(self, workflowId: str, fromTimepoint: str = None, toTimepoint: str = None, count: int = None):
        """Show next fire times of a workflow"""

        if fromTimepoint == None:
            fromTimepoint = datetime.today().isoformat()

        if toTimepoint == None:
            toTimepoint = datetime.today() + timedelta(days=3)

        if count == None:
            _count = ''
        else:
            _count = f'count: {count}'

        graphQLString = f'''query nextFireTimes {{
            nextFireTimes (
                workflowId: "{workflowId}",
                from: "{fromTimepoint}", 
                to: "{toTimepoint}",
                {_count}
                
                ) {{
                scheduleId
                fireTime
                }}
            }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None:
            return

        df = pd.json_normalize(result['nextFireTimes'])

        return df
