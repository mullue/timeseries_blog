import boto3, time, s3fs, json, warnings
from datetime import date, timedelta
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import sagemaker
from sagemaker.predictor import RealTimePredictor
from sagemaker.tuner import HyperparameterTuner, ContinuousParameter, IntegerParameter
from smexperiments import experiment
from multiprocessing import Pool

from IPython.display import display, HTML, Javascript

from bokeh.plotting import curdoc, figure, output_notebook, show
from bokeh.layouts import column, row, layout
from bokeh.models import GeoJSONDataSource, ColumnDataSource
from bokeh.models import Select, Slider
from bokeh.models.callbacks import CustomJS
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
from bokeh.palettes import inferno


# to skip querying raw data multiple times, provide and id to a previously run query 
results_uri = None

# the external Athena table only needs to be created once, set this to False to avoid error message
create_table_uri = None

# if a training job name is given, then no hpo training will occur
training_job_name = 'forecasting-deepar-200707-0838-046-f1fa5ffa'

# if an endpoint name is given, then no endpoint will be created
endpoint_name = 'forecasting-deepar-200707-0838-046-f1fa5ffa' 

# the train test split date is used to split each time series into train and test sets
train_test_split_date = date.today() - timedelta(days=30)#).strftime('%y-%m-%d 00:00:00')

# the sampling frequency determines the number of hours per sample
# and is used for aggregating and filling missing values
frequency = '1' # hours

# prediction length is how many hours into future to predict values for
prediction_length = 48

# context length is how many prior time steps the predictor needs to make a prediction
context_length = 3

# flag to generate predictions or get them from a file
generate_predictions = False

# the test dates to generate predictions for
test_start_date = '2020-05-01 00:00:00'

# how many period to create predictions for
test_periods = 168

# date to start graphing data
graph_start_date = '2020-05-02 00:00:00'

# date to stop graphing data
graph_end_date = '2020-05-12 00:00:00'

# the file to save predictions to
predictions_file = 'data/predictions.pkl'

# quantiles that will be predicted
quantiles = range(5,10) 

warnings.filterwarnings('ignore')

session = boto3.Session()
region = session.region_name
account_id = session.client('sts').get_caller_identity().get('Account')
bucket_name = f"{account_id}-openaq-lab"
console_s3_uri= 'https://s3.console.aws.amazon.com/s3/object/'
s3 = boto3.client('s3')
try:
    s3.create_bucket(Bucket=bucket_name)
except:
    pass


def athena_create_table(query_file, wait=None):
    global create_table_uri
    create_table_uri = athena_execute(query_file, create_table_uri, 'txt', wait)
    return create_table_uri
 
    
def athena_query_table(query_file, wait=None):
    global results_uri
    results_uri = athena_execute(query_file, results_uri, 'csv', wait)
    return results_uri


def athena_execute(query_file, results_uri, ext, wait):
    '''Define Athena query helper function. To make querying simpler, define a reusable query function for Athena that will block until the query finishes. 
    '''    
    with open(query_file) as f:
        query_str = f.read()  
        
    if results_uri == None:
        display(HTML(f'Executing query:<br><br><code>{query_str}</code><br><br>'))
        
        athena = boto3.client('athena')
        s3_dest = f's3://{bucket_name}/athena/results/'
        query_id = athena.start_query_execution(
            QueryString= query_str, 
            ResultConfiguration={'OutputLocation': s3_dest}
        )['QueryExecutionId']
        
        results_uri = f'{s3_dest}{query_id}.{ext}'
        
        start = time.time()
        while wait == None or wait == 0 or time.time() - start < wait:
            result = athena.get_query_execution(QueryExecutionId=query_id)
            status = result['QueryExecution']['Status']['State']
            if wait == 0 or status == 'SUCCEEDED':
                break
            elif status in ['QUEUED','RUNNING']:
                continue
            else:
                raise Exception(f'query {query_id} failed with status {status}')

            time.sleep(1)
    else:
        display(HTML(f'Results from previously executed query:<br><br><code>{query_str}</code><br><br>'))   

    console_url = f'{console_s3_uri}{bucket_name}/athena/results/{query_id}.{ext}?region={region}&tab=overview'
    display(HTML(f'results are located at <a href="{console_url}">{results_uri}</a>'))
    
    return results_uri

