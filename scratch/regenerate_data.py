import pandas as pd
import numpy as np
import os

base_dir = r"c:\Users\ajcbu\Documents\College\Third Year\2nd Sem\BA Sir Pao\Final Project May 31"

poverty_path = os.path.join(base_dir, "share-of-population-in-extreme-poverty (1)", "share-of-population-in-extreme-poverty.csv")
social_path = os.path.join(base_dir, "share-covered-by-one-social-protection-benefit", "share-covered-by-one-social-protection-benefit.csv")
basic_path = os.path.join(base_dir, "access-to-basic-services", "access-to-basic-services.csv")

# Load datasets
df_p = pd.read_csv(poverty_path)
df_s = pd.read_csv(social_path)
df_b = pd.read_csv(basic_path)

# Standardize columns
df_p = df_p.rename(columns={"Share of population in poverty ($3 a day)": "Poverty_Rate"})
df_s = df_s.rename(columns={"1.3.1 - [ILO] Proportion of population covered by at least one social protection benefit, by sex (%) - SI_COV_BENFTS - Both sexes": "Social_Protection_Coverage"})

df_b = df_b.rename(columns={
    "Electricity": "Electricity_Access",
    "Clean cooking fuels and technologies": "Clean_Cooking_Access",
    "Improved water source": "Water_Access",
    "Improved sanitation facilities": "Sanitation_Access"
})

# Get region mapping for each country (Entity -> Region)
region_map = df_p[['Entity', 'World region according to OWID']].dropna().drop_duplicates()
entity_to_region = dict(zip(region_map['Entity'], region_map['World region according to OWID']))

# Filter years 2010 to 2026 (today)
years_range = list(range(2010, 2027))

# Get all unique countries (Entity, Code) present in the poverty dataset (only actual countries with 3-letter codes)
countries = df_p[['Entity', 'Code']].drop_duplicates().dropna()
countries = countries[countries['Code'].str.len() == 3]

# Create a skeleton dataframe of all country-year combinations from 2010 to 2026
skeleton = []
for _, row in countries.iterrows():
    for year in years_range:
        skeleton.append({
            "Entity": row["Entity"],
            "Code": row["Code"],
            "Year": year,
            "Region": entity_to_region.get(row["Entity"], "Unknown")
        })
df_skeleton = pd.DataFrame(skeleton)

# Merge datasets
df_merged = df_skeleton.merge(df_p[['Entity', 'Code', 'Year', 'Poverty_Rate']], on=['Entity', 'Code', 'Year'], how='left')
df_merged = df_merged.merge(df_s[['Entity', 'Code', 'Year', 'Social_Protection_Coverage']], on=['Entity', 'Code', 'Year'], how='left')
df_merged = df_merged.merge(df_b[['Entity', 'Code', 'Year', 'Electricity_Access', 'Clean_Cooking_Access', 'Water_Access', 'Sanitation_Access']], on=['Entity', 'Code', 'Year'], how='left')

# Imputation columns list
cols_to_impute = [
    "Poverty_Rate", 
    "Social_Protection_Coverage", 
    "Electricity_Access", 
    "Clean_Cooking_Access", 
    "Water_Access", 
    "Sanitation_Access"
]

# Step 1: Country-level linear interpolation & boundary fill
def impute_country(group, entity_name):
    group = group.sort_values("Year")
    for col in cols_to_impute:
        if group[col].notna().any():
            group[col] = group[col].interpolate(method="linear").ffill().bfill()
    group["Entity"] = entity_name
    return group

# Explicitly loop and impute
imputed_groups = []
for name, group in df_merged.groupby("Entity"):
    imputed_groups.append(impute_country(group, name))

df_imputed = pd.concat(imputed_groups, ignore_index=True)

# Step 2: Calculate regional and global averages per year for hierarchical imputation
regional_avg = df_imputed.groupby(["Region", "Year"])[cols_to_impute].transform("mean")
global_avg = df_imputed.groupby("Year")[cols_to_impute].transform("mean")

# Step 3: Impute remaining NaNs using regional average, then global average
for col in cols_to_impute:
    df_imputed[col] = df_imputed[col].fillna(regional_avg[col])
    df_imputed[col] = df_imputed[col].fillna(global_avg[col])

# Reorder and format columns
df_final = df_imputed.rename(columns={"Poverty_Rate": "Poverty_Rate_Imputed"})
df_final = df_final[[
    "Entity", "Code", "Year", 
    "Poverty_Rate_Imputed", "Social_Protection_Coverage", 
    "Electricity_Access", "Clean_Cooking_Access", 
    "Water_Access", "Sanitation_Access"
]]

# Save the final imputed dataset to the workspace path (overwriting the old file)
output_path = os.path.join(base_dir, "dashboard_final_data.csv")
df_final.to_csv(output_path, index=False)

print(f"Successfully saved {len(df_final)} rows to {output_path}")
print("Years covered:", df_final["Year"].min(), "to", df_final["Year"].max())
print("Unique countries:", df_final["Entity"].nunique())
print("Missing values after final check:")
print(df_final.isna().sum())
