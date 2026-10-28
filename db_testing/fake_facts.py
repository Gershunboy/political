from models import *
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_, select, func

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine("sqlite:///" + os.path.join(basedir, "politician.db"))

with Session(engine) as session:
    count = session.execute(
        select(func.count(Politician.id))
        ).scalar_one()
    for i in range(1, 1+count):
        for j in range(3):
            j+=1
            newFact = Facts(fact=f"fun fact {j}", politician_id=i)
            session.add(newFact)
    session.commit()