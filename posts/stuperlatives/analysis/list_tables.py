
from posts.stuperlatives.etl.bq_utils import get_bq_client

def list_tables():
    client = get_bq_client()
    dataset_id = 'pff_analysis'
    tables = client.list_tables(dataset_id) 
    print(f"Tables in {dataset_id}:")
    for table in tables:
        print(table.table_id)

if __name__ == "__main__":
    list_tables()
