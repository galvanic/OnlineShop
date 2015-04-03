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

[Sandman]() can act as an API client for the database. It's an easy way to carry out admin stuff (like deleting flatmates) and features that I haven't yet added to the program. Sandman is however not necessary to run the program.

```shell
pip install sandman
sandmanctl sqlite:///<path to the database>
```

Getting Started
---------------

You can interact with the program through:

	- a command-line interface:

	```shell
	python3 onlineshop-cli.py <filepath to shop receipt file>
	```

	- a graphical interface which works by running a local server on your computer:

	```shell
	python3 runserver.py
	```

	- directly interacting with the database by sending GET and POST requests to the API, or using Sandman's GUI.

Future Improvements
-------------------
- Mail API to fetch shop receipt email automatically
- Makes guesses on whose item it is based on previous shop assignments

See TODOs ...
