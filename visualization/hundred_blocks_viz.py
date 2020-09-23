#!/usr/bin/env python3
"""
Script to visualize Tim Urban's "100 Blocks" (https://waitbutwhy.com/2016/10/100-blocks-day.html)

Usage: python hundred_blocks_viz.py [GOOGLE_SPREADSHEET URL]
"""

import sys
import pandas as pd
import datetime
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np

from utils import load_google_sheet

def next_nearest_activity(timestamp, df):
    return df[df['Timestamp'] > timestamp]['Category'].values[0]

def hundred_blocks_viz(df, ncols=10):
    start = df['Timestamp'].iloc[0]
    end = df['Timestamp'].iloc[-1]
    print('start: ', start)
    print('end: ', end)
    category_ids = {category: i for i, category in enumerate(df['Category'].unique())}
    block_start_times = pd.date_range(start=start, end=end, freq='10min')
    block_activities = [category_ids[next_nearest_activity(ts, df)]
                        for ts in block_start_times]
    block_activities = np.pad(
        block_activities, (0, ncols - (len(block_activities) % ncols)), 'constant', constant_values=-1
    )
    block_activities_mat = block_activities.reshape(-1, ncols)
    cmap = ListedColormap([f'C{i}' for i in category_ids.values()])
    plt.matshow(block_activities_mat, cmap=cmap)
    legend_elements = [Line2D([0], [0], marker='o', color=f'C{i}', label=category, markersize=15)
                       for category, i in category_ids.items()]
    plt.legend(handles=legend_elements)
    plt.axis('off')

if __name__ == "__main__":
    df = load_google_sheet(sys.argv[1])
    hundred_blocks_viz(df)
