from flask import * 
from db_stuff.geocod import *
import sqlite3

DB_PATH = "politicians.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = OFF")  # off during migration
cur = conn.cursor()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")
@app.route("/next")
def next():
    ad=request.args.get("address")
    zip=request.args.get("zip")
    city=request.args.get("city")
    st=request.args.get("st")
    address=f"{ad}, {city}, {st} {zip}"
    address = lookup_address(address)
    politician = {}
        for i in address:
            politician[i] = cur.execute("""
            SELECT name FROM politician WHERE position_id = (
                    SELECT )
            """) 
    return render_template("next.html",address=address)


if __name__ == "__main__":
    app.run(debug=True)