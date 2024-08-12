import sys
import db_parser

db_parser.run(db_parser.parse_args(sys.argv[1:]))