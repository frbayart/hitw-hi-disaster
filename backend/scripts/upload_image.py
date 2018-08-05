#!/usr/bin/python
import datetime
from pymongo import MongoClient


mongo = MongoClient("mongodb://localhost:27017/hd")
print mongo.hd.disaster_zone.get_one()
