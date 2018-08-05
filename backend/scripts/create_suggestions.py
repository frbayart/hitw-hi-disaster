#!/usr/bin/python
import base64
import datetime
import random
from pymongo import MongoClient

X=692
Y=519



mongo = MongoClient("mongodb://localhost:27017/hd")

for penis in range(10):
    mongo.hd.suggestions.insert_one({
            "zone_id": "666",
            "disaster_type": random.randint(0, 8),
            "coordinates": [random.randint(0,X), random.randint(0,Y), random.randint(0,X), random.randint(0,Y)],
            "score": round(random.random(), 2)
        })
