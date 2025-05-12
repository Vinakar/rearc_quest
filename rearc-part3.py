# Imports
import pandas as pd
import requests
import json

# Data sources
SERIES_DATA = "https://vinakar-rearcbucket.s3.amazonaws.com/pr.data.0.Current"
POPULATION_DATA = "https://vinakar-rearcbucket.s3.amazonaws.com/population.json"

# Load data
series = pd.read_csv('pr.data.0.Current', delimiter="\t")
# print(series)

pop_data = requests.get(POPULATION_DATA).json()

population = pd.json_normalize(pop_data, record_path="data")
# print(population)

# Filter data between [2013, 2018] inclusive
population_stats = population[(population["Year"].astype(int) >= 2013) &
                              (population["Year"].astype(int) <= 2018)]
# Display mean and standard deviation of population
print("Part-3 Result 1")
print(population_stats["Population"].mean()) 
print(population_stats["Population"].std())

# Remove columns names whitespace
series.rename(columns={"series_id        ": "series_id"}, inplace=True)
series.rename(columns={"       value": "value"}, inplace=True)
# Generate report
max_value_series = series.groupby(["series_id", "year"], as_index=False)["value"].agg("sum")
max_value_series = max_value_series.sort_values("value", ascending=False).drop_duplicates("series_id", keep="first").sort_index().reset_index(drop=True)
print("Part-3 Result 2")
print(max_value_series)

# Filter series data
specific_series = series.loc[series["series_id"].str.contains("PRS30006032", case=False)]
specific_series = specific_series[specific_series["period"].str.contains("Q01", case=False)]
# Filter population data
population_extract = population["Population"].astype(int)
population["Year"] = population["Year"].astype(int)
# Merge and filter results
result = pd.merge(specific_series, population, left_on="year", right_on="Year", how="left")
print("Part-3 Result 3")
print(result[["series_id", "year", "period", "value", "Population"]])