import json
import os

SCRIPT_PATH = 'posts/pff_analysis/run_analysis.py'
NOTEBOOK_PATH = 'posts/pff_analysis/nfl_ihop_analysis_updated.ipynb'

def create_notebook():
    if not os.path.exists(SCRIPT_PATH):
        print(f"Error: {SCRIPT_PATH} not found.")
        return

    with open(SCRIPT_PATH, 'r') as f:
        code_content = f.read()

    # Create notebook structure
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# PFF Run Blocking & IHOP Proximity Analysis\n",
                    "\n",
                    "This notebook performs the full analysis of PFF run blocking grades vs. IHOP proximity.\n",
                    "It fetches data from Google Sheets, filters for Offensive Linemen, merges with NFL schedule/stadium data,\n",
                    "calculates distances to the nearest IHOP, and saves the results to `pff_ihop_analysis_results.csv`."
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": code_content.splitlines(keepends=True)
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {
                    "name": "ipython",
                    "version": 3
                },
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.5"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }

    with open(NOTEBOOK_PATH, 'w') as f:
        json.dump(notebook, f, indent=4)
    
    print(f"Created notebook: {NOTEBOOK_PATH}")

if __name__ == "__main__":
    create_notebook()
