
import pandas as pd
from posts.stuperlatives.etl.bq_utils import DATASET_ID
from posts.stuperlatives.analysis.sql_loader import load_query

def run_query(client, query):
    return client.query(query).to_dataframe()

def analyze_grizzly_adams(client):
    """
    Tackles by bearded defenders.
    """
    print("Analyzing Grizzly Adams (SQL)...")
    
    query = load_query('grizzly_adams')
    return run_query(client, query)

def analyze_yosemite_sam(client):
    """
    EPA/Play for Mustached QBs.
    """
    print("Analyzing Yosemite Sam (SQL)...")
    
    MINSHEW_ID = '00-0035289'
    
    query = load_query('yosemite_sam')
    return run_query(client, query)

def analyze_rooster_fever(client):
    """
    Sacks AGAINST Redheaded QBs.
    """
    print("Analyzing Rooster Fever (SQL)...")
    
    DARNOLD_ID = '00-0034869'
    
    query = load_query('rooster_fever')
    return run_query(client, query)

def get_labels():
    # Deprecated for Analysis, but kept for ETL if needed?
    # Actually ETL uses it. But this file is analysis. 
    # Logic moved to BQ for analysis.
    pass
