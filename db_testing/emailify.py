import pandas as pd
import os
from sqlalchemy.orm import *
from sqlalchemy import *
from models import *

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine("sqlite:///" + os.path.join(basedir, "politician.db"))

path = pd.ExcelFile('/Users/alexgershuni/Documents/python/political/db_stuff/emails.xlsx')
df = pd.read_excel(path, sheet_name=2, skiprows=[0, 1])
df = df.dropna(subset=[df.columns[3]])
df.columns = df.columns.str.replace("_", " ").str.title()
df.columns = df.columns.str.strip()
df = df.map(lambda x: x.title() if isinstance(x, str) else x)
print('\n\n\n\n\n\n\n\n\n\n')
#df["Office"] = df["Office"].str.split(" ", n=1).str[1]
with Session(engine) as session:
    for index,row in df.iterrows():
        pol = session.execute(
            select(Politician).where(Politician.name == row.iloc[10])
        ).scalar_one_or_none()
        if pol is None:
            print(f"No match for: {row.iloc[10]}")
            continue
        print(row.iloc[10])
        pol.email=row.iloc[6]
        print(pol.email)
    session.commit()