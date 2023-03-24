import requests
import pandas as pd
import os
from datetime import datetime
import re
import boto3
import toml
from dotenv import load_dotenv
import sqlalchemy as sa

#############
# app_config = toml.load('config.toml')
load_dotenv()
user=os.getenv('user')
password=os.getenv('password')
sql_filename = app_config['run']['filename']
# bucketname= app_config['aws']['bucketname']
# foldername= app_config['aws']['foldername']
#############

def read_sql_file(file_path):
    with open(file_path, 'r') as f:
        sql = f.read()
    return sql

sql = read_sql_file(sql_filename)


session = boto3.Session()
s3 = session.resource('s3')
s3_client = session.client('s3')

response = requests.request("GET", url)
results = response.json()['results']
