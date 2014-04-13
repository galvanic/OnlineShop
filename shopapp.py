

"""
Seems to be problem with an unclosed socket.
"""


from bottle import route, run, template, static_file
import csv
from code import interact


def getRows(date):

    filepath = "%d.csv" % date
    with open(filepath, "rU") as file:
        reader = csv.reader(file)
        rows = list(reader)

    return rows


@route('/')
@route('/<date:int>')
def shoplist(date=220114):

    rows = getRows(date)

    return template("shoplist", date=date, rows=rows)



def main():
    run(host='localhost', port=8080, debug=True)
    return


if __name__ == '__main__':
    main()
