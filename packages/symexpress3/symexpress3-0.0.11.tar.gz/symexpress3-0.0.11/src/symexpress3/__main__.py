# pylint: disable=invalid-name
"""
Command line handling
"""

import sys

if __name__ == '__main__':
  from symexpress3 import symexp3cmd
  symexp3cmd.CommandLine( sys.argv )
