import pandas as pd
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_, select
import numpy as np
from models import *

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine("sqlite:///" + os.path.join(basedir, "politician.db"))

path = pd.ExcelFile('/Users/alexgershuni/Documents/python/political/db_stuff/emails.xlsx')
df = pd.read_excel(path, sheet_name=4, skiprows=[0, 1])
df = df.dropna(subset=[df.columns[7]])
df = df.dropna()
df.columns = df.columns.str.replace("_", " ").str.title()
df.columns = df.columns.str.strip()
df = df.map(lambda x: x.title() if isinstance(x, str) else x)
print(df.columns.tolist())


with Session(engine) as session:
    existing = session.scalars(select(Politician.name)).all()
    for index,row in df.iterrows():
        stmt = select(Municipality.id).where(Municipality.name == row.iloc[0])
        mun = session.execute(stmt).scalars
        stmt = select(Position.id).where(
            and_(
                Position.name==row.iloc[1],
                Position.state_id==30,
                Position.county_id==2,
                Position.municipality_id==mun
                )
        )
        pos = session.execute(stmt).scalar()
        print(pos)
        print(row.iloc[10])
        nam = f"{row.iloc[5]} {row.iloc[6]}"
        if nam not in existing:
            par = "Democratic"
            new_pol=Politician(name=nam, position_id=pos, party=par, email=row.iloc[8])
            session.add(new_pol)
    session.commit()