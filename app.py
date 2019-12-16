from .app import create_app

app = create_app()
# mongo = mydb.get_mongo(app)
#
#
# @app.route('/')
# def hello_world():
#     return '<br>http://ip-address/person/string:name</br><br>name=test</br><br>Like \'http://123.456/person/test\'</br>'
#
#
# # @app.route('/api/route')
#
#
# @app.route('/person/<string:name>')
# def query_person(name):
#     persons = mongo.db.test.find({'name': name})
#     resp = ''.join([person['name'] for person in persons])
#     print(resp)
#     return 'Person \'' + name + '\' ' + ('Found' if resp != '' else 'Not Found')


if __name__ == '__main__':
    app.run()
