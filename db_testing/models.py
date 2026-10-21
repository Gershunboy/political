from extensions import db

class State(db.Model):
    __tablename__ = "state"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    abbreviation = db.Column(db.String, unique=True, nullable=False)


class County(db.Model):
    __tablename__ = "county"
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), nullable=False)
    name = db.Column(db.String, nullable=False)


class Municipality(db.Model):
    __tablename__ = "municipality"
    id = db.Column(db.Integer, primary_key=True)
    county_id = db.Column(db.Integer, db.ForeignKey("county.id"), nullable=False)
    name = db.Column(db.String, nullable=False)


class Position(db.Model):
    __tablename__ = "position"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scope = db.Column(db.String, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"))
    county_id = db.Column(db.Integer, db.ForeignKey("county.id"))
    municipality_id = db.Column(db.Integer, db.ForeignKey("municipality.id"))
    congressional_district_id = db.Column(db.Integer, db.ForeignKey("congressional_district.id"))
    state_senate_district_id = db.Column(db.Integer, db.ForeignKey("state_senate_district.id"))
    state_house_district_id = db.Column(db.Integer, db.ForeignKey("state_house_district.id"))
    term_years = db.Column(db.Integer)
    partisan = db.Column(db.Integer, default=1)
    votefor = db.Column(db.Integer, default=1)


class Politician(db.Model):
    __tablename__ = "politician"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey("position.id"))
    party = db.Column(db.String)
    email = db.Column(db.String)


class Facts(db.Model):
    __tablename__ = "facts"
    id = db.Column(db.Integer, primary_key=True)
    fact = db.Column(db.String)
    politician_id = db.Column(db.Integer, db.ForeignKey("politician.id"))


class CongressionalDistrict(db.Model):
    __tablename__ = "congressional_district"
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    at_large = db.Column(db.Integer, nullable=False, default=0)
    ocd_id = db.Column(db.String)


class StateSenateDistrict(db.Model):
    __tablename__ = "state_senate_district"
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), nullable=False)
    number = db.Column(db.String, nullable=False)
    ocd_id = db.Column(db.String)


class StateHouseDistrict(db.Model):
    __tablename__ = "state_house_district"
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), nullable=False)
    number = db.Column(db.String, nullable=False)
    ocd_id = db.Column(db.String)


class SchoolDistrict(db.Model):
    __tablename__ = "school_district"
    id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey("state.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
