
# from ChemMod.equation import equation
# from ChemMod.plot import plot
# from ChemMod import ChemMod

import numpy as np
import matplotlib.pyplot as plt

__all__ = [s for s in dir() if not s.startswith("_")]

from ChemMod.experiment import __all__
from ChemMod.experiment._experiment import pxrd

