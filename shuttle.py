from datetime import datetime
from flask import Flask, render_template, request
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/time", methods=["POST"])
def time():
    stop = request.form.get('stop', None)
    destination = request.form.get('destination', None)
    arrival = Arrival(stop, destination)
    db.session.add(arrival)
    db.session.commit()
    return "Thanks! Recorded that the {s} shuttle to {d} picked up at {t}" \
      .format(t=datetime.utcnow(), d=destination, s=stop)

if __name__ == '__main__':
    app.run(debug=True)
