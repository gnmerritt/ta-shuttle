from datetime import datetime
from flask import Flask
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
    pass

@app.route("/time", methods=["POST"])
def time():
    pass

if __name__ == '__main__':
    app.run()
