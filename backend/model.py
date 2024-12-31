from config import db
from werkzeug.security import generate_password_hash

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True,nullable=False)
    passhash = db.Column(db.String(256),nullable=False)
    name = db.Column(db.String(64),nullable=False)

class Sponsor(db.Model):
    __tablename__ = 'sponsors'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128),unique=True,nullable=False)
    passhash = db.Column(db.String(256),nullable=False)
    name = db.Column(db.String(64),nullable=False)
    budget = db.Column(db.Integer,nullable=False)
    industry = db.Column(db.String(64), nullable=False)
    approved = db.Column(db.Boolean, default=False, nullable=False)
    admin_rejected = db.Column(db.Boolean)
    flagged = db.Column(db.Boolean, default=False)

    campaigns = db.relationship('Campaign', back_populates='sponsor')
    ad_requests = db.relationship('AdRequest', back_populates='sponsor')

class Influencer(db.Model):
    __tablename__ = 'influencers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128),unique=True,nullable=False)
    passhash = db.Column(db.String(256),nullable=False)
    name = db.Column(db.String(64),nullable=False)
    category = db.Column(db.String(128),nullable=False)
    niche = db.Column(db.String(128),nullable=False)
    reach = db.Column(db.Integer)
    flagged = db.Column(db.Boolean, default=False)

    ad_requests = db.relationship('AdRequest', back_populates='influencer')

class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    budget = db.Column(db.Float)
    visibility = db.Column(db.String(64))  # Could be 'public' or 'private'
    goals = db.Column(db.Text)
    payment_amount = db.Column(db.Float, nullable=False)
    requirements = db.Column(db.String, nullable=False)
    flagged = db.Column(db.Boolean, default=False)

    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id'))
    sponsor = db.relationship('Sponsor', back_populates='campaigns')
    
    ad_requests = db.relationship('AdRequest', back_populates='campaign')

class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'))
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencers.id'))
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsors.id')) 
    messages = db.Column(db.Text)
    requirements = db.Column(db.Text)
    payment_amount = db.Column(db.Integer)
    status = db.Column(db.String(64), nullable=False, default='Pending')  # Could be 'Pending', 'Accepted', 'Rejected'
    sponsor_accepted = db.Column(db.Boolean, default=None)
    influencer_accepted = db.Column(db.Boolean, default=None)
    payment_status = db.Column(db.Boolean, default=False)
    
    campaign = db.relationship('Campaign', back_populates='ad_requests')
    influencer = db.relationship('Influencer', back_populates='ad_requests')
    sponsor = db.relationship('Sponsor', back_populates='ad_requests')
