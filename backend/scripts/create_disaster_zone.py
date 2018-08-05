#!/usr/bin/python
import base64
import datetime
from PIL import Image
from pymongo import MongoClient

mongo = MongoClient("mongodb://localhost:27017/hd")

with open('penis') as penis:
    data = penis.read().split('\n\n')

    i = 0

    for block in data:
        image, ul, lr = block.strip().split('\n')
        ul_lat, ul_long = [float(zob) for zob in ul.split(',')]
        lr_lat, lr_long = [float(zob) for zob in lr.split(',')]
        print image + " [" + str(ul_lat) + " " + str(ul_long) + "] [" + str(lr_lat) + "] [" + str(lr_long) + "]"

        IMAGE = "../../hiroshima-squares/" + image
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
                "image": 'data:image/jpeg;base64,' + base64.b64encode(open(IMAGE).read())
                #"image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAAAwFBMVEXm7NK41k3w8fDv7+q01Tyy0zqv0DeqyjOszDWnxjClxC6iwCu11z6y1DvA2WbY4rCAmSXO3JZDTxOiwC3q7tyryzTs7uSqyi6tzTCmxSukwi9aaxkWGga+3FLv8Ozh6MTT36MrMwywyVBziSC01TbT5ZW9z3Xi6Mq2y2Xu8Oioxy7f572qxzvI33Tb6KvR35ilwTmvykiwzzvV36/G2IPw8O++02+btyepyDKvzzifvSmw0TmtzTbw8PAAAADx8fEC59dUAAAA50lEQVQYV13RaXPCIBAG4FiVqlhyX5o23vfVqUq6mvD//1XZJY5T9xPzzLuwgKXKslQvZSG+6UXgCnFePtBE7e/ivXP/nRvUUl7UqNclvO3rpLqofPDAD8xiu2pOntjamqRy/RqZxs81oeVzwpCwfyA8A+8mLKFku9XfI0YnSKXnSYZ7ahSII+AwrqoMmEFKriAeVrqGM4O4Z+ADZIhjg3R6LtMpWuW0ERs5zunKVHdnnnMLNQqaUS0kyKkjE1aE98b8y9x9JYHH8aZXFMKO6JFMEvhucj3Wj0kY2D92HlHbE/9Vk77mD6srRZqmVEAZAAAAAElFTkSuQmCC"
            })
