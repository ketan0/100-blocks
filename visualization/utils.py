#!/usr/bin/env python3

from io import BytesIO
import requests
import pandas as pd
import boto3
from datetime import datetime, timedelta, timezone

def load_google_sheet(google_sheet_url):
    r = requests.get(google_sheet_url)
    data = r.content
    df = pd.read_csv(BytesIO(data), parse_dates=['Timestamp'])
    return df

def load_dynamo_table(table_name, start_dt=None, end_dt=None):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    data = table.scan() # TODO: query+filter with DynamoDB itself (don't load whole table)
    df = pd.DataFrame(data['Items']).sort_values(by='timestamp').reset_index(drop=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    if start_dt:
        df = df[df['timestamp'] >= start_dt]
    if end_dt:
        df = df[df['timestamp'] <= end_dt]
    return df

def next_nearest_activity(timestamp, df, timestamp_column, activity_column):
    activity = df[df[timestamp_column] > timestamp][activity_column].values[0]
    return activity

def extract_blocks(df, timestamp_column='timestamp', activity_column='activity'):
    df[timestamp_column] = pd.to_datetime(df[timestamp_column])
    start = df[timestamp_column].iloc[0]
    end = df[timestamp_column].iloc[-1]
    block_start_times = pd.date_range(start=start, end=end, freq='10min')
    blocks = [next_nearest_activity(
        ts,
        df,
        timestamp_column,
        activity_column
    ) for ts in block_start_times]
    return blocks
