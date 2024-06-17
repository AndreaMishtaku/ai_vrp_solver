from sqlalchemy import create_engine,text

def create_database_if_not_exists(connection_uri,db_name):
    engine = create_engine(connection_uri)
    conn = engine.connect()  
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {db_name}"))
    conn.close()