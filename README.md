
## Introduction

This is a partial re-implementation of Jock Mackinlay's APT based on the 1986 Transactions on Graphics paper.

Currently there is a bug which causes only bar charts to be rendered.

Currently the only "languages" supported are:
* HorizontalAxis
* VerticalAxis
* BarChart
* Color

## How to run aptremake

On the command line, type:

    python runserver.py

In your browser, navigate to [127.0.0.1:5000](127.0.0.1:5000)

## Dependencies

* [Flask](http://flask.pocoo.org/ "Flask")
* [SQLite](https://www.sqlite.org/ "SQLite")


