SELECT 
    f.response_id,
    c.country_name,
    f.ConvertedCompYearly AS salary,
    NTILE(100) OVER (
        PARTITION BY f.country_id 
        ORDER BY f.ConvertedCompYearly ASC
    ) AS salary_percentile
FROM 
    fact_responses f
JOIN 
    dim_country c ON f.country_id = c.country_id
WHERE 
    f.ConvertedCompYearly IS NOT NULL
ORDER BY 
    c.country_name, f.ConvertedCompYearly;
