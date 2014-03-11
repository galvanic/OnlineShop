from bottle import route, run, template, static_file



@route('/')
@route('/<date:int>')
def shoplist(date=140303):
    return template("shoplist", date=date, rows=[[]])

run(host='localhost', port=8080, debug=True)