import json
import requests
from requests.adapters import HTTPAdapter, Retry
from . import db, timer, dataLoadJobHelper

class TaskHelper:
    '''
    setting up basic variables (e.g. dagId or taskId), connections and helper classes.
    This setup method should be more or less static for most of the load jobs from data sources

    :param kwargs: for local usage it is kwargs dictionary in __main__; for Airflow usage it is from op_kwargs of Python Operator
    :param loopAttributes: if attributes from op_attributes which occur in data load jobs should be used in a loop, then provide the attribute number in a list.
    '''
    def __init__(self,kwargs:dict,SCHEMA:list,ENV:str) -> None:
        ####### Getting args 
        # local: kwargs dictionary in __main__
        # Airflow: from op_kwargs of Python Operator
        source = self.__nvl(kwargs,'source')
        databaseConnection = self.__nvl(kwargs,'databaseConnection')
        
        self.LOGGING = {
            'general': [],
            'detail': []
        }
        self.SETTINGS = {
            'dagId': self.__nvl(kwargs,'dagId'),
            'taskId': self.__nvl(kwargs,'taskId'),
            'schema': '_'.join(SCHEMA).lower(),
            'env': ENV
        }
        
        self.TASK_INSTANCE = self.__nvl(kwargs,'ti')

        ####### HTTP Request setup
        self.REQUEST_SESSION = None
        self.customizeRequestSession()

        ####### Database setup
        if source == 'local' and databaseConnection is not None:
            self.CONNECTION = db.connectURI(databaseConnection)
        elif source == 'airflow' and databaseConnection is not None:
            self.CONNECTION = db.connect(databaseConnection.login,databaseConnection.password,databaseConnection.host,databaseConnection.port,databaseConnection.schema)
        else:
            self.CONNECTION = None

        ####### Setup timer
        self.TIMER = timer.Timer()

        self.DATA_LOAD_JOB_HELPER = None

    def setUpDataLoadJobHelper(self,loopAttributes:list=[]):
        if self.SETTINGS.dagId is not None and self.SETTINGS.taskId is not None:
            ####### Setup data load job Helper
            dataLoadJob = db.SELECT_FUNCTION(self.connection,'op_prod','op_create_data_load_job',[self.SETTINGS.dagId,self.SETTINGS.taskId,self.SETTINGS.env])
            self.DATA_LOAD_JOB_HELPER = dataLoadJobHelper.DataLoadJobHelper({
                'loopAttributes': loopAttributes
            })
            self.DATA_LOAD_JOB_HELPER.init(dataLoadJob)
    
    def getParametersForDataLoadJobFinish(self):
        openJobParts = self.DATA_LOAD_JOB_HELPER.getOpenJobParts()
        if len(json.loads(openJobParts)) == 0:
            return [self.SETTINGS.dagId,self.SETTINGS.taskId,self.SETTINGS.env]
        else:
            return [self.SETTINGS.dagId,self.SETTINGS.taskId,self.SETTINGS.env,self.DATA_LOAD_JOB_HELPER.getOpenJobParts()]

    def customizeRequestSession(self,total=5,backoff_factor=1,status_forcelist=[ 502, 503, 504 ]):
        self.REQUEST_SESSION = requests.Session()
        retries = Retry(total=total, backoff_factor=backoff_factor, status_forcelist=status_forcelist)
        self.REQUEST_SESSION.mount('https://', HTTPAdapter(max_retries=retries))

    def __nvl(self,obj,key,default=None):
        if key not in obj:
            return default
        else:
            return obj[key]
    
    def logGeneralInfo(self,message:str):
        self.LOGGING['general'].append(message)

    def logDetailInfo(self,message:str):
        self.LOGGING['detail'].append(message)

    def getLog(self, maxDetailCount=5):
        if maxDetailCount is None:
            detailList = self.LOGGING['detail']
        else:
            totalDetails = len(self.LOGGING['detail'])

            # If the list has fewer items than twice the maxDetailCount, just return the whole list
            if totalDetails <= 2 * maxDetailCount:
                detailList = self.LOGGING['detail']
            else:
                # Calculate the first and last n items
                firstN = self.LOGGING['detail'][:maxDetailCount]
                lastN = self.LOGGING['detail'][-maxDetailCount:]

                # Number of items skipped
                skippedCount = totalDetails - 2 * maxDetailCount

                # Construct the detailList
                detailList = (
                    firstN + 
                    [f"Skipped {skippedCount} items"] + 
                    lastN
                )

        return {
            'general': self.LOGGING['general'],
            'detail': detailList
        }

        
def dataProcessor(limit=10):
    '''
    Returning SQL Query "SELECT * FROM op_prod.op_data_processor(%(dag_id)s,%(task_id)s,%(env)s)".
    However with limit, only n rows of type "detail" are returned

    :param limit: Number of returned rows for with type_str = "detail". If None, all rows are returned.
    '''
    if limit is None:
        sql = 'SELECT * FROM op_prod.op_data_processor(%(dag_id)s,%(task_id)s,%(env)s)'
    else:
        sql=f'''
            SELECT
                  base.key_str
                , base.type_str
                , base.value_str
            FROM
            (
                SELECT 
                      f.key_str
                    , f.type_str
                    , f.value_str
                    , ROW_NUMBER() OVER (PARTITION BY f.key_str ORDER BY f.type_str) AS rn
                FROM op_prod.op_data_processor(%(dag_id)s,%(task_id)s,%(env)s) f
            ) base
            WHERE 1=1
            AND base.type_str = 'general'
            OR base.rn <= {limit}
        '''
    return sql