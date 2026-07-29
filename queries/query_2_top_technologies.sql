WITH unnested_tech AS (
    SELECT 
        f.country_id,
        unnest(string_to_array(f.LanguageHaveWorkedWith, ';')) AS technology
    FROM 
        fact_responses f
    WHERE 
        f.LanguageHaveWorkedWith IS NOT NULL
),
tech_counts AS (
    SELECT 
        u.country_id,
        c.country_name,
        u.technology,
        COUNT(*) AS tech_count
    FROM 
        unnested_tech u
    JOIN 
        dim_country c ON u.country_id = c.country_id
    WHERE 
        c.country_name IN ('United States of America', 'India', 'Germany', 'United Kingdom of Great Britain and Northern Ireland')
    GROUP BY 
        u.country_id, c.country_name, u.technology
),
ranked_tech AS (
    SELECT 
        country_name,
        technology,
        tech_count,
        ROW_NUMBER() OVER (
            PARTITION BY country_id 
            ORDER BY tech_count DESC
        ) AS rank
    FROM 
        tech_counts
)
SELECT 
    country_name,
    technology,
    tech_count,
    rank
FROM 
    ranked_tech
WHERE 
    rank <= 5
ORDER BY 
    country_name, rank;
