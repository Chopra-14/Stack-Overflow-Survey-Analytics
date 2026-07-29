-- schema/schema.sql

-- Dimension Tables
CREATE TABLE IF NOT EXISTS dim_country (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_employment (
    employment_id SERIAL PRIMARY KEY,
    employment_name VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS dim_developer_type (
    dev_type_id SERIAL PRIMARY KEY,
    dev_type_name VARCHAR(255) UNIQUE
);

-- Fact Table
CREATE TABLE IF NOT EXISTS fact_responses (
    response_id SERIAL PRIMARY KEY,
    country_id INTEGER REFERENCES dim_country(country_id),
    employment_id INTEGER REFERENCES dim_employment(employment_id),
    dev_type_id INTEGER REFERENCES dim_developer_type(dev_type_id),
    ConvertedCompYearly NUMERIC,
    YearsCode NUMERIC,
    LanguageHaveWorkedWith TEXT,
    LanguageWantToWorkWith TEXT
);
