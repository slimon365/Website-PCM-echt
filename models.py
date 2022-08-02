from db import db, db2

class stages(db.Model):
    id = db.Column('id', db.Integer(), primary_key = True)
    race = db.Column('race', db.String(100))
    year = db.Column('year', db.Text())
    number = db.Column('number', db.Integer())
    creator = db.Column('creator', db.String(100))
    start = db.Column('start', db.String(30))
    finish = db.Column('finish', db.String(30))
    profile = db.Column('profile', db.Text())
    link = db.Column('link', db.Text())

    def __init__(self, race, year, number, creator, start, finish, profile, link):
        self.race = race
        self.year = year
        self.number = number
        self.creator = creator
        self.start = start
        self.finish = finish
        self.profile = profile
        self.link = link
    
class tours(db2.Model):
    id = db2.Column('id', db2.Integer(), primary_key = True)
    race = db2.Column('race', db2.String(100))
    year = db2.Column('year', db2.Text())
    number = db2.Column('number', db2.Integer())
    overview = db2.Column('overview', db2.Text())
    link = db2.Column('link', db2.Text())

    def __init__(self, race, year, number, overview, link):
        self.race = race
        self.year = year
        self.number = number
        self.overview = overview
        self.link = link