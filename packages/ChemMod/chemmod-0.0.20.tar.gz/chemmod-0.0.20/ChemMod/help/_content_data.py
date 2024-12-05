
from ChemMod.help._content import content
from ChemMod.equation._M import M
from ChemMod.equation._equilibrium import equilibrium
from ChemMod.help._info import info
from ChemMod.plot._arrhenius_plot import arrhenius_plot
from ChemMod.plot._bjerrum_plot import bjerrum_plot
from ChemMod.plot._gibbs_plot import gibbs_plot
from ChemMod.plot._theme import theme
from ChemMod.plot._order_plot import order_plot

content_data = {
    "content": {"Info": content.__doc__
    },
    "info": {"Info": info.__doc__
    },
    "content_data": {"Info":str('''content_data is a library containing descriptions of all content in ChemMod.
        \n It contains the following information about the functions:
        \n\t Info
        \n\n The data is structured as follows:
        \n\n     "content": {
        \n\t"Info": content.__doc__,
        \n\t},
        \n\nTo extract the wanted information write the following (Works for all function, we use content in this example):
        \n\tInformation:
        \n\tcontent_data['content']['Info']
    ''')
    },
    "element_data": {
        "Info": str(f'''element_data is a library containing all the elements in the periodic system.
        \n It contains the following information about the elements:
        \n\t Atomic number
        \n\t Molar mass
        \n\t Valency
        \n\t Name
        \n\t Electronegativity
        \n\n The data is structured as follows:'''
        + '''\n\n     "H": {
        \n\t"AtomicNumber": 1,
        \n\t"MolarMass": 1.008,
        \n\t"Valency": 1,
        \n\t"Name": "Hydrogen",
        \n\t"Electronegativity": 2.20
        \n\t},
        \n\nTo extract the wanted information write the following (Works for all elements, we use Helium (He) in this example):
        \n\tAtomic Number:
        \n\telement_data['He']['AtomicNumber']
        \n\tMolar Mass:
        \n\telement_data['He']['MolarMass']
        \n\tValency:
        \n\telement_data['He']['Valency']
        \n\tName:
        \n\telement_data['He']['Name']
        \n\tElectronegativity:
        \n\telement_data['He']['Electronegativity']
    ''')
    },
    "M": {"Info": M.__doc__
    },
    "gibbs_plot": {"Info":gibbs_plot.__doc__
    },
    "bjerrum_plot": {"Info":bjerrum_plot.__doc__
    },
    "order_plot": {"Info": order_plot.__doc__,
    },
    "arrhenius_plot": {"Info": arrhenius_plot.__doc__
    },
    "equilibrium": {"Info":equilibrium.__doc__
    },    
    "equilibrium": {"Info":theme.__doc__
    },
}
