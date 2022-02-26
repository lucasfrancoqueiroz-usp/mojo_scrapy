import pandas as pd
df = pd.read_json('movies.jl', lines=True)

# Filter movies having max theather
has_max_th = ~(df['max_th'] == '-')
df = df[has_max_th]

# Filter movies wide
df['max_th'] = df['max_th'].str.replace(',', '').astype(int)
wide = df['max_th'] >= 600
df = df[wide]

# Remove duplication between years
df.sort_values(by='max_th', ascending=False, inplace=True)
df.drop_duplicates(subset=['release', 'year'], inplace=True)