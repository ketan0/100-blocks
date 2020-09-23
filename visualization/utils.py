#!/usr/bin/env python3

from io import BytesIO
import requests
import pandas as pd

def load_google_sheet(google_sheet_url):
    r = requests.get(google_sheet_url)
    data = r.content
    df = pd.read_csv(BytesIO(data), parse_dates=['Timestamp'])
    return df[35:65]

def load_dynamo_table(google_sheet_url):
    pass
