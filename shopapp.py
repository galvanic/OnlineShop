

"""
Seems to be problem with an unclosed socket.
"""


from bottle import route, run, template, static_file
import csv


@route('/')
@route('/<date:int>')
def shoplist(date=220114):

    filepath = "%d.csv" % date
    with open(filepath, "rU") as file:
        reader = csv.reader(file)

    rows = [row for row in reader]

    from code import interact
    interact(local=dict( globals(), **locals() ))
        

    return template("shoplist", date=date, rows=[["Item 1", "Price"]])



def main():
    run(host='localhost', port=8080, debug=True)
    return


if __name__ == '__main__':
    main()