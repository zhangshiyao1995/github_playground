# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 22:49:37 2019

@author: shiyao
"""

import json
import os
from db import db, Building, Level, Spot
from flask import Flask, request

db_filename = "todo.db"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/')
def hello():
    return os.environ['GOOGLE_CLIENT_ID'], 200

@app.route('/api/building/', methods=['POST'])
def create_building():
    post_body = json.loads(request.data)
    shortName = post_body.get('shortName', '')
    longName = post_body.get('longName', '')
    building = Building(
        shortName = shortName,
        longName = longName
    )
    db.session.add(building)
    db.session.commit()
    return json.dumps({'success': True, 'data': building.serialize()}), 201

@app.route('/api/buildings/')
def get_building():
    buildings = Building.query.all()
    res = {'success': True, 'data': [t.serialize() for t in buildings]}
    return json.dumps(res), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
