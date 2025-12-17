import pandas as pd
import os

os.makedirs("data", exist_ok=True)

df = pd.read_excel("Gen_AI Dataset.xlsx")

df = df.rename(columns={
    "Query": "Query",
    "Assessment_url": "Assessment_url"
})

df.to_csv("data/train.csv", index=False)

print("Train queries:", df["Query"].nunique())
print("Train rows:", len(df))
