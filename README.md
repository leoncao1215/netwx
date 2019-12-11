Need to add mydb.py
```python
from flask_pymongo import PyMongo


def get_mongo(app):
    return PyMongo(app, uri='mongodb://host-ip:port/DATABASE_NAME')
```

Recommend venv by `python3 -m venv venv`, then `source venv/bin/activate`

Install dependencies using `pip3 install -r requirements.txt`