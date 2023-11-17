import argparse
import sys
import logging
import signal
import json
from common import crawl, print_details, group_by_name


def signal_handler(sig, frame):
    print("Catched SIGINT, closing...")
    exit(-1)


if __name__ == "__main__":
    # general configs
    signal.signal(signal.SIGINT, signal_handler)
    logging.basicConfig(level=logging.INFO)

    ap = argparse.ArgumentParser()
    # 3 possible inputs: org, repo, list
    ap.add_argument(
        "-i", "--input", required=True, help="Input type: 'org', 'repo', or 'list'."
    )
    # name of the org, repo, or list
    ap.add_argument("name", help="Name of the organization or repository.")
    # Output expected: print at stdout, file, db [NOT IMPLEMENTED]
    ap.add_argument(
        "-o",
        "--output",
        required=False,
        default="print",
        help="Output type: 'print' or 'db'. By default, prints to stdout.",
    )

    # Fields to print
    ap.add_argument(
        "-f",
        "--fields",
        required=False,
        nargs="+",
        default=["name", "license", "language"],
        help="Fields to print: 'name', 'license', 'authors', etc.",
    )

    args = ap.parse_args()
    if args.input not in ["org", "repo", "list"]:
        logging.error("Invalid input type. Check --help.")
        sys.exit(-1)

    # TODO: implement db and file outputs
    if args.output not in ["print", "file"]:
        logging.error("Invalid output type. Check --help.")
        sys.exit(-1)

    results = crawl(args.input, args.name)
    if not results:
        logging.error("No results found. Exiting.")
        sys.exit(-1)

    # Files are always grouped by, if you want a file without grouping, just > file_name
    if args.input in ["org", "list"] and args.output == "file":
        results = group_by_name(results)
        with open("output.json", "w") as f:
            json.dump(results, f, indent=4)
    else:
        print_details(results, args.fields)

    sys.exit(-1)
