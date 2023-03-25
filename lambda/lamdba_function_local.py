import requests
import pandas as pd
import json 
import sqlalchemy as sa
from dotenv import load_dotenv
from datetime import date
import os
import toml 
import subprocess
from sqlalchemy import text
#####
app_config = toml.load('config.toml')
load_dotenv()
user=os.getenv('user')
password=os.getenv('password')

sql_filename = app_config['sql']['filename']
hostname = app_config['sql']['hostname']
port = app_config['sql']['port']
database = app_config['sql']['database']

bucketname= app_config['s3']['bucketname']
foldername= app_config['s3']['foldername']
aws_filename= app_config['s3']['filename']

api_url = app_config['api']['url']
######

def mysql_connect(host, user, password, database, port,schema):
    """
    Connect to the database
    """
    engine = sa.create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{database}')

    return engine

def get_custID(filepath):
    df = pd.read_json(filepath)
    CustID = tuple(df['customerID'].to_list())
    return CustID

def get_customer_data_to_json(engine, sql):
    """
    Get customer data from database with pandas way
    """
    df=pd.read_sql(sql, con=engine)
    data=df.to_json(orient='records')
    return data

if __name__== "__main__": 

    subprocess.call(['aws', 's3', 'cp', 's3://' + bucketname + '/' + foldername + aws_filename, 'download/' + aws_filename])
    
    CustID = get_custID('download/' + aws_filename)

    engine = mysql_connect(hostname, user, password, database, port, database)
    sql=f"""select customerID, CustomerName
            from customers
            where customerID in {CustID}
         """
    
    with engine.connect() as conn:
        data = get_customer_data_to_json(conn, text(sql))

    request = requests.post(api_url, data=data)
    print(request.status_code)
    print(request)