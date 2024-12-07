#!/bin/env python3

"""
to-do list manager
"""

from .lib import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("")
        exit()
