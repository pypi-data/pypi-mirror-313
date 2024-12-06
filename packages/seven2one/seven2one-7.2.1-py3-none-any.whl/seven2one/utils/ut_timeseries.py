from itertools import islice
import pandas as pd
import pytz
from loguru import logger
from .ut import Utils
import math

gq = Utils._toGraphQL


class UtilsTimeSeries():

    def _tsCollectionToString(collection: list) -> str:
        """Converts a list of dicts with time series data into graphQL string"""

        tsData = '[\n'
        for item in collection:
            tsData += '{\n'
            for key, value in item.items():
                if key in ['sys_inventoryId', 'sys_inventoryItemId']:
                    tsData += f'  {key}: "{value}"\n'
                elif key == 'data':
                    tsData += '  data: {\n'
                    for dkey, dvalue in value.items():
                        if dkey == 'resolution':
                            tsData += f'''  resolution: {{timeUnit: {dvalue['timeUnit']}, factor: {dvalue['factor']}}}\n'''
                        elif dkey == 'unit':
                            tsData += f'''  unit: "{dvalue}"\n'''
                        elif dkey == 'dataPoints':
                            tsData += '    dataPoints: [\n'
                            for dp_key in dvalue:
                                if 'flag' not in dp_key:
                                    value = dp_key['value']
                                    if (value is None) or (isinstance(value, float) and math.isnan(value)):
                                        tsData += f'''     {{timestamp: "{dp_key['timestamp']}", value: 0 flag: MISSING}}\n'''
                                    else:
                                        tsData += f'''     {{timestamp: "{dp_key['timestamp']}", value: {value}}}\n'''
                                else:
                                    tsData += f'''     {{timestamp: "{dp_key['timestamp']}", value: {dp_key['value']}, flag: {dp_key['flag']}}}\n'''
                            tsData += '    ]\n'
                        else:
                            pass
                    tsData += '  }\n'
                else:
                    pass
            tsData += '}\n'
        tsData += ']\n'
        return tsData

    def _dataPointsToString(dataPoints: dict) -> str:
        """Converts a dictionary of datapoints to GraphQL string"""

        _dataPoints = ''
        for timestamp, value in dataPoints.items():
            if (value is None) or (isinstance(value, float) and math.isnan(value)):
                _dataPoints += f'{{ timestamp: {gq(timestamp)} value: 0 flag: MISSING }}\n'
            else:
                _dataPoints += f'{{ timestamp: {gq(timestamp)} value: {gq(value)} }}\n'

        return _dataPoints

    def _sliceDataPoints(dataPoints: dict, start: int, stop: int):
        """Return a slice of the dataPoints dictionary"""

        return dict(islice(dataPoints, start, stop))

    def _processDataFrame(
        self,
        result: dict,
        dataFrame: pd.DataFrame,
        fields: list,
        timeZone: pytz.timezone,
        displayMode: str,
        includeMissing: bool
    ) -> pd.DataFrame:
        """
        Creates a time Series DataFrame for different time series data methods
        """
        df = dataFrame
        if df.empty:
            logger.info('The query did not produce results.')
            return df
        df.loc[(df.flag == 'MISSING'), 'value'] = math.nan

        if displayMode == 'pivot':
            #pivot needs values to be set, so replace all None values with 'N/A'!
            df[fields] = df[fields].fillna('N/A')
            
            if includeMissing == False:
                df = df.pivot_table(index='timestamp', columns=fields, values='value', dropna=True)
            elif len(fields)>1:
                # Get a list of all valid combinations and pivot df
                valid_combinations = df.groupby(fields).size().reset_index()
                list_valid_combinations = list(valid_combinations[fields].itertuples(index=False, name=None))
                df = df.pivot_table(index='timestamp', columns=fields, values='value', dropna=False)
                # Remove all combinations, that don't exist
                df = df.loc[:, list_valid_combinations]
            else:
                df = df.pivot_table(index='timestamp', columns=fields, values='value', dropna=False)

            if len(df.columns) == 0:
                logger.warning(
                    f"Could not pivot DataFrame. Try different properties for fields-argument or use displayMode='rows'")
                return
            df.index = pd.to_datetime(
                df.index, format='%Y-%m-%dT%H:%M:%S').tz_convert(pytz.timezone(timeZone))
            if self.defaults.useDateTimeOffset == False:
                df.index = df.index.tz_localize(tz=None)

            columnNumber = len(result)
            dfColumnNumber = len(df.columns)
            if len(df.columns) < len(result):
                logger.info(
                    f"{columnNumber-dfColumnNumber} columns omitted due to duplicate column headers or NaN-columns.")
            return df

        elif displayMode == 'rows':
            df.set_index('timestamp', inplace=True)
            df.index = pd.to_datetime(
                df.index, format='%Y-%m-%dT%H:%M:%S').tz_convert(pytz.timezone(timeZone))
            if self.defaults.useDateTimeOffset == False:
                df.index = df.index.tz_localize(tz=None)
            return df

        else:
            Utils._error(
                self, msg=f"Unknown displayMode '{displayMode}'. Use 'pivot' or 'rows'.")
            return

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
                if item == ['resolution']:
                    continue
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

        fields += f'resolution {{timeUnit, factor}}  \n'
        fields += f'_dataPeriod {{from, to}}  \n'
        return fields
