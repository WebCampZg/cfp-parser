import pymongo
import pprint
import csv
import sys
import datetime

from dateutil.parser import parse
from pymongo import MongoClient
from pprint import pprint

from settings.local import *

def main():
    # Setup a connection to mongo
    mongo = MongoClient(MONGO_URL)

    # Parse the CSV file and process each row
    with open('submissions.csv', 'r') as f:
        reader = csv.reader(f, delimiter=',')
        row_id = 1

        # Skip header
        next(reader)
        for row in reader:
            process_speaker(mongo, row)
            process_talk(mongo, row, row_id)
            row_id += 1

def process_talk(mongo, row, row_id):
    talk = {
        "row_id": row_id,
        "submitted": parse(row[0], dayfirst=True),
        "title": row[1],
        "short_abstract": row[2],
        "long_abstract": row[3],
        "language": row[4],
        "level": row[5],
        "status": "pending",
        "scores": {}
    }

    speaker = mongo.webcamp.speakers.find_one({ "email": row[7] })

    if speaker is None:
        raise Exception("Cannot find speaker with email %s" % row[7])

    talk['speaker_id'] = speaker['_id']

    talks = mongo.webcamp.talks
    count = talks.find({ 'row_id': talk['row_id'] }).count()

    if count > 0:
        return

    print "Adding talk: %s" % talk['title']
    talks.insert(talk)

def process_speaker(mongo, row):
    speaker = {
        'name': row[6],
        'email': row[7],
        'short_bio': row[8],
        'long_bio': row[9],
        'experience': row[10],
        'image': row[11],
        'shirt': row[12],
        'twitter': row[13],
        'github': row[14],
    }

    speakers = mongo.webcamp.speakers
    count = speakers.find({ 'email': speaker['email'] }).count()

    if count > 0:
        return

    print "Adding new speaker: %s" % speaker['name']
    speakers.insert(speaker)

if __name__ == '__main__':
    main()
