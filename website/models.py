from . import db
from flask_login import UserMixin
from datetime import datetime, timezone
import pytz

manila_tz = pytz.timezone('Asia/Manila')


class emp(db.Model, UserMixin):
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    fname = db.Column(db.String(150))
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))    
    
    # Relation with Time logs
    timelogspi = db.relationship('TimeLog', backref='employee', lazy=True)
    
class TimeLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('emp.id'), nullable=False)
    date = db.Column(db.Date, default=lambda:datetime.now(manila_tz).date())
    time_in = db.Column(db.DateTime, nullable=True)
    time_out = db.Column(db.DateTime, nullable=True)
    
    def hours_worked(self):
        if self.time_in and self.time_out:
            return round((self.time_out - self.time_in).total_seconds() / 3600, 2)
        return 0    