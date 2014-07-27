Webcamp CFP submissions parser
==============================

Parses submissions from a google spreadsheet and records them to a MongoDB
instance.

Installation
------------

Install prerequisites:
```
pip install -r requirements.txt
```

Setup configuration:
```
cp settings/dist.py settings/local.py
```

Edit local.py and enter required information. You will need to have a Google
account which has access to the spreadsheet. Then go into the 
[API console](https://code.google.com/apis/console/), activate the 
Drive API, and create a service account. From there, generate a P12 key, and
add a path to it to your local.py.

Usage
-----

Fetch CFP data from google drive and save it as `submissions.csv`:

```
python fetch.py
```

Parse submissions and save those which don't yet exist into MongoDB:
```
python parse.py
```
