# Initialise ArgumentParser
import argparse

parser = argparse.ArgumentParser(description='Configure run mode.', prog='TestArgumentParse')
parser.add_argument('-m', '--getperiodfrom', metavar='xxx', choices=['scrape', 'database'],
                    help='scrape: scraping from web page or database: fetching periods from database')
parser.add_argument('--version', action='version', version='%(prog)s 0.1')
parser.print_help()
# args = parser.parse_args('-m scrape'.split())
args = parser.parse_args()
print(vars(args))