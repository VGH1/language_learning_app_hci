import glob
import os
import sys

lib_dir = os.path.join(os.path.dirname(__file__), 'lib')

for wheel in glob.glob(os.path.join(lib_dir, "*.whl")):
    sys.path.insert(0, wheel)
