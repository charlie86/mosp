import os

def load_query(query_name):
    """
    Loads a SQL query from the 'sql' directory.
    
    Args:
        query_name (str): The name of the sql file without extension (e.g. 'bird_hunters')
        
    Returns:
        str: The raw SQL query.
    """
    
    # Path to SQL directory relative to this file
    sql_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sql')
    file_path = os.path.join(sql_dir, f"{query_name}.sql")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"SQL file not found: {file_path}")
        
    with open(file_path, 'r') as f:
        query = f.read()
        
    return query
