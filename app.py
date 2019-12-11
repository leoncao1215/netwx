from flask import Flask
import mydb

app = Flask(__name__)
mongo = mydb.get_mongo(app)


@app.route('/')
def hello_world():
    persons = mongo.db.test.find({'name': 'test'})
    print(persons)
    for person in persons:
        print(person)
    return 'found'


@app.route('/person/<string:name>')
def query_person(name):
    persons = mongo.db.test.find({'name': name})
    resp = ''.join([person['name'] for person in persons])
    print(resp)
    return resp


if __name__ == '__main__':
    app.run()
