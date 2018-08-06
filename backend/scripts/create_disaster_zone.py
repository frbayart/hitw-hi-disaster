#!/usr/bin/python
import base64
import datetime
from PIL import Image
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017/hd")

with open('images_coordinates.txt') as fd:
    data = fd.read().split('\n\n')

    i = 0

    for block in data:
        image, ul, lr = block.strip().split('\n')
        ul_lat, ul_long = [float(zob) for zob in ul.split(',')]
        lr_lat, lr_long = [float(zob) for zob in lr.split(',')]
        print image + " [" + str(ul_lat) + " " + str(ul_long) + "] [" + str(lr_lat) + "] [" + str(lr_long) + "]"

        IMAGE = "../../images/hiroshima-png/" + image
        COORD = (
                (ul_lat, ul_long),
                (lr_lat, lr_long)
                )
        i += 1
        mongo.hd.disaster_zone.insert_one({
                "id": str(i),
                "doc": datetime.datetime.now().isoformat(),
                "dou": None,
                "coordinates": COORD,
                "image_size": Image.open(IMAGE).size,
                "image": 'data:image/png;base64,' + base64.b64encode(open(IMAGE).read())
            })
