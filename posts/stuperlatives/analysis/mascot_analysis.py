
import pandas as pd
from posts.stuperlatives.data.team_taxonomy import BIRD_TEAMS, CIRCUS_TEAMS, SOCIAL_JUSTICE_TEAMS, AQUATIC_TEAMS, PIRATE_TEAMS
from posts.stuperlatives.etl.bq_utils import DATASET_ID
from posts.stuperlatives.analysis.sql_loader import load_query

def run_query(client, query):
    return client.query(query).to_dataframe()

def analyze_bird_hunters(client):
    """
    Calculates passes defended (PDs) and INTs by defenders against Bird Teams.
    """
    print("Analyzing Bird Hunters (SQL)...")
    
    query = load_query('bird_hunters')
    return run_query(client, query)

def analyze_deadliest_catch(client):
    """
    Calculates INTs against Aquatic Teams.
    """
    print("Analyzing Deadliest Catch (SQL)...")
    
    query = load_query('deadliest_catch')
    return run_query(client, query)

def analyze_circus_tamers(client):
    """
    Calculates Rushing Yards Allowed by Defenses against Circus Teams.
    """
    print("Analyzing Circus Tamers (SQL)...")
    
    query = load_query('circus_tamers')
    return run_query(client, query)

def analyze_social_justice_warriors(client):
    """
    Calculates Win % and Point Differential against Social Justice Teams.
    Using 'schedules' table in BQ.
    """
    print("Analyzing Social Justice Warriors (SQL)...")
    
    query = load_query('social_justice_warriors')
    return run_query(client, query)

def analyze_pirates_booty(client):
    """
    Calculates Total Turnovers Committed (INTs + Fumble Lost) by players AGAINST Pirate Teams.
    """
    print("Analyzing Pirate's Booty (SQL)...")
    
    query = load_query('pirates_booty')
    return run_query(client, query)

def analyze_schoolyard_bullies(client):
    """
    Calculates Tackles made against players who attended Ivy League schools.
    Uses 'ivy_league_players' table to identify targets.
    """
    print("Analyzing Schoolyard Bullies (SQL)...")
    
    query = load_query('schoolyard_bullies')
    return run_query(client, query)



def analyze_nine_lives(client):
    """
    Calculates the most fumbles NOT LOST by Cat Team players.
    """
    print("Analyzing Nine Lives (SQL)...")
    
    query = load_query('nine_lives')
    return run_query(client, query)

if __name__ == "__main__":
    pass
