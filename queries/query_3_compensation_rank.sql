SELECT 
    f.response_id,
    f.YearsCode AS years_of_experience,
    f.ConvertedCompYearly AS salary,
    RANK() OVER (
        PARTITION BY f.YearsCode 
        ORDER BY f.ConvertedCompYearly DESC
    ) AS compensation_rank
FROM 
    fact_responses f
WHERE 
    f.YearsCode IS NOT NULL 
    AND f.ConvertedCompYearly IS NOT NULL
ORDER BY 
    f.YearsCode, compensation_rank
