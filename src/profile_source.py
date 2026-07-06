"""
Profiles a representative sample of the Chicago Traffic API.

This script is intended for exploratory data profiling and schema validation.
The `# %%` markers allow the file to be run in sections using the VS Code
Interactive Window, but the script can also be executed normally from the
command line.
"""

# %%
# Setup window
import pandas as pd

df = pd.read_json("C:/Users/dawn/chicago-traffic-etl/data/raw/chicago_traffic_raw_sample.json")

print(df.head())

print(df.dtypes)

df.info()

# %%
# Profiling Segment ID

print(df["segmentid"].min())
print(df["segmentid"].max())
print(df["segmentid"].isnull().sum())

# %%
sorted(df["_strheading"].unique())


# %%
df["_strheading"].value_counts()

# %%

sorted(df["_comments"].dropna().unique())

df["_comments"].value_counts(dropna=False)

# %%
df.groupby("segmentid")["_comments"].nunique(dropna=False).sort_values(ascending=False).head(20)

# %%
df["_direction"].value_counts()

# %%
