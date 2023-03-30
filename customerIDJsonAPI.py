import requests
import pandas as pd
import os
from datetime import datetime
import re
import boto3
import toml
from dotenv import load_dotenv
import sqlalchemy as sa

from sqlalchemy import text
import json 
#############
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

CustomerQuery = '''select c.customerID,sum(Sales) SumOfSales from superstore.customers c
left join superstore.orders o on c.customerID = o.customerID
group by c.customerID
order by sum(Sales) desc
limit 10'''
#############

engine = sa.create_engine(f'mysql+pymysql://{user}:{password}@{hostname}:{port}/{database}')

with engine.connect() as conn:

    resultsDF = pd.read_sql(text(CustomerQuery), conn)


session = boto3.Session()
s3 = session.resource('s3')
s3_client = session.client('s3')
print('S3 Client Connected!')

resultsDF.to_json('input/'+aws_filename)

s3_client.upload_file('input/'+aws_filename, bucketname, foldername+aws_filename)
print(aws_filename,'File Uploaded to Bucket',bucketname,foldername)
