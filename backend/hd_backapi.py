#!/usr/bin/python3

import json
import random
import uuid
import copy
import sys
import os
import time
from base64 import b64decode
from tempfile import mkstemp
from datetime import timedelta
from six import string_types
from functools import update_wrapper
from flask import Flask, Response, request, make_response, current_app
from flask_pymongo import PyMongo

# bricolage pour importer le truc vite fait
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'tensorflow'))
from predict import suggestions


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/hd"
mongo = PyMongo(app)


def error(code, msg):
    return Response(json.dumps({"msg": msg}), status=code, mimetype='application/json')

def ok(msg):
    return Response(json.dumps(msg), status=200, mimetype='application/json')


# http://flask.pocoo.org/snippets/56/
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, string_types):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, string_types):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator




@app.route("/hd/disaster-zone", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def disaster_default_zone():
    return ok(mongo.db.disaster_zone.find_one({}, {'_id': 0}))


@app.route("/hd/disaster-zone/<zid>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def disaster_zone(zid):
    return ok(mongo.db.disaster_zone.find_one({'id': zid}, {'_id': 0}))



@app.route("/hd/disaster-zone/<zid>/disaster", methods=['POST', 'OPTIONS'])
@crossdomain(origin='*', headers="*")
def create_disaster(zid):
    try:
        data = json.loads(request.data.decode('utf-8'))
    except ValueError as e:
        return error(500, "invalid json %s"%str(e))

    data["zone_id"] = zid
    data["id"] = uuid.uuid4().hex


    # get zone info and calculate x,y to lat/long
    zoneinfo = mongo.db.disaster_zone.find_one({'id': zid}, {"coordinates": 1, "image_size": 1, '_id': 0})
   
    # from back
    latlong = zoneinfo["coordinates"]
    image_size = zoneinfo["image_size"]

    # from front / px
    x = int(data["xy_coordinates"][0])
    y = int(data["xy_coordinates"][1])

    x_unit_ppx = abs(latlong[1][1] - latlong[0][1])/float(image_size[0])
    y_unit_ppx = abs(latlong[1][0] - latlong[0][0])/float(image_size[1])

    data["coordinates"] = [
                latlong[0][0] - y * y_unit_ppx,
                latlong[0][1] + x * x_unit_ppx
            ]

    # inset_one modifies data and adds an ObjectID and c'est la meeeerde
    fuckmongo = copy.deepcopy(data)

    oid = mongo.db.disasters.insert_one(data)
    return ok(fuckmongo)



@app.route("/hd/disaster-zone/<zid>/disaster", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def get_disasters_per_zone(zid):
    results = {"results": []}
    for r in mongo.db.disasters.find({"zone_id": zid}, {'_id': 0}):
        results["results"].append(r)

    return ok(results)



@app.route("/hd/disaster-zone/<zid>/<disaster_type>", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def run_le_truc_intelligent(zid, disaster_type):
    results = {"results": []}
    #for r in mongo.db.suggestions.find({"zone_id": zid, "disaster_type": int(disaster_type)}, {'_id': 0}):
    #    results["results"].append(r)

    # get image
    img = mongo.db.disaster_zone.find_one({'id': zid}, {'image': 1, '_id': 0})['image']
    img = img[img.find(';base64,')+8:]

    fd, fname = mkstemp()
    try:
        os.write(fd, b64decode(img))
        os.close(fd)
        r = suggestions(fname, 
                os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'tensorflow', 'model100relu'), sizes = (100, 50, 25, 12, 6))

        for sug in r:
            x1, y1, x2, y2, w = sug
            results['results'].append({
                'zone_id': zid,
                'disaster_type': disaster_type,
                'coordinates': [x1, y1, x2, y2],
                'score': w
                })

    finally:
        os.unlink(fname)


    return ok(results)


@app.route('/', methods=['GET'])
def slash():
    resp = Response("hi disaster")
    resp.headers["Content-Type"] = "text/plain"
    return resp


@app.route("/hd/biere", methods=['GET', 'OPTIONS'])
@crossdomain(origin='*')
def biere():
    if not int(time.time()) % 10:
        return ok({"status": "WIN"})
    return ok({"status": "FAILED"})


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        app.run(host="0.0.0.0", processes=10)
    else:
        app.run(host="0.0.0.0", port=5001, processes=10)

