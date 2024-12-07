import argparse
import sys
from csra import __version__

def main():
    parser = argparse.ArgumentParser(description="Collect NIH NCBI SRA metadata of several GEO studies in one search")

    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s version {__version__}")
    parser.add_argument("-q", "--query", nargs="+", type=str, help="The NIH NCBI query between quotes", required=True)
    args = parser.parse_args()

    if args.query:
        if len(args.query) > 1:
            print("Error: It looks like your query isn't quoted.",file=sys.stderr)
            print("Usage: csra \"your query here\"",file=sys.stderr)
            sys.exit(1)
        else:
            query = " ".join(args.query)
            print(f"Received query: {query}")


if __name__ == "__main__":
    main()
