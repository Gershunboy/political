CREATE TABLE state (
    "id"           INTEGER PRIMARY KEY,
    "name"         TEXT UNIQUE NOT NULL,
    "abbreviation" TEXT UNIQUE NOT NULL
);

CREATE TABLE county (
    "id"         INTEGER PRIMARY KEY,
    "state_id"   INTEGER NOT NULL,
    "name"       TEXT NOT NULL,
    FOREIGN KEY ("state_id") REFERENCES state("id")
);

CREATE TABLE municipality (
    "id"         INTEGER PRIMARY KEY,
    "county_id"  INTEGER NOT NULL,
    "name"       TEXT NOT NULL,
    FOREIGN KEY ("county_id") REFERENCES county("id")
);

-- U.S. House districts (one per state, numbered, or at-large)
CREATE TABLE congressional_district (
    "id"            INTEGER PRIMARY KEY,
    "state_id"      INTEGER NOT NULL,
    "number"        INTEGER NOT NULL,        -- 0 for at-large
    "at_large"      INTEGER NOT NULL DEFAULT 0,
    "ocd_id"        TEXT,
    FOREIGN KEY ("state_id") REFERENCES state("id")
);

-- State senate (upper chamber) districts
CREATE TABLE state_senate_district (
    "id"          INTEGER PRIMARY KEY,
    "state_id"    INTEGER NOT NULL,
    "number"      TEXT NOT NULL,             -- TEXT since some states use letters
    "ocd_id"      TEXT,
    FOREIGN KEY ("state_id") REFERENCES state("id")
);

-- State house / assembly (lower chamber) districts
CREATE TABLE state_house_district (
    "id"          INTEGER PRIMARY KEY,
    "state_id"    INTEGER NOT NULL,
    "number"      TEXT NOT NULL,
    "ocd_id"      TEXT,
    FOREIGN KEY ("state_id") REFERENCES state("id")
);

-- School board districts (from Geocodio's "school" field)
CREATE TABLE school_district (
    "id"          INTEGER PRIMARY KEY,
    "state_id"    INTEGER NOT NULL,
    "name"        TEXT NOT NULL,
    "type"        TEXT NOT NULL,             -- "elementary", "secondary", "unified"
    FOREIGN KEY ("state_id") REFERENCES state("id")
);

-- Every seat/office a politician can hold.
-- Exactly one of the *_id columns should be set, matching "scope".
CREATE TABLE position (
    "id"                       INTEGER PRIMARY KEY,
    "name"                     TEXT NOT NULL,    -- e.g. "U.S. Senator", "Mayor"
    "scope"                    TEXT NOT NULL,    -- "federal", "state_senate", "state_house",
                                                   -- "congressional", "statewide", "countywide",
                                                   -- "municipal", "school"
    "state_id"                 INTEGER,
    "county_id"                INTEGER,
    "municipality_id"          INTEGER,
    "congressional_district_id" INTEGER,
    "state_senate_district_id"  INTEGER,
    "state_house_district_id"   INTEGER,
    "school_district_id"        INTEGER,
    "term_years"               INTEGER,
    "partisan"                 INTEGER NOT NULL DEFAULT 1,  -- 0 = nonpartisan
    FOREIGN KEY ("state_id")                  REFERENCES state("id"),
    FOREIGN KEY ("county_id")                 REFERENCES county("id"),
    FOREIGN KEY ("municipality_id")           REFERENCES municipality("id"),
    FOREIGN KEY ("congressional_district_id") REFERENCES congressional_district("id"),
    FOREIGN KEY ("state_senate_district_id")  REFERENCES state_senate_district("id"),
    FOREIGN KEY ("state_house_district_id")   REFERENCES state_house_district("id"),
    FOREIGN KEY ("school_district_id")        REFERENCES school_district("id")
);

CREATE TABLE politician (
    "id"          INTEGER PRIMARY KEY,
    "name"        TEXT NOT NULL,
    "position_id" INTEGER,
    "party"       TEXT,
    FOREIGN KEY ("position_id") REFERENCES position("id")
);

CREATE TABLE facts (
    "id"            INTEGER PRIMARY KEY,
    "fact"          TEXT,
    "politician_id" INTEGER,
    FOREIGN KEY ("politician_id") REFERENCES politician("id")
);