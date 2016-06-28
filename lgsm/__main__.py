""" Invoke LGSM from command line
Example: python -m lgsm install
"""
import sys, os
from lgsm.core import *

if __name__ == "__main__":
	core = LGSM()
	core.execute_from_command_line()
