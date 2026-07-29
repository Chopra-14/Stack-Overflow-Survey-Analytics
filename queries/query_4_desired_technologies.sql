WITH python_devs AS (
    SELECT 
        response_id,
        LanguageWantToWorkWith
    FROM 
        fact_responses
    WHERE 
        LanguageHaveWorkedWith LIKE '%Python%'
        AND LanguageWantToWorkWith IS NOT NULL
),
unnested_desired AS (
    SELECT 
        unnest(string_to_array(LanguageWantToWorkWith, ';')) AS desired_technology
    FROM 
        python_devs
),
tech_counts AS (
    SELECT 
        desired_technology,
        COUNT(*) AS tech_count
    FROM 
        unnested_desired
    GROUP BY 
        desired_technology
),
ranked_desired_tech AS (
    SELECT 
        desired_technology,
        tech_count,
        RANK() OVER (ORDER BY tech_count DESC) AS rank
    FROM 
        tech_counts
)
SELECT 
    desired_technology,
    tech_count,
    rank
FROM 
    ranked_desired_tech
WHERE 
    rank <= 3
ORDER BY 
    rank;
