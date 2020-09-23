#!/usr/bin/env python3
"""
Script to visualize Tim Urban's "100 Blocks" (https://waitbutwhy.com/2016/10/100-blocks-day.html)

Usage: python hundred_blocks_viz.py [GOOGLE_SPREADSHEET URL]
"""

import sys
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.colors import BoundaryNorm
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

from utils import load_google_sheet, load_dynamo_table, extract_blocks

def hundred_blocks_viz(blocks, activity_ids, ncols=10):
    fig, ax = plt.subplots()
    ax.axis("equal")
    for i, activity_id in enumerate(blocks):
        circle = Circle((2 * (i % ncols), 2 * (i // ncols)), 0.4, color=f'C{activity_id}')
        ax.add_patch(circle)
    ax.autoscale_view()
    ax.set_ylim(ax.get_ylim()[::-1])
    legend_elements = [Line2D([0], [0], marker='o', color=f'C{i}', label=activity, markersize=15)
                       for activity, i in activity_ids.items()]
    plt.title(f'The Story of Today, in {len(blocks)} blocks')
    ax.legend(handles=legend_elements,bbox_to_anchor=(1.25, 1.25))
    ax.axis('off')

if __name__ == "__main__":
    df = load_dynamo_table(sys.argv[1])
    blocks, activity_ids = extract_blocks(df)
    hundred_blocks_viz(blocks, activity_ids)
