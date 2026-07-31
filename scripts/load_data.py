import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
import os

DB_USER = os.getenv("POSTGRES_USER", "your_user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "your_password")
DB_NAME = os.getenv("POSTGRES_DB", "your_db")
DB_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
DB_PORT = os.getenv("POSTGRES_PORT", "5433")

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

def load_dimension(conn, df, col_name, table_name, id_col, val_col):
    """Extracts unique values, inserts into dim table, returns a mapping dict."""
    unique_vals = df[col_name].dropna().unique()
    
    with conn.cursor() as cur:
        # Insert ignoring conflicts
        insert_query = f"""
            INSERT INTO {table_name} ({val_col}) 
            VALUES %s ON CONFLICT ({val_col}) DO NOTHING
            RETURNING {id_col}, {val_col}
        """
        data_tuples = [(val,) for val in unique_vals]
        
        if data_tuples:
            execute_values(cur, f"INSERT INTO {table_name} ({val_col}) VALUES %s ON CONFLICT ({val_col}) DO NOTHING", data_tuples)
        
        conn.commit()
        
        # Fetch mapping
        cur.execute(f"SELECT {id_col}, {val_col} FROM {table_name}")
        mapping = {row[1]: row[0] for row in cur.fetchall()}
        
    return mapping

def main():
    csv_path = "data/survey_results_public.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Please place the dataset in the data/ directory.")
        return
    
    print("Loading CSV into pandas...")
    df = pd.read_csv(csv_path)
    
    # Basic cleaning
    df['ConvertedCompYearly'] = pd.to_numeric(df['ConvertedCompYearly'], errors='coerce')
    df['YearsCode'] = pd.to_numeric(df['YearsCode'].replace('Less than 1 year', 0).replace('More than 50 years', 51), errors='coerce')
    
    conn = get_db_connection()
    try:
        print("Loading Dimension Tables...")
        country_mapping = load_dimension(conn, df, 'Country', 'dim_country', 'country_id', 'country_name')
        employment_mapping = load_dimension(conn, df, 'Employment', 'dim_employment', 'employment_id', 'employment_name')
        devtype_mapping = load_dimension(conn, df, 'DevType', 'dim_developer_type', 'dev_type_id', 'dev_type_name')
        
        print("Mapping Facts...")
        df['country_id'] = df['Country'].map(country_mapping)
        df['employment_id'] = df['Employment'].map(employment_mapping)
        df['dev_type_id'] = df['DevType'].map(devtype_mapping)
        
        # Prepare fact table data
        fact_cols = ['country_id', 'employment_id', 'dev_type_id', 'ConvertedCompYearly', 'YearsCode', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith']
        
        # Ensure columns exist even if some are missing from CSV
        for col in fact_cols:
            if col not in df.columns:
                df[col] = None
                
        df_facts = df[fact_cols]
        # Replace NaN with None for psycopg2
        df_facts = df_facts.where(pd.notnull(df_facts), None)
        fact_data = [tuple(x) for x in df_facts.to_numpy()]
        
        print("Loading Fact Table...")
        with conn.cursor() as cur:
            insert_query = """
                INSERT INTO fact_responses 
                (country_id, employment_id, dev_type_id, ConvertedCompYearly, YearsCode, LanguageHaveWorkedWith, LanguageWantToWorkWith)
                VALUES %s
            """
            execute_values(cur, insert_query, fact_data)
            conn.commit()
            
        print("ETL process completed successfully.")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
