
# from ChemMod.equation import equation
# from ChemMod.plot import plot
# from ChemMod import ChemMod

import numpy as np
import matplotlib.pyplot as plt



__all__ = [s for s in dir() if not s.startswith("_")]

from ChemMod.equation import __all__
from ChemMod.equation._element_data import element_data
from ChemMod.equation._equilibrium import equilibrium
from ChemMod.equation._M import M





