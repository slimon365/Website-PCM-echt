from cProfile import Profile
from cgitb import html
from email.mime import image
from enum import unique
import imp
from operator import imod
from tokenize import maybe
from unicodedata import name
import flask
from flask import Flask, render_template, request, redirect
from flask.helpers import url_for

from db import db_init, db, db2_init, db2
from models import stages, tours

app = Flask(__name__)
app.secret_key = "test123viervijf"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stages.db'
app.config['SQLALCHEMY_Track_MODIFICATIONS'] = False
db_init(app)
db2_init(app)


@app.route('/')
def main():
    return render_template('index.html', values = stages.query.all()[-10:])



@app.route('/addstage', methods=["POST", "GET"])
def addstage():
    if request.method == "POST":
        stage = request.form["stage"]
        year = request.form["year"]
        number = request.form["number"]
        if number == '':
            number = '0'
        creator = request.form["creator"]
        start = request.form["start"]
        finish = request.form["finish"]
        profile = request.form["profile"]
        link = request.form['link']
        if link == '':
            link = '0'
        if not (stages.query.filter_by(race = stage).first() and stages.query.filter_by(year = year).first() and stages.query.filter_by(number = int(number)).first() and stages.query.filter_by(creator= creator).first()):
            stg = stages(stage, year, int(number), creator, start, finish, profile, link)
            db.session.add(stg)
            db.session.commit()

        return redirect(url_for("showstage", id = stg.id))
    else:
        return render_template('addstage.html')


@app.route('/showstage/<id>')
def showstage(id):
    if stages.query.filter_by(id = id).first():
        stage = stages.query.filter_by(id = id).first()
        race0 = stage.race
        year0 = stage.year
        stagenumber0 = stage.number
        stagemaker0 = stage.creator
        start0 = stage.start
        finish0 = stage.finish
        profile0 = stage.profile
        link0 = stage.link
    else:
        return redirect(url_for('addstage'))
    return render_template('showstage.html', race=race0, year=year0, number=stagenumber0, creator=stagemaker0, start=start0, finish=finish0, profile=profile0, link=link0)


@app.route('/addtour', methods=["POST", "GET"])
def addtour():
    if request.method == "POST":
        stage = request.form["stage"]
        year = request.form["year"]
        amount = request.form["number"]
        overview = request.form["profile"]
        if overview == '':
            overview = '0'
        link = request.form['link']

        if not (tours.query.filter_by(race = stage).first() and tours.query.filter_by(year = year).first()):
            tour = tours(stage, year, int(amount), overview, link)
            db2.session.add(tour)
            db2.session.commit()

        return redirect(url_for("showtour", id = tour.id))
    else:
        return render_template('addtour.html')    


@app.route('/showtour/<id>')
def showtour(id):
    if tours.query.filter_by(id = id).first():
        tour = tours.query.filter_by(id = id).first()
        race0 = tour.race
        year0 = tour.year
        amount0 = tour.number
        overview0 = tour.overview
        link0 = tour.link
    else:
        return redirect(url_for('addtour'))
    liststages0 = []
    creators0 = []
    for i in range(amount0):
        if stages.query.filter_by(race = race0, year = year0, number = i+1).first():
            stage = stages.query.filter_by(race = race0, year = year0, number = i+1).first()
            if not stage.creator in creators0:
                creators0.append(stage.creator)
            liststages0.append((i+1, stage.id, stage.profile))
        else:
            liststages0.append((i+1, '0', '0'))     
    return render_template('showtour.html', race=race0, year=year0, amount=amount0, overview=overview0, link=link0, creators = ', '.join(creators0), liststages = liststages0)



@app.route('/stagesdatabase')
def stagesdatabase():
    return render_template('stagesdatabase.html', values = stages.query.all())


@app.route('/stagesdatabase/deleteentry/<id>')
def deleteentry(id):
    if stages.query.get(id):
        deletestage = stages.query.get(id)
        db.session.delete(deletestage)
        db.session.commit()
        return redirect(url_for('stagesdatabase'))
    else:
        return redirect(url_for('main'))


@app.route('/searchstage', methods=["POST", "GET"])
def searchstage():
    values = 0
    if request.method == "POST":
        stagename = request.form["stage"]
        creatorname = request.form["creator"]
        values = []   
        stagelist  = stages.query.all()
        if stagename and not creatorname:
            for item in stagelist:
                if stagename.lower() in item.race.lower():
                    values.append(item)
        elif creatorname and not stagename:
            for item in stagelist:
                if creatorname.lower() in item.creator.lower():
                    values.append(item)
        elif stagename and creatorname:
            for item in stagelist:
                if stagename.lower() in item.race.lower() and creatorname.lower() in item.creator.lower():
                    values.append(item)

    return render_template('searchstage.html', results = values)


@app.route('/searchtour', methods=["POST", "GET"])
def searchtour():
    values = 0
    if request.method == "POST":
        stagename = request.form["stage"]
        values = []
        if stagename:
            tourlist = tours.query.all()
            for item in tourlist:
                if stagename.lower() in item.race.lower():
                    values.append(item)

    return render_template('searchtour.html', results = values)

if __name__==("__main__"):
    app.run(debug=True)