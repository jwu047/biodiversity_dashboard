import os
import numpy as np
import pandas as pd

# https://docs.sqlalchemy.org/en/13/orm/extensions/automap.html
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# https://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


""" Setup the Database """
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/bellybutton.sqlite"
db = SQLAlchemy(app)

Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# mapped classes are now created with names by default, matching that of the table name
Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples


""" Create routes """
@app.route("/")
def index():
    # Homepage
    return render_template("index.html")


@app.route("/names")
def names():
    # List of sample names
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # return list of only the sample names
    return jsonify(list(df.columns)[2:])


@app.route("/metadata/<sample>")
def sample_metadata(sample):
    # Metadata for selected sample
    # https://docs.sqlalchemy.org/en/13/orm/tutorial.html#using-textual-sql
    arguments = [
        Samples_Metadata.sample,
        Samples_Metadata.ETHNICITY,
        Samples_Metadata.GENDER,
        Samples_Metadata.AGE,
        Samples_Metadata.LOCATION,
        Samples_Metadata.BBTYPE,
        Samples_Metadata.WFREQ,
    ]

    # Query over *args for that passed in sample
    results = db.session.query(
        *arguments).filter(Samples_Metadata.sample == sample).all()

    sample_metadata = {}
    for result in results:
        sample_metadata["sample"] = result[0]
        sample_metadata["ETHNICITY"] = result[1]
        sample_metadata["GENDER"] = result[2]
        sample_metadata["AGE"] = result[3]
        sample_metadata["LOCATION"] = result[4]
        sample_metadata["BBTYPE"] = result[5]
        sample_metadata["WFREQ"] = result[6]

    # print(sample_metadata)
    return jsonify(sample_metadata)


@app.route("/samples/<sample>")
def samples(sample):
    # return 'otu_id', 'otu_labels', and 'sample_values'
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    # Filter the df for sample values larger than 1 and return otu_id, otu_label, and sample_value(sample)
    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]

    data = {
        "otu_ids": sample_data["otu_id"].values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data["otu_label"].tolist()
    }
    return jsonify(data)


if __name__ == "main":
    app.run()
