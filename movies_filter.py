'''
Select wide realease from monthly extraction
'''

import pandas as pd

movies_json = 'movies.jl'
df = pd.read_json(movies_json, lines=True)

# Filter movies having max theather
has_max_th = ~(df['max_th'] == '-')
df = df[has_max_th]

# Filter movies wide
df['max_th'] = df['max_th'].str.replace(',', '').astype(int)
wide = df['max_th'] >= 600
df = df[wide]

# Remove duplication between years
df.sort_values(by='max_th', ascending=False, inplace=True)
df.drop_duplicates(subset=['release_id'], inplace=True)

# Save into file
json = df.to_json(lines=True, orient="records")
with open("movies_wide.jl", "w") as file:
    file.write(json)