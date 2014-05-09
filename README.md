
## Introduction

This is a partial re-implementation of Jock Mackinlay's APT based on the 1986 Transactions on Graphics paper.

Currently there is a bug which causes only bar charts to be rendered.

Currently the only "languages" supported are:
* HorizontalAxis
* VerticalAxis
* BarChart
* Color

This means that bar charts and scatter plots can be generated.
Currently there is no support for mark labels.

## How to run aptremake

On the command line, type:

    python runserver.py

In your browser, navigate to [127.0.0.1:5000](127.0.0.1:5000)

## Dependencies

* [Flask](http://flask.pocoo.org/ "Flask")
* [SQLite](https://www.sqlite.org/ "SQLite")

## Contributing

I am happy to review PR's for contributions to this project, but before 
running off to implement a change that you would like to have merged, 
please contact me first with your idea about what you'd like to implement.
This is a research project so many parts of the code are subject to change.
That said, I have lots of ideas of things to work on for this project.
So contact me if you'd like to help but aren't sure what to work on.

