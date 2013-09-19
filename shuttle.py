from datetime import datetime
from flask import Flask, render_template, url_for
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
        return '{a} to {b} at {t}'.format(a=stop, b=destination,
                                          t=time)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/time", methods=["POST"])
def time():
    time = datetime.utcnow()
    return "Thanks! We recorded that the {d} shuttle to {s} picked up at {t}" \
      .format(t=time)

if __name__ == '__main__':
    app.run(debug=True)
