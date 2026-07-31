SELECT 
    f.response_id,
    c.country_name,
    dt.dev_type_name,
    f.ConvertedCompYearly AS individual_salary,
    AVG(f.ConvertedCompYearly) OVER (
        PARTITION BY f.country_id, f.dev_type_id
    ) AS avg_peer_salary
FROM 
    fact_responses f
JOIN 
    dim_country c ON f.country_id = c.country_id
JOIN 
    dim_developer_type dt ON f.dev_type_id = dt.dev_type_id
WHERE 
    f.ConvertedCompYearly IS NOT NULL
ORDER BY 
    c.country_name, dt.dev_type_name, f.ConvertedCompYearly DESC
