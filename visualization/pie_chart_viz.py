#!/usr/bin/env python3
"""
Script to visualize my activities as a pie chart.

Usage: python pie_chart_viz.py [DYNAMODB_TABLE_NAME]
"""

import sys
import pandas as pd
import datetime
from collections import Counter
import matplotlib.pyplot as plt

from utils import load_dynamo_table, extract_blocks
from config import ACTIVITY_COLORS

def pie_chart_viz(blocks, activity_colors):
    frequencies = Counter(blocks)
    plt.pie(frequencies.values(),
            labels=frequencies.keys(),
            autopct='%1.1f%%',
            colors=[activity_colors[ac] for ac in frequencies.keys()])

if __name__ == "__main__":
    df = load_dynamo_table(sys.argv[1])
    blocks = extract_blocks(df)
    pie_chart_viz(blocks, ACTIVITY_COLORS)
