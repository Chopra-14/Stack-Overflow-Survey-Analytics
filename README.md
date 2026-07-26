# Stack Overflow Survey Analytics Data Warehouse

## Overview
This project builds a PostgreSQL data warehouse and an ETL pipeline using the Stack Overflow Developer Survey dataset. It uses a star schema design optimized for analytical queries with window functions.

## Setup Instructions

1. **Download Dataset**: Download the Stack Overflow Developer Survey (2023 CSV) dataset and place it in the `data/` directory. Name the file `survey_results_public.csv`. The `data/` directory is git-ignored.
2. **Start Database**: Use Docker Compose to spin up the PostgreSQL instance.
   ```bash
   docker-compose up -d
   ```
3. **Initialize Schema**: Run the schema creation script on the running DB (or apply it through your SQL client):
   ```bash
   docker exec -i <container_id_or_name> psql -U your_user -d your_db < schema/schema.sql
   ```
4. **Install Python Dependencies**: It is recommended to use a virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install pandas psycopg2-binary
   ```
5. **Run ETL Pipeline**: Extract, transform and load the data.
   ```bash
   python scripts/load_data.py
   ```
6. **Apply Indexes**: After loading data, apply the indexes for optimized querying.
   ```bash
   docker exec -i <container_id_or_name> psql -U your_user -d your_db < schema/indexes.sql
   ```
7. **Run Queries**: Execute the analytical queries located in the `queries/` directory and save their output to the `output/` directory as CSV files. Additionally, run `EXPLAIN ANALYZE` on each and save execution plans to `explain_analyze/`.