def filter_dates(df, min_time, max_time, frequency):
    min_time = None if min_time is None else pd.to_datetime(min_time)
    max_time = None if max_time is None else pd.to_datetime(max_time)
    interval = pd.Timedelta(frequency)
    
    def _filter_dates(r): 
        if min_time is not None and r['start'] < min_time:
            start_idx = int((min_time - r['start']) / interval)
            r['target'] = r['target'][start_idx:]
            r['start'] = min_time
        
        end_time = r['start'] + len(r['target']) * interval
        if max_time is not None and end_time > max_time:
            end_idx = int((end_time - max_time) / interval)
            r['target'] = r['target'][:-end_idx]
            
        return r
    
    filtered = df.apply(_filter_dates, axis=1) 
    filtered = filtered[filtered['target'].str.len() > 0]
    return filtered

def get_tests(features, split_dates, frequency, context_length, prediction_length):
    tests = []
    end_date_delta = pd.Timedelta(f'{frequency} hour') * context_length
    prediction_id = 0
    for split_date in split_dates:
        context_end = split_date + end_date_delta
        test = filter_dates(features, split_date, context_end, frequency)
        test['prediction_start'] = context_end
        test['prediction_id'] = prediction_id
        tests.append(test)
        prediction_id += 1
        
    tests = pd.concat(tests).reset_index().set_index(['id', 'prediction_id', 'prediction_start']).sort_index()
    return tests

def init_predict_process(func, endpoint_name, quantiles):
    func.predictor = RealTimePredictor(endpoint_name)
    func.quantiles = quantiles
    
def call_endpoint(feature):
    feature['start'] = feature['start'].strftime('%Y-%m-%d %H:%M:%S')
    request = json.dumps(dict(
        instances= [feature],
        configuration= dict(
            num_samples= 100,
            output_types= [quantiles],
            quantiles= call_endpoint.quantiles
        )   
    )).encode('utf-8')
    
    response = json.loads(call_endpoint.predictor.predict(request).decode('utf-8'))
            
    raw_quantiles = response['predictions'][0]['quantiles']
    return {q: [[np.around(v, 2) for v in l]] for q,l in raw_quantiles.items()}      

def predict(endpoint_name, samples, quantiles, processes=10):
    features = samples[['start', 'target', 'cat']].to_dict(orient='records')
    with Pool(processes, init_predict_process, [call_endpoint, endpoint_name, quantiles]) as pool:
        inferences = pool.map(call_endpoint, features)
      
    df = pd.concat([pd.DataFrame(inference) for inference in inferences], ignore_index=True)                          
    df = df[sorted(df.columns.values)]
    df.set_index(samples.index, inplace=True)
    df.index.names = ['id', 'prediction_id', 'start']
    df.reset_index(level=2, inplace=True)
    return df

def create_indexdb_tables():
    with open('javascript/create_table.js', 'r') as f:
        create_table_script = f.read()
        display(Javascript(create_table_script))

def index_prediction_data():
    with open('javascript/index_data.js', 'r') as f:
        index_script = f.read()
        
    def exec_js(actual_strs, prediction_strs):
        actual_str = '['+','.join(actual_strs)+']'
        prediction_str = '['+','.join(prediction_strs)+']'
        display(Javascript(f"""
            {index_script}
            index_data('openaq','actuals', {actual_str});
            index_data('openaq','predictions', {prediction_str});
        """))
             
    actual_strs = []
    prediction_strs = []
    last_actual_lid = None
    for index, row in filtered_predictions.reset_index().iterrows():
        lid = row['id']
        
        if last_actual_lid != lid:
            actual_row = actuals.loc[lid]
            start = actual_row['start'].strftime('%Y-%m-%dT%H:%M:%SZ')
            target_str = json.dumps(actual_row['target'])
            actual_strs.append('{' + f'id:"{lid}",start:"{start}",target:{target_str}' + '}')
            last_actual_lid = lid
        
        pid = row['prediction_id']
        start = row['start'].strftime('%Y-%m-%dT%H:%M:%SZ')
        quantile_results = []
        for q in range(1,10):
            quantile = f'0.{q}'  
            if quantile in row:
                values = json.dumps(row[quantile])
                quantile_results.append(f'"{quantile}":{values}')
        
        prediction_str = ','.join(quantile_results)
        prediction_strs.append('{' + f'id:"{lid}:{pid}",start:"{start}",{prediction_str}' + '}')
        
        if len(prediction_strs) == 100:
            exec_js(actual_strs, prediction_strs)
            actual_strs = []
            prediction_strs = []
            
    if len(actual_strs):
        exec_js(actual_strs, prediction_strs)