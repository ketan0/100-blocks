#!/usr/bin/env python3

from io import BytesIO
import requests
import pandas as pd
import boto3


def load_google_sheet(google_sheet_url):
    r = requests.get(google_sheet_url)
    data = r.content
    df = pd.read_csv(BytesIO(data), parse_dates=['Timestamp'])
    return df[35:65]

def load_dynamo_table(table_name):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    data = table.scan() # TODO: query+filter for only stuff during a certain day
    df = pd.DataFrame(data['Items']).sort_values(by='timestamp').reset_index(drop=True)
    return df

def next_nearest_activity(timestamp, df, timestamp_column, activity_column):
    activity = df[df[timestamp_column] > timestamp][activity_column].values[0]
    # print(f'Most recent activity after {timestamp} is {activity}')
    return activity

def extract_blocks(df, timestamp_column='timestamp', activity_column='activity'):
    df[timestamp_column] = pd.to_datetime(df[timestamp_column])
    start = df[timestamp_column].iloc[0]
    end = df[timestamp_column].iloc[-1]
    # print('start: ', start)
    # print('end: ', end)
    activity_ids = {activity: i for i, activity in enumerate(df[activity_column].unique())}
    # print(f'activity ids: {activity_ids}')
    block_start_times = pd.date_range(start=start, end=end, freq='10min')
    blocks = [activity_ids[next_nearest_activity(
        ts,
        df,
        timestamp_column,
        activity_column
    )] for ts in block_start_times]
    return blocks, activity_ids
