from datetime import datetime
from flask import Flask, render_template, request, make_response
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/shuttle.db'
db = SQLAlchemy(app)

class Arrival(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stop = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    time = db.Column(db.DateTime)

    def __init__(self, stop, destination):
        self.stop = stop
        self.destination = destination
        self.time = datetime.utcnow()

    def __repr__(self):
        return '{a} to {b} at {t}'.format(a=self.stop,
                                          b=self.destination,
                                          t=self.time)


class Endpoint(object):
    def __init__(self, val, name):
        self.val = val
        self.name = name
        self.default = False


CAMBRIDGE = [Endpoint("cambridge", "Cambridge")]
OFFICES = [
    Endpoint("newton141", "141 Needham St"),
    Endpoint("kendrick", "Kendrick Street"),
]
MORNING_PICKUPS = [
    Endpoint("kendall", "Kendall Square"),
    Endpoint("central", "Central Square"),
]

def is_inbound():
    """Returns whether the shuttles are going inbound"""
    now = datetime.now()
    return now.hour < 12

def get_stops():
    if is_inbound():
        return MORNING_PICKUPS
    return OFFICES

def get_destinations():
    if is_inbound():
        return OFFICES
    return CAMBRIDGE

def get_questions():
    stops = get_stops()
    destinations = get_destinations()
    return {
        "stops":stops,
        "destinations":destinations
    }

@app.route("/")
def index():
    context = get_questions()
    return render_template("index.html", **context)

@app.route("/time", methods=["POST"])
def time():
    stop = request.form.get('stop', None)
    destination = request.form.get('destination', None)
    arrival = Arrival(stop, destination)
    db.session.add(arrival)
    db.session.commit()
    resp = make_response(
        "Thanks! Recorded that the {s} shuttle to {d} picked up at {t}"
        .format(t=datetime.utcnow(), d=destination, s=stop)
    )
    return resp

if __name__ == '__main__':
    app.run(debug=True)
