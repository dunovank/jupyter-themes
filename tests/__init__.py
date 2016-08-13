import os, sys
from glob import glob

modules = glob(os.path.dirname(__file__)+"/*.py")
__all__ = [ os.path.basename(f)[:-3] for f in modules]

from .test_themes import *
