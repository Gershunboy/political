import os
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.orm import Session
from db_stuff.geocod import lookup_address

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine("sqlite:///" + os.path.join(basedir, "politicians.db"))

metadata = MetaData()
metadata.reflect(bind=engine)  # reads existing table structure from the db file

state_table = metadata.tables["state"]
county_table = metadata.tables["county"]
municipality_table = metadata.tables["municipality"]
congressional_district_table = metadata.tables["congressional_district"]
state_senate_district_table = metadata.tables["state_senate_district"]
state_house_district_table = metadata.tables["state_house_district"]

address = input()
address = lookup_address(address)
print (address)

with Session(engine) as session:
    state = session.execute(
        select(state_table.c.id).where(state_table.c.abbreviation == address["state"])
    ).scalar_one_or_none()
    print(state)

    county = address['county']
    cny = session.execute(
        select(county_table.c.id).where(county_table.c.name == county)
    ).scalar_one_or_none()
    print(cny)

    city = address['city']
    muni = session.execute(
        select(municipality_table.c.id).where(municipality_table.c.name == city)
    ).scalar_one_or_none()
    print(muni)

    cong = address['congressional_district']
    cg = session.execute(
        select(congressional_district_table.c.id).where(congressional_district_table.c.number == cong)
    ).scalar_one_or_none()
    print(cg)

    stSen = address['state_senate_district']
    st_sen = session.execute(
        select(state_senate_district_table.c.id).where(state_senate_district_table.c.number == stSen)
    ).scalar_one_or_none()
    print(st_sen)

    StHDt = address['state_house_district']
    st_hor = session.execute(
        select(state_house_district_table.c.id).where(state_house_district_table.c.number == StHDt)
    ).scalar_one_or_none()
    print(st_hor)