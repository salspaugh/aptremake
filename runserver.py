
from aptremake import app
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-p", "--port", dest="port",
                        help="start server on PORT")
    parser.add_argument("-m", "--metadata", dest="metadata",
                        help="full path to metadata file")
    parser.add_argument("-s", "--host", dest="host",
                        help="start server at this IP address")
    args = parser.parse_args()
    port = int(args.port) if args.port else 5000
    if args.metadata:
        set_metadata(args.metadata)
    if args.host is None:
        app.run(debug=True, port=port)
    else:
        app.run(debug=True, port=port, host="0.0.0.0")
