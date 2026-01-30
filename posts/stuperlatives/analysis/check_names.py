
from posts.stuperlatives.etl.bq_utils import get_bq_client

def check_names():
    client = get_bq_client()
    query = """
    SELECT DISTINCT passer_player_name 
    FROM `stuperlatives.pbp_data` 
    WHERE passer_player_name LIKE '%Dalton%' 
       OR passer_player_name LIKE '%Wentz%'
       OR passer_player_name LIKE '%Darnold%'
    LIMIT 20
    """
    df = client.query(query).to_dataframe()
    print(df.to_string())

if __name__ == "__main__":
    check_names()
