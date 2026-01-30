
from posts.stuperlatives.etl.bq_utils import get_bq_client

def check_weather():
    client = get_bq_client()
    if not client: return

    table_id = "stuperlatives.pbp_data"
    
    try:
        table = client.get_table(table_id)
        print(f"--- Schema for {table_id} ---")
        weather_cols = [schema.name for schema in table.schema if any(x in schema.name.lower() for x in ['weather', 'temp', 'wind', 'roof', 'stadium', 'surface'])]
        
        if not weather_cols:
            print("No obvious weather columns found.")
        else:
            print(f"Found potential weather columns: {weather_cols}")
            
            # Get a sample
            cols_str = ", ".join(weather_cols)
            query = f"SELECT {cols_str} FROM `{table_id}` WHERE weather IS NOT NULL LIMIT 5"
            df = client.query(query).to_dataframe()
            print("\n--- Sample Data ---")
            print(df.to_string())

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_weather()
