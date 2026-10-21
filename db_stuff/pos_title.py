import pandas as pd
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_, select
import numpy as np
from models import *

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine("sqlite:///" + os.path.join(basedir, "politician.db"))

path = pd.ExcelFile('/Users/alexgershuni/Documents/python/political/db_stuff/PUBLIC UNOFFICIAL 2026 GENERAL CANDIDATE LIST.xlsx')
df = pd.read_excel(path, sheet_name=3, skiprows=[0, 1])
df = df.dropna(subset=[df.columns[3]])
df.columns = df.columns.str.replace("_", " ").str.title()
df.columns = df.columns.str.strip()
df = df.map(lambda x: x.title() if isinstance(x, str) else x)
print('\n\n\n\n\n\n\n\n\n\n')
#df["Office"] = df["Office"].str.split(" ", n=1).str[1]



unique = []
with Session(engine) as session:
    exist = session.scalars(select(Position)).all()
    for i in exist:
        stmt = select(Municipality.name).where(Municipality.id == i.municipality_id)
        mun = session.execute(stmt).one_or_none()
        pos = {"mun": mun, "nam": i.name}
        unique.append(pos)
    for index, row in df.iterrows():
        if not row.iloc[3]:
            continue
        nam = row.iloc[1]
        mun = row.iloc[0]
        pos = {"mun": mun, "nam": nam}
        if pos not in unique:
            unique.append(pos)
            if row.iloc[3] == "ONE":
                votfor = 1
            else:
                votfor = 2
            stmt = select(Municipality.id).where(Municipality.name == mun)
            munid = session.execute(stmt).scalar_one()

            existing = session.execute(
                select(Position).where(Position.name == nam, Position.municipality_id == munid)
            ).scalar_one_or_none()

            print(f"Row {index}: mun={mun}, nam={nam}, munid={munid}, existing={existing}")

            if existing is None:
                new_pos = Position(name=nam, scope='local', state_id=30, votefor=votfor, county_id=2, municipality_id=munid)
                session.add(new_pos)
            else:
                print(index)
    session.commit()





#sheet 1
"""
unique = [x for x in df['Congressional District'].unique() if isinstance(x, (float, np.floating))]
list = {}
with Session(engine) as session:
    for i in unique:
        stmt = select(Position.id).where(
            and_(
                Position.state_id == 30,
                Position.congressional_district_id == i
            )
        )
        list[i] = session.execute(stmt).scalar()
    for index,row in df.iterrows():
        par = row.iloc[0].title()
        ful_name = row.iloc[5].title()
        cd = int(row.iloc[1])
        cd = list[cd]
        new_pol = Politician(name=ful_name, position_id = cd, party = par)
        session.add(new_pol)
    session.commit()
"""





#sheet 0
"""
with Session(engine) as session:
    for index, row in df.iterrows():
        par = row.iloc[0].title()
        ful_name = row.iloc[4].title()
        new_politician = Politician(name=ful_name, position_id=1, party=par)
        session.add(new_politician)
    session.commit()
"""

