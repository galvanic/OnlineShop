Onlineshop
==========

Overview
--------
This is a program to simplify dividing an Ocado shop bill between flatmates. The program parses the shop text to extract individual purchases, you assign each purchase and the program calculates how much each flatmate owes for their part of the shop. Everything is saved in a database so you can go back to it later.

Installation
------------
The libraries necessary to run this program are in `requirements.txt`.

```shell
git clone https://github.com/galvanic/onlineshop.git
```

[Sandman]() acts as an API client for the database so that I could practise sending API requests. It needs to run for the application to work since that's the only way it's interacting with the database at the moment:

```shell
pip install sandman
sandmanctl sqlite:///<path to the database>
```

Getting Started
---------------

You can interact with the program through:

	- a CLI:

	```shell
	python3 onlineshop-cli.py <filepath to shop receipt file>
	```

	- a GUI which works by running a local server on your computer:

	```shell
	python3 runserver.py
	```

	- directly interacting with the database by sending GET and POST requests to the API, or using [Sandman]()'s GUI. Sandman acts as an API client for the database so that I could practise sending API requests.

Future Improvements
-------------------
- Yahoo Mail API to fetch shop receipt email automatically
- Makes guesses on whose item it is based on previous shop assignments

See TODOs ...