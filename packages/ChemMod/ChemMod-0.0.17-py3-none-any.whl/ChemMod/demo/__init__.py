
# from ChemMod.equation import equation
# from ChemMod.plot import plot
# from ChemMod import ChemMod

import numpy as np
import matplotlib.pyplot as plt

__all__ = [s for s in dir() if not s.startswith("_")]

from ChemMod.demo import __all__
from ChemMod.demo._plot import plot
from ChemMod.demo._pxrd import pxrd
