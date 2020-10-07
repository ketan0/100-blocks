#!/usr/bin/env python3
"""
Script to visualize Tim Urban's "100 Blocks"
(https://waitbutwhy.com/2016/10/100-blocks-day.html)
on a grid.

Usage: python hundred_blocks_viz.py [DYNAMODB_TABLE_NAME]
"""

import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from utils import load_dynamo_table, extract_blocks
from config import ACTIVITY_COLORS

def hundred_blocks_viz(blocks, activity_colors, day=None, ncols=10):
    fig, ax = plt.subplots()
    ax.axis("equal")
    for i, activity in enumerate(blocks):
        act_color = activity_colors[activity] if activity in activity_colors else 'black'
        circle = Circle((i % ncols, i // ncols), 0.4, color=act_color)
        ax.add_patch(circle)
    ax.autoscale_view()
    ax.set_ylim(ax.get_ylim()[::-1])
    legend_elements = [Line2D([0], [0], marker='o', color=color, label=activity, markersize=15)
                       for activity, color in activity_colors.items()]
    placeholder = 'A Day'
    plt.title(f'The Story of {day.strftime("%x") if day is not None else placeholder}, in {len(blocks)} blocks')
    ax.legend(handles=legend_elements,bbox_to_anchor=(1.25, 1.25))
    ax.axis('off')

if __name__ == "__main__":
    df = load_dynamo_table(sys.argv[1])
    blocks = extract_blocks(df)
    hundred_blocks_viz(blocks, ACTIVITY_COLORS)
