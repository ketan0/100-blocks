#!/usr/bin/env python3
"""
Script to visualize my activities as a pie chart

Usage: python pie_chart_viz.py [DYNAMODB_TABLE_NAME]
"""

import sys
import pandas as pd
import datetime
from collections import Counter
import matplotlib.pyplot as plt

from utils import load_dynamo_table, extract_blocks

def pie_chart_viz(blocks, activity_ids):
    ids_to_activities = {v: k for k, v in activity_ids.items()}
    frequencies = Counter(blocks)
    plt.pie(frequencies.values(), labels=[ids_to_activities[id] for id in frequencies.keys()])

if __name__ == "__main__":
    df = load_dynamo_table(sys.argv[1])
    blocks, activity_ids = extract_blocks(df)
    pie_chart_viz(blocks, activity_ids)
