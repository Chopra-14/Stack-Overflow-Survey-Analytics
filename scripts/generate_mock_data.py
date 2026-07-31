import pandas as pd
import random

# Generate 1000 rows of mock data for the demo
def generate_mock_dataset(filename="data/survey_results_public.csv"):
    countries = ['United States of America', 'India', 'Germany', 'United Kingdom of Great Britain and Northern Ireland', 'Canada', 'France', 'Brazil']
    employments = ['Employed, full-time', 'Independent contractor, freelancer, or self-employed', 'Student, full-time', 'Not employed, but looking for work']
    dev_types = ['Developer, full-stack', 'Developer, back-end', 'Developer, front-end', 'Data scientist or machine learning specialist', 'DevOps specialist']
    languages = ['Python', 'JavaScript', 'HTML/CSS', 'SQL', 'Java', 'C#', 'C++', 'TypeScript', 'Go', 'Rust']
    
    data = []
    for i in range(1, 1001):
        country = random.choice(countries)
        employment = random.choice(employments)
        dev_type = random.choice(dev_types)
        
        # Salary and Experience based somewhat on location/role just to have numbers
        if country == 'India':
            salary = random.randint(10000, 50000)
        elif country == 'United States of America':
            salary = random.randint(60000, 250000)
        else:
            salary = random.randint(40000, 120000)
            
        years_code = random.randint(0, 40)
        if years_code == 0:
            years_code = 'Less than 1 year'
            
        have_worked_with = ";".join(random.sample(languages, random.randint(1, 5)))
        want_to_work_with = ";".join(random.sample(languages, random.randint(1, 4)))
        
        # Randomly inject some NAs
        if random.random() < 0.1:
            salary = 'NA'
        
        data.append({
            'ResponseId': i,
            'Country': country,
            'Employment': employment,
            'DevType': dev_type,
            'ConvertedCompYearly': salary,
            'YearsCode': years_code,
            'LanguageHaveWorkedWith': have_worked_with,
            'LanguageWantToWorkWith': want_to_work_with
        })

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Mock dataset generated at {filename}!")

if __name__ == "__main__":
    generate_mock_dataset()
