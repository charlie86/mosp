
from posts.stuperlatives.etl.bq_utils import get_bq_client

def check_team_cols():
    client = get_bq_client()
    table = client.get_table("stuperlatives.pbp_data")
    team_cols = [s.name for s in table.schema if 'team' in s.name.lower()]
    print(f"Team Columns: {team_cols}")

if __name__ == "__main__":
    check_team_cols()
