
from aptremake import app
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", dest="port",
                        help="start server on PORT", metavar="PORT")
    args = parser.parse_args()
    port = int(args.port) if args.port else 5000
    app.run(debug=True, port=port)
    #app.run(debug=True, port=port, host="0.0.0.0")
