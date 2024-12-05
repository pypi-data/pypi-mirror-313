import sys
from optparse import OptionParser

from sastadev.macros import expandmacros


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="infilename",
                      help="File that contains the query to be expanded")
    parser.add_option("-q", "--query", dest="query",
                      help="query as a string")

    (options, args) = parser.parse_args()
    if options.infilename is not None:
        with open(options.infilename, 'r', encoding='utf8') as infile:
            query = infile.read()
    elif options.query is not None:
        query = options.query  # sys.argv[1]
    else:
        print('Specify a query (-q) or a filename containing a query (-f)', file=sys.stderr)
        exit(-1)
    expandedquery = expandmacros(query)
    outfilename = 'expandedqueries.txt'
    with open(outfilename, 'w', encoding='utf8') as of:
        print(expandedquery, file=of)


if __name__ == '__main__':
    main()
