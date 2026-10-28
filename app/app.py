import os
from models import *
from flask import Flask, render_template, request
from sqlalchemy import select, or_, and_
from geocod import *
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "politician.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/next")
def next():
    ad = request.args.get("address")
    zip = request.args.get("zip")
    city = request.args.get("city")
    st = request.args.get("st")
    address = f"{ad}, {city}, {st} {zip}"
    address = lookup_address(address)

    state = db.session.execute(
        select(State.id).where(State.abbreviation == address["state"])
    ).scalar_one_or_none()

    county = address['county']
    cny = db.session.execute(
        select(County.id).where(County.name == county)
    ).scalar_one_or_none()

    city = address['city']
    muni = db.session.execute(
        select(Municipality.id).where(Municipality.name == city)
        ).scalar_one_or_none()

    cong = address['congressional_district']
    cg = db.session.execute(
            select(CongressionalDistrict.id).where(CongressionalDistrict.number == cong)
        ).scalar_one_or_none()

    stSen = address['state_senate_district']
    st_sen = db.session.execute(
        select(StateSenateDistrict.id).where(StateSenateDistrict.number == stSen)
        ).scalar_one_or_none()

    StHDt = address['state_house_district']
    st_hor = db.session.execute(
        select(StateHouseDistrict.id).where(StateHouseDistrict.number == StHDt)
    ).scalar_one_or_none()


    stmt = select(Position.id).where(
        and_(
            or_(Position.state_id == state, Position.state_id.is_(None)),
            or_(Position.county_id == cny, Position.county_id.is_(None)),
            or_(Position.municipality_id == muni, Position.municipality_id.is_(None)),
            or_(Position.congressional_district_id == cg, Position.congressional_district_id.is_(None)),
            or_(Position.state_senate_district_id == stSen, Position.state_senate_district_id.is_(None)),
            or_(Position.state_house_district_id == st_hor, Position.state_house_district_id.is_(None))
        )
    )
    pos_id = db.session.execute(stmt).scalars().all()
    title = []
    politician = []
    facts = []
    for i in pos_id:
        title_stmt = select(Position.name).where(Position.id == i)
        people_stmt = select(Politician.name).where(Politician.position_id == i)
        people = db.session.execute(people_stmt).scalars().all()
        if people:
            title.append(db.session.execute(title_stmt).scalar_one_or_none())  
            politician.append(people)
            person_fact = []
            for p in people:
                facts_stmt = select(Facts.fact).where(Facts.politician_id == select(Politician.id).where(Politician.name == p).scalar_subquery())
                fact = db.session.execute(facts_stmt).scalars().all()
                person_fact.append(fact)
            facts.append(person_fact)
    return render_template("next.html", title=title, politician=politician, facts=facts)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)