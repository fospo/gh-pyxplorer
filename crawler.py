import argparse
import sys
import logging
import signal
from crawler import dry_run


def signal_handler(sig, frame):
    print("Catched SIGINT, closing...")
    exit(-1)


if __name__ == "__main__":
    # general configs
    signal.signal(signal.SIGINT, signal_handler)
    logging.basicConfig(level=logging.INFO)

    ap = argparse.ArgumentParser()
    # run as -d orgName
    ap.add_argument(
        "-d",
        "--dryrun",
        required=False,
        help="Dry Run: nothing will be persisted. Org name needed.",
    )
    # run as -o orgName
    ap.add_argument(
        "-o",
        "--crawl-org",
        required=False,
        help="Complete crawl of the org with persistency. Org name needed.",
    )
    # run as -l fileWithList
    ap.add_argument(
        "-l",
        "--crawl-list",
        required=False,
        help="Complete crawl of the list with persistency. Input file needed",
    )

    args = ap.parse_args()
    if not len(sys.argv) > 1:
        logging.info("No arguments provided, check --help.")
        sys.exit(-1)

    if args.dryrun:
        logging.info("Performing dry run on " + args.dryrun)
        if not dry_run(args.dryrun):
            sys.exit(-1)

    sys.exit(0)
