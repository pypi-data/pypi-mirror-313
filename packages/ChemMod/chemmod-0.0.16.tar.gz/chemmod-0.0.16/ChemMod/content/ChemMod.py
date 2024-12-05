
#heyhey - Check if Chem.Mod is active

def heyhey():
	print("Hello my friend:)")

#element_data - The periodic elements dictionary from which Chem.Mod-functions extract data

element_data = {
    "H": {
        "AtomicNumber": 1,
        "MolarMass": 1.008,
        "Valency": 1,
        "Name": "Hydrogen",
        "Electronegativity": 2.20
    },
    "He": {
        "AtomicNumber": 2,
        "MolarMass": 4.0026,
        "Valency": 0,
        "Name": "Helium",
        "Electronegativity": None
    },
    "Li": {
        "AtomicNumber": 3,
        "MolarMass": 6.94,
        "Valency": 1,
        "Name": "Lithium",
        "Electronegativity": 0.98
    },
    "Be": {
        "AtomicNumber": 4,
        "MolarMass": 9.0122,
        "Valency": 2,
        "Name": "Beryllium",
        "Electronegativity": 1.57
    },
    "B": {
        "AtomicNumber": 5,
        "MolarMass": 10.81,
        "Valency": 3,
        "Name": "Boron",
        "Electronegativity": 2.04
    },
    "C": {
        "AtomicNumber": 6,
        "MolarMass": 12.011,
        "Valency": 4,
        "Name": "Carbon",
        "Electronegativity": 2.55
    },
    "N": {
        "AtomicNumber": 7,
        "MolarMass": 14.007,
        "Valency": 3,
        "Name": "Nitrogen",
        "Electronegativity": 3.04
    },
    "O": {
        "AtomicNumber": 8,
        "MolarMass": 15.999,
        "Valency": 2,
        "Name": "Oxygen",
        "Electronegativity": 3.44
    },
    "F": {
        "AtomicNumber": 9,
        "MolarMass": 18.998,
        "Valency": 1,
        "Name": "Fluorine",
        "Electronegativity": 3.98
    },
    "Ne": {
        "AtomicNumber": 10,
        "MolarMass": 20.180,
        "Valency": 0,
        "Name": "Neon",
        "Electronegativity": None
    },
    "Na": {
        "AtomicNumber": 11,
        "MolarMass": 22.990,
        "Valency": 1,
        "Name": "Sodium",
        "Electronegativity": 0.93
    },
    "Mg": {
        "AtomicNumber": 12,
        "MolarMass": 24.305,
        "Valency": 2,
        "Name": "Magnesium",
        "Electronegativity": 1.31
    },
    "Al": {
        "AtomicNumber": 13,
        "MolarMass": 26.982,
        "Valency": 3,
        "Name": "Aluminum",
        "Electronegativity": 1.61
    },
    "Si": {
        "AtomicNumber": 14,
        "MolarMass": 28.085,
        "Valency": 4,
        "Name": "Silicon",
        "Electronegativity": 1.90
    },
    "P": {
        "AtomicNumber": 15,
        "MolarMass": 30.974,
        "Valency": 3,
        "Name": "Phosphorus",
        "Electronegativity": 2.19
    },
    "S": {
        "AtomicNumber": 16,
        "MolarMass": 32.06,
        "Valency": 2,
        "Name": "Sulfur",
        "Electronegativity": 2.58
    },
    "Cl": {
        "AtomicNumber": 17,
        "MolarMass": 35.453,
        "Valency": 1,
        "Name": "Chlorine",
        "Electronegativity": 3.16
    },
    "Ar": {
        "AtomicNumber": 18,
        "MolarMass": 39.948,
        "Valency": 0,
        "Name": "Argon",
        "Electronegativity": None
    },
    "K": {
        "AtomicNumber": 19,
        "MolarMass": 39.098,
        "Valency": 1,
        "Name": "Potassium",
        "Electronegativity": 0.82
    },
    "Ca": {
        "AtomicNumber": 20,
        "MolarMass": 40.078,
        "Valency": 2,
        "Name": "Calcium",
        "Electronegativity": 1.00
    },
    "Sc": {
        "AtomicNumber": 21,
        "MolarMass": 44.956,
        "Valency": 3,
        "Name": "Scandium",
        "Electronegativity": 1.36
    },
    "Ti": {
        "AtomicNumber": 22,
        "MolarMass": 47.867,
        "Valency": 4,
        "Name": "Titanium",
        "Electronegativity": 1.54
    },
    "V": {
        "AtomicNumber": 23,
        "MolarMass": 50.942,
        "Valency": 5,
        "Name": "Vanadium",
        "Electronegativity": 1.63
    },
    "Cr": {
        "AtomicNumber": 24,
        "MolarMass": 51.996,
        "Valency": 6,
        "Name": "Chromium",
        "Electronegativity": 1.66
    },
    "Mn": {
        "AtomicNumber": 25,
        "MolarMass": 54.938,
        "Valency": 7,
        "Name": "Manganese",
        "Electronegativity": 1.55
    },
    "Fe": {
        "AtomicNumber": 26,
        "MolarMass": 55.845,
        "Valency": 2,
        "Name": "Iron",
        "Electronegativity": 1.83
    },
    "Co": {
        "AtomicNumber": 27,
        "MolarMass": 58.933,
        "Valency": 2,
        "Name": "Cobalt",
        "Electronegativity": 1.88
    },
    "Ni": {
        "AtomicNumber": 28,
        "MolarMass": 58.693,
        "Valency": 2,
        "Name": "Nickel",
        "Electronegativity": 1.91
    },
    "Cu": {
        "AtomicNumber": 29,
        "MolarMass": 63.546,
        "Valency": 1,
        "Name": "Copper",
        "Electronegativity": 1.90
    },
    "Zn": {
        "AtomicNumber": 30,
        "MolarMass": 65.38,
        "Valency": 2,
        "Name": "Zinc",
        "Electronegativity": 1.65
    },
    "Ga": {
        "AtomicNumber": 31,
        "MolarMass": 69.723,
        "Valency": 3,
        "Name": "Gallium",
        "Electronegativity": 1.81
    },
    "Ge": {
        "AtomicNumber": 32,
        "MolarMass": 72.630,
        "Valency": 4,
        "Name": "Germanium",
        "Electronegativity": 2.01
    },
    "As": {
        "AtomicNumber": 33,
        "MolarMass": 74.922,
        "Valency": 3,
        "Name": "Arsenic",
        "Electronegativity": 2.18
    },
    "Se": {
        "AtomicNumber": 34,
        "MolarMass": 78.971,
        "Valency": 2,
        "Name": "Selenium",
        "Electronegativity": 2.55
    },
    "Br": {
        "AtomicNumber": 35,
        "MolarMass": 79.904,
        "Valency": 1,
        "Name": "Bromine",
        "Electronegativity": 2.96
    },
    "Kr": {
        "AtomicNumber": 36,
        "MolarMass": 83.798,
        "Valency": 0,
        "Name": "Krypton",
        "Electronegativity": None
    },
    "Rb": {
        "AtomicNumber": 37,
        "MolarMass": 85.468,
        "Valency": 1,
        "Name": "Rubidium",
        "Electronegativity": 0.82
    },
    "Sr": {
        "AtomicNumber": 38,
        "MolarMass": 87.62,
        "Valency": 2,
        "Name": "Strontium",
        "Electronegativity": 0.95
    },
    "Y": {
        "AtomicNumber": 39,
        "MolarMass": 88.906,
        "Valency": 3,
        "Name": "Yttrium",
        "Electronegativity": 1.22
    },
    "Zr": {
        "AtomicNumber": 40,
        "MolarMass": 91.224,
        "Valency": 4,
        "Name": "Zirconium",
        "Electronegativity": 1.33
    },
    "Nb": {
        "AtomicNumber": 41,
        "MolarMass": 92.906,
        "Valency": 5,
        "Name": "Niobium",
        "Electronegativity": 1.6
    },
    "Mo": {
        "AtomicNumber": 42,
        "MolarMass": 95.951,
        "Valency": 6,
        "Name": "Molybdenum",
        "Electronegativity": 2.16
    },
    "Tc": {
        "AtomicNumber": 43,
        "MolarMass": 98.000,
        "Valency": 7,
        "Name": "Technetium",
        "Electronegativity": 1.9
    },
    "Ru": {
        "AtomicNumber": 44,
        "MolarMass": 101.07,
        "Valency": 8,
        "Name": "Ruthenium",
        "Electronegativity": 2.2
    },
    "Rh": {
        "AtomicNumber": 45,
        "MolarMass": 102.91,
        "Valency": 3,
        "Name": "Rhodium",
        "Electronegativity": 2.28
    },
    "Pd": {
        "AtomicNumber": 46,
        "MolarMass": 106.42,
        "Valency": 2,
        "Name": "Palladium",
        "Electronegativity": 2.2
    },
    "Ag": {
        "AtomicNumber": 47,
        "MolarMass": 107.87,
        "Valency": 1,
        "Name": "Silver",
        "Electronegativity": 1.93
    },
    "Cd": {
        "AtomicNumber": 48,
        "MolarMass": 112.41,
        "Valency": 2,
        "Name": "Cadmium",
        "Electronegativity": 1.69
    },
    "In": {
        "AtomicNumber": 49,
        "MolarMass": 114.82,
        "Valency": 3,
        "Name": "Indium",
        "Electronegativity": 1.78
    },
    "Sn": {
        "AtomicNumber": 50,
        "MolarMass": 118.71,
        "Valency": 4,
        "Name": "Tin",
        "Electronegativity": 1.96
    },
    "Sb": {
        "AtomicNumber": 51,
        "MolarMass": 121.76,
        "Valency": 3,
        "Name": "Antimony",
        "Electronegativity": 2.05
    },
    "Te": {
        "AtomicNumber": 52,
        "MolarMass": 127.60,
        "Valency": 2,
        "Name": "Tellurium",
        "Electronegativity": 2.1
    },
    "I": {
        "AtomicNumber": 53,
        "MolarMass": 126.90,
        "Valency": 1,
        "Name": "Iodine",
        "Electronegativity": 2.66
    },
    "Xe": {
        "AtomicNumber": 54,
        "MolarMass": 131.29,
        "Valency": 0,
        "Name": "Xenon",
        "Electronegativity": 2.6
    },
    "Cs": {
        "AtomicNumber": 55,
        "MolarMass": 132.91,
        "Valency": 1,
        "Name": "Cesium",
        "Electronegativity": 0.79
    },
    "Ba": {
        "AtomicNumber": 56,
        "MolarMass": 137.33,
        "Valency": 2,
        "Name": "Barium",
        "Electronegativity": 0.89
    },
    "La": {
        "AtomicNumber": 57,
        "MolarMass": 138.91,
        "Valency": 3,
        "Name": "Lanthanum",
        "Electronegativity": 1.10
    },
    "Ce": {
        "AtomicNumber": 58,
        "MolarMass": 140.12,
        "Valency": 3,
        "Name": "Cerium",
        "Electronegativity": 1.12
    },
    "Pr": {
        "AtomicNumber": 59,
        "MolarMass": 140.91,
        "Valency": 3,
        "Name": "Praseodymium",
        "Electronegativity": 1.13
    },
    "Nd": {
        "AtomicNumber": 60,
        "MolarMass": 144.24,
        "Valency": 3,
        "Name": "Neodymium",
        "Electronegativity": 1.14
    },
    "Pm": {
        "AtomicNumber": 61,
        "MolarMass": 145.00,
        "Valency": 3,
        "Name": "Promethium",
        "Electronegativity": 1.13
    },
    "Sm": {
        "AtomicNumber": 62,
        "MolarMass": 150.36,
        "Valency": 3,
        "Name": "Samarium",
        "Electronegativity": 1.17
    },
    "Eu": {
        "AtomicNumber": 63,
        "MolarMass": 152.00,
        "Valency": 3,
        "Name": "Europium",
        "Electronegativity": 1.2
    },
    "Gd": {
        "AtomicNumber": 64,
        "MolarMass": 157.25,
        "Valency": 3,
        "Name": "Gadolinium",
        "Electronegativity": 1.20
    },
    "Tb": {
        "AtomicNumber": 65,
        "MolarMass": 158.93,
        "Valency": 3,
        "Name": "Terbium",
        "Electronegativity": 1.20
    },
    "Dy": {
        "AtomicNumber": 66,
        "MolarMass": 162.50,
        "Valency": 3,
        "Name": "Dysprosium",
        "Electronegativity": 1.22
    },
    "Ho": {
        "AtomicNumber": 67,
        "MolarMass": 164.93,
        "Valency": 3,
        "Name": "Holmium",
        "Electronegativity": 1.23
    },
    "Er": {
        "AtomicNumber": 68,
        "MolarMass": 167.26,
        "Valency": 3,
        "Name": "Erbium",
        "Electronegativity": 1.24
    },
    "Tm": {
        "AtomicNumber": 69,
        "MolarMass": 168.93,
        "Valency": 3,
        "Name": "Thulium",
        "Electronegativity": 1.25
    },
    "Yb": {
        "AtomicNumber": 70,
        "MolarMass": 173.05,
        "Valency": 3,
        "Name": "Ytterbium",
        "Electronegativity": 1.1
    },
    "Lu": {
        "AtomicNumber": 71,
        "MolarMass": 175.00,
        "Valency": 3,
        "Name": "Lutetium",
        "Electronegativity": 1.27
    },
    "Hf": {
        "AtomicNumber": 72,
        "MolarMass": 178.49,
        "Valency": 4,
        "Name": "Hafnium",
        "Electronegativity": 1.3
    },
    "Ta": {
        "AtomicNumber": 73,
        "MolarMass": 180.95,
        "Valency": 5,
        "Name": "Tantalum",
        "Electronegativity": 1.5
    },
    "W": {
        "AtomicNumber": 74,
        "MolarMass": 183.84,
        "Valency": 6,
        "Name": "Tungsten",
        "Electronegativity": 2.36
    },
    "Re": {
        "AtomicNumber": 75,
        "MolarMass": 186.21,
        "Valency": 7,
        "Name": "Rhenium",
        "Electronegativity": 1.9
    },
    "Os": {
        "AtomicNumber": 76,
        "MolarMass": 190.23,
        "Valency": 8,
        "Name": "Osmium",
        "Electronegativity": 2.2
    },
    "Ir": {
        "AtomicNumber": 77,
        "MolarMass": 192.22,
        "Valency": 3,
        "Name": "Iridium",
        "Electronegativity": 2.20
    },
    "Pt": {
        "AtomicNumber": 78,
        "MolarMass": 195.08,
        "Valency": 2,
        "Name": "Platinum",
        "Electronegativity": 2.28
    },
    "Au": {
        "AtomicNumber": 79,
        "MolarMass": 196.97,
        "Valency": 1,
        "Name": "Gold",
        "Electronegativity": 2.54
    },
    "Hg": {
        "AtomicNumber": 80,
        "MolarMass": 200.59,
        "Valency": 2,
        "Name": "Mercury",
        "Electronegativity": 2.00
    },
    "Tl": {
        "AtomicNumber": 81,
        "MolarMass": 204.38,
        "Valency": 1,
        "Name": "Thallium",
        "Electronegativity": 1.62
    },
    "Pb": {
        "AtomicNumber": 82,
        "MolarMass": 207.2,
        "Valency": 2,
        "Name": "Lead",
        "Electronegativity": 2.33
    },
    "Bi": {
        "AtomicNumber": 83,
        "MolarMass": 208.98,
        "Valency": 3,
        "Name": "Bismuth",
        "Electronegativity": 2.02
    },
    "Po": {
        "AtomicNumber": 84,
        "MolarMass": 209.98,
        "Valency": 4,
        "Name": "Polonium",
        "Electronegativity": 2.0
    },
    "At": {
        "AtomicNumber": 85,
        "MolarMass": 210.00,
        "Valency": 1,
        "Name": "Astatine",
        "Electronegativity": 2.2
    },
    "Rn": {
        "AtomicNumber": 86,
        "MolarMass": 222.00,
        "Valency": 0,
        "Name": "Radon",
        "Electronegativity": None
    },
    "Fr": {
        "AtomicNumber": 87,
        "MolarMass": 223.00,
        "Valency": 1,
        "Name": "Francium",
        "Electronegativity": 0.7
    },
    "Ra": {
        "AtomicNumber": 88,
        "MolarMass": 226.00,
        "Valency": 2,
        "Name": "Radium",
        "Electronegativity": 0.89
    },
    "Ac": {
        "AtomicNumber": 89,
        "MolarMass": 227.00,
        "Valency": 3,
        "Name": "Actinium",
        "Electronegativity": 1.1
    },
    "Th": {
        "AtomicNumber": 90,
        "MolarMass": 232.04,
        "Valency": 4,
        "Name": "Thorium",
        "Electronegativity": 1.3
    },
    "Pa": {
        "AtomicNumber": 91,
        "MolarMass": 231.04,
        "Valency": 5,
        "Name": "Protactinium",
        "Electronegativity": 1.5
    },
    "U": {
        "AtomicNumber": 92,
        "MolarMass": 238.03,
        "Valency": 6,
        "Name": "Uranium",
        "Electronegativity": 1.38
    },
    "Np": {
        "AtomicNumber": 93,
        "MolarMass": 237.00,
        "Valency": 7,
        "Name": "Neptunium",
        "Electronegativity": 1.36
    },
    "Pu": {
        "AtomicNumber": 94,
        "MolarMass": 244.00,
        "Valency": 8,
        "Name": "Plutonium",
        "Electronegativity": 1.28
    },
    "Am": {
        "AtomicNumber": 95,
        "MolarMass": 243.00,
        "Valency": 6,
        "Name": "Americium",
        "Electronegativity": 1.3
    },
    "Cm": {
        "AtomicNumber": 96,
        "MolarMass": 247.00,
        "Valency": 6,
        "Name": "Curium",
        "Electronegativity": 1.3
    },
    "Bk": {
        "AtomicNumber": 97,
        "MolarMass": 247.00,
        "Valency": 6,
        "Name": "Berkelium",
        "Electronegativity": 1.3
    },
    "Cf": {
        "AtomicNumber": 98,
        "MolarMass": 251.00,
        "Valency": 6,
        "Name": "Californium",
        "Electronegativity": 1.3
    },
    "Es": {
        "AtomicNumber": 99,
        "MolarMass": 252.00,
        "Valency": 6,
        "Name": "Einsteinium",
        "Electronegativity": 1.3
    },
    "Fm": {
        "AtomicNumber": 100,
        "MolarMass": 257.00,
        "Valency": 6,
        "Name": "Fermium",
        "Electronegativity": 1.3
    },
    "Md": {
        "AtomicNumber": 101,
        "MolarMass": 258.00,
        "Valency": 6,
        "Name": "Mendelevium",
        "Electronegativity": 1.3
    },
    "No": {
        "AtomicNumber": 102,
        "MolarMass": 259.00,
        "Valency": 6,
        "Name": "Nobelium",
        "Electronegativity": 1.3
    },
    "Lr": {
        "AtomicNumber": 103,
        "MolarMass": 262.00,
        "Valency": 6,
        "Name": "Lawrencium",
        "Electronegativity": 1.3
    },
    "Rf": {
        "AtomicNumber": 104,
        "MolarMass": 267.00,
        "Valency": 4,
        "Name": "Rutherfordium",
        "Electronegativity": None
    },
    "Db": {
        "AtomicNumber": 105,
        "MolarMass": 270.00,
        "Valency": 5,
        "Name": "Dubnium",
        "Electronegativity": None
    },
    "Sg": {
        "AtomicNumber": 106,
        "MolarMass": 269.00,
        "Valency": 6,
        "Name": "Seaborgium",
        "Electronegativity": None
    },
    "Bh": {
        "AtomicNumber": 107,
        "MolarMass": 270.00,
        "Valency": 7,
        "Name": "Bohrium",
        "Electronegativity": None
    },
    "Hs": {
        "AtomicNumber": 108,
        "MolarMass": 277.00,
        "Valency": 8,
        "Name": "Hassium",
        "Electronegativity": None
    },
    "Mt": {
        "AtomicNumber": 109,
        "MolarMass": 278.00,
        "Valency": 9,
        "Name": "Meitnerium",
        "Electronegativity": None
    },
    "Ds": {
        "AtomicNumber": 110,
        "MolarMass": 281.00,
        "Valency": 10,
        "Name": "Darmstadtium",
        "Electronegativity": None
    },
    "Rg": {
        "AtomicNumber": 111,
        "MolarMass": 281.00,
        "Valency": 11,
        "Name": "Roentgenium",
        "Electronegativity": None
    },
    "Cn": {
        "AtomicNumber": 112,
        "MolarMass": 285.00,
        "Valency": 12,
        "Name": "Copernicium",
        "Electronegativity": None
    },
    "Nh": {
        "AtomicNumber": 113,
        "MolarMass": None,
        "Valency": 13,
        "Name": "Nihonium",
        "Electronegativity": None
    },
    "Fl": {
        "AtomicNumber": 114,
        "MolarMass": None,
        "Valency": 14,
        "Name": "Flerovium",
        "Electronegativity": None
    },
    "Mc": {
        "AtomicNumber": 115,
        "MolarMass": None,
        "Valency": 15,
        "Name": "Moscovium",
        "Electronegativity": None
    },
    "Lv": {
        "AtomicNumber": 116,
        "MolarMass": None,
        "Valency": 16,
        "Name": "Livermorium",
        "Electronegativity": None
    },
    "Ts": {
        "AtomicNumber": 117,
        "MolarMass": None,
        "Valency": 17,
        "Name": "Tennessine",
        "Electronegativity": None
    },
    "Og": {
        "AtomicNumber": 118,
        "MolarMass": None,
        "Valency": 18,
        "Name": "Oganesson",
        "Electronegativity": None
    }
}

#M - Find molar masses of different atoms and molecules by inputting a string

def M(molecule):
  if type(molecule)!=str:
    raise TypeError(type(molecule),molecule,"STOP wtf I want a f*cking string dumb ass")
  else:
    molarmass=0
    molecule1=molecule.split()
    molecule_atoms=[]
    molecule_n_atoms=[]
    for i in range(len(molecule1)):
      try:
        molecule_n_atoms.append(int(molecule1[i]))
      except ValueError:
        molecule_atoms.append(molecule1[i])
        try:
          a=int(molecule1[i+1])
        except ValueError:
          molecule_n_atoms.append(int(1))
        except IndexError:
          molecule_n_atoms.append(int(1))
    for i in range(len(molecule_atoms)):
      molarmass+=molecule_n_atoms[i]*element_data[molecule_atoms[i]]['MolarMass']
  return molarmass
 
#buffer_opskrift - Giver en opskrift på bufferen Opgave 2

def buffer_opskrift(pk_a_b, ph, bufferstyrke, syre = False, base = False, salt = None, mass = None, proton = 0, dele = 1):


  if syre == True and base == False:
    buffer = 10**(ph - pk_a_b)
    if buffer > 1:
      mængde = buffer + 1
      alt = bufferstyrke*mængde
      alt_s = (bufferstyrke+(proton*alt))

    else:
      buffer = 1/buffer
      mængde = buffer + 1
      alt = bufferstyrke*mængde
      alt_s = (alt-bufferstyrke)+(proton*alt)

    buffer_opskr = print(f'Opskrift: \n {alt_s/2:.4} L  2 M HCL afmåles og overføres til en 1 L volumetrisk flaske. \n {alt/dele:.4} M * {mass:.4} g/mol = {alt/dele*mass:.4} g {salt} afvejes i et bægerglas og tilsættes LANGSOMT til den volumetriske flaske. \n Bægerglasset vaskes med 2 gange 0,050 L vand, der overføres til den volumetriske flaske. \n Når væsken har nået stuetemperatur, fyldes der op til 1L med vand')
  
  elif base == True and syre == False:

    buffer = 10**(ph - pk_a_b)

    if buffer > 1:
      mængde = buffer + 1
      alt = bufferstyrke*mængde
      alt_b = (alt-bufferstyrke)+(proton*alt)

    else:
      buffer = 1/buffer
      mængde = buffer + 1
      alt = bufferstyrke*mængde
      alt_b = bufferstyrke+(proton*alt)

    buffer_opskr = print(f'Opskrift: \n {alt_b:.4} L 1 M NaOH afmåles og overføres til en 1 L volumetrisk flaske. \n {alt/dele:.4} M * {mass:.4} g/mol = {alt/dele*mass:.4} g {salt} afvejes i et bægerglas og tilsættes LANGSOMT til den volumetriske flaske. \n Bægerglasset vaskes med 2 gange 0,050 L vand, der overføres til den volumetriske flaske. \n Når væsken har nået stuetemperatur, fyldes der op til 1 L med vand')

  else:
    buffer_opskr = ':('

  return buffer_opskr
  
#gibbs_plot - Plot Gibbs energy as a function of temperature and calculate Gibbs energies from given temperature entries

def gibbs_plot(enthalpy=[],entropy=[],temperatures=[],initial_temperature=0,final_temperature=1000,names=['Reaction1','Reaction2','Reaction3','Reaction4','Reaction5','Reaction6','Reaction7']):

  import matplotlib.pyplot as plt
  import numpy as np

  if len(enthalpy)<1 or len(entropy)<1:
    n_reactions=int(eval(input("Hello there beautiful person, how many reactions do you want to plot: ")))
    initial_temperature=int(eval(input("\nYou are pretty hot, but can you please enter the initial temperature ( K ): ")))
    final_temperature=int(eval(input("\nAaand the final temperature ( K ): ")))

    enthalpy=[]
    entropy=[]
    names=[]

    for i in range(n_reactions):
      print(f"\nReaction {i+1}:")
      enthalpy.append(float(eval(input(f"\nEnter enthalpy ( kJ/mol ): "))))
      entropy.append(float(eval(input(f"Enter entropy ( kJ/K\u22C5mol ): "))))
      names.append(str(input("Enter name of reaction: ")))

  if len(temperatures) == 0:
    n_temperatures=int(eval(input("\nHow many temperatures do you want to find \u0394G for: ")))
    print('\n')

    temperatures=[]

    for i in range(n_temperatures):
      temperatures.append(abs(float(eval(input(f"Enter temperature {i+1} ( K ): ")))))

  print('\n')

  T = np.linspace(initial_temperature,final_temperature,final_temperature+1)

  viridis = plt.colormaps['viridis'].resampled(len(temperatures))


  font = {'family': 'serif',
          'color':  'teal',
          'weight': 'bold',
          'size': 20,

          }

  font1 = {'family': 'serif',
          'color':  'teal',
          'weight': 'bold',
          'size': 15,
          }

  font2 = {'family': 'serif',
        'color':  'teal',
        'weight': 'bold',
        'size': 8,
        }

  gibbs=plt.figure(facecolor='paleturquoise')
  ax=plt.axes()


  ax.set_facecolor('lightcyan')
  ax.set_alpha(0.1)
  ax.spines["top"].set_color("teal")
  ax.spines["bottom"].set_color("teal")
  ax.spines["left"].set_color("teal")
  ax.spines["right"].set_color("teal")
  ax.tick_params(axis='x', colors='teal',labelsize=10)
  ax.tick_params(axis='y', colors='teal',labelsize=10)
  ax.set_xlabel('',fontdict=font1)
  ax.set_ylabel('',fontdict=font1)

  legend_ncols=1
  n_labels=0

  for i in range(len(enthalpy)):
    plt.plot(T,(enthalpy[i]-T*entropy[i]),label=f'{names[i]}')
    if len(temperatures) != 0:
      for j in range(len(temperatures)):
        plt.plot(temperatures[j],(enthalpy[i]-temperatures[j]*entropy[i]),label=f'T={temperatures[j]} $\Delta$G = {round(enthalpy[i]-temperatures[j]*entropy[i],2)} kJ/mol',marker='o',color=viridis(j,1))
        n_labels+=1
        if n_labels % 15 == 0:
          legend_ncols+=1


  plt.legend(loc='center left',bbox_to_anchor=(1, 0,legend_ncols*(0.5),1.1), bbox_transform=None,mode="expand", borderpad=1, fontsize=9, title='Reactions',title_fontsize=12,facecolor='lightcyan',edgecolor='teal', shadow=True, fancybox=True,labelcolor='teal', framealpha=1,ncols=legend_ncols,columnspacing=1000)
  plt.grid(color='paleturquoise')
  plt.ylabel(f'Gibbs Energy ( $kJ/mol$ )\n\n',fontdict=font1)
  plt.xlabel('\nTemperature ( $K$ )\n',fontdict=font1)
  plt.title('\n\t$\Delta$Gibbs energy as a function of Temperature\t\t\n', fontdict=font,ha='center')
  plt.text((legend_ncols*0.5)+0.9,-0.3,f'©Chem.Mod', fontdict=font2, ha='center',verticalalignment='center', transform=ax.transAxes)

  return gibbs
  
  
  #bjerrum_plot - Plot the molar fraction of acids and their conjugate base. Extract molar % of acid from a given pH-value
  
def bjerrum_plot(pKa=[],optimalpH=7,pHvalues=[],Ka=[],acidname=['...','...','...','...','...','...','...','(: No names?']):

  import matplotlib.pyplot as plt
  import numpy as np


  if len(pKa)<1 and len(Ka)<1:
    n_reactions=int(eval(input("Hello there young padawan,\n how many equilibrium reactions do you want to plot?: ")))

    pKa=[]
    acidname=[]

    for i in range(n_reactions):
      print(f"\nReaction {i+1}:")
      pKa.append(float(eval(input("\nEnter pKa-value: "))))
      acidname.append(str(input("Enter the name of the acid: ")))

    acidname.append(str(input("\nEnter the name of the conjugate base: ")))

  if optimalpH == 7:
    optimalpH = int(eval(input("\nEnter the wanted pH-value for your buffer: ")))

  if len(pHvalues) == 0:
    n_pHvalues=int(eval(input("\nHow many pH values do you want to find concentrations for: ")))
    print('\n')

    pHvalues=[]

    for i in range(n_pHvalues):
      pHvalues.append(abs(float(eval(input(f"Enter pH {i+1}: ")))))

  print('\n')

    
  def formatmolecules(a):
    import copy
    a1=copy.copy(a)
    a2=copy.copy(a)

    get_n=[]
    pos_slut=[]
    pos_start=[]

    for k in range(len(a1)):
      if a1.upper()[k] == a1[k] and a1[k]!=' ':
        a2=a2.replace(a1[k],f" {a1[k]}")

    a1ny=a2.split()
    a2ny=a2.split()


    for i in range(len(a1ny)):
      if a1ny[i] == ')':
        get_n.append(a1ny[i+1])
        pos_slut.append(i)

      elif a1ny[i] == '(':
        pos_start.append(i)

    for q in range(len(get_n)):
      for j in range(pos_start[q]+1,pos_slut[q]):

        if a1ny[j+1].lower() != a1ny[j+1] or a1ny[j+1]==')':
          try:
            test=int(a1ny[j])
            a2ny[j] = int(a1ny[j])*int(get_n[q])
          except ValueError:
            a2ny[j]=f"{a1ny[j]} {get_n[q]}"

    a2nyny=copy.copy(a2ny)

    count=0

    for r in range(len(get_n)):
      a2nyny.pop(pos_slut[r]+1)
      try:
        count+=1
        pos_slut[r+1]-=count
        print(pos_slut)
      except IndexError:
        break


    aresult = " ".join(str(i) for i in a2nyny)

    aresult=aresult.replace('(','')
    aresult=aresult.replace(')','')

    return aresult


  names = []

  for i in range(len(acidname)):
    names.append(formatmolecules(acidname[i]))

  Mnames = []

  for i in range(len(names)):
    try:
      Mnames.append(M(names[i]))
    except KeyError:
      plot_title = ''
      break

  count_rights = 0

  for i in range(len(Mnames)-1):
    if abs(Mnames[i] - Mnames[i+1]) < 1.2:
      count_rights += 1

  plot_title=''

  if count_rights == len(Mnames)-1:
    plot_title = acidname[0]
  elif len(acidname) < 2:
    plot_title = acidname[0]

  if len(Ka) == 0:
    Ka = [10**(pKa[i]) for i in range(len(pKa))]

  if len(pKa) == 0:
    pKa = [np.log10(Ka[i]) for i in range(len(pKa))]

  viridis = plt.colormaps['viridis'].resampled(len(pHvalues))

  pH = np.linspace(0,14,1500)

  x_ticks=np.linspace(0,14,15)

  font = {'family': 'serif',
          'color':  'teal',
          'weight': 'bold',
          'size': 20,
          #'backgroundcolor':'lightblue'
          }

  font1 = {'family': 'serif',
          'color':  'teal',
          'weight': 'bold',
          'size': 15,
          }

  font2 = {'family': 'serif',
        'color':  'teal',
        'weight': 'bold',
        'size': 8,
        }

  bjerrum=plt.figure(facecolor='paleturquoise')
  ax=plt.axes()


  ax.set_facecolor('lightcyan')
  ax.set_alpha(0.1)
  ax.spines["top"].set_color("teal")
  ax.spines["bottom"].set_color("teal")
  ax.spines["left"].set_color("teal")
  ax.spines["right"].set_color("teal")
  ax.tick_params(axis='x', colors='teal',labelsize=10)
  ax.tick_params(axis='y', colors='teal',labelsize=10)
  ax.set_xlabel('',fontdict=font1)
  ax.set_ylabel('',fontdict=font1)

  legend_ncols=1
  n_labels=0


  for i in range(len(pKa)):
    plt.plot(pH,(1 / ( 1 + 10**(  pH - (pKa[i])  ) )),label=f'{acidname[i]}')

    if len(pKa)<5:

      if i != 0:
        distance = pKa[i] - pKa[i-1]
      else:
        distance = pKa[i]

      if distance>0.7:
        plt.text(pKa[i]-0.5*distance-0.2,0.5, f'{acidname[i]}',va='center_baseline',rotation=90, fontdict=font1,)

    for j in range(len(pHvalues)):
      plt.plot(pHvalues[j],(1 / ( 1 + 10**(  pHvalues[j] - (pKa[i])  ) )),label=f'pH = {pHvalues[j]}:  ({acidname[i]}) = {round((1 / ( 1 + 10**(  pHvalues[j] - (pKa[i] ) ) ))*100,1)} %',marker='o',color=viridis(j,1))
      n_labels+=1
      if n_labels % 15 == 0:
        legend_ncols+=1

  if len(pKa)<5:
    plt.text(pKa[-1]+1, 0.5, f'{acidname[-1]}\n\n\n',va='center', rotation=90, fontdict=font1)


  plt.axvline(x = optimalpH, color = 'teal', label = f'pH = {optimalpH}',dash_capstyle='projecting', lw=2.5, dashes=(4,5),  )
  plt.axvspan(optimalpH+1, optimalpH-1, facecolor='teal', alpha=0.2 , hatch='*', ec='teal')
  plt.legend(loc='center left',bbox_to_anchor=(1, 0,legend_ncols*(0.5)+0.1,1.1), bbox_transform=None,mode="expand", borderpad=1, fontsize=9, title='Reactions',title_fontsize=12,facecolor='lightcyan',edgecolor='teal', shadow=True, fancybox=True,labelcolor='teal', framealpha=1,ncols=legend_ncols,columnspacing=1000)
  plt.grid(color='paleturquoise')
  plt.ylabel(f'\nMolar fraction of acids\n\n',fontdict=font1)
  plt.xlabel('\npH\n',fontdict=font1, )
  plt.xticks(x_ticks)
  plt.title(f'\nBjerrum Plot {plot_title}\n', fontdict=font)
  plt.text((legend_ncols*0.5)+1,-0.3,f'©Chem.Mod', fontdict=font2, ha='center',verticalalignment='center', transform=ax.transAxes)

  return bjerrum
  

#order_plot - Raction Kinetics. Find the order of the reaction by linear regression.

def order_plot(c=[],time=[],names=['Reaction1','Reaction2','Reaction3','Reaction4','Reaction5','Reaction6','Reaction7']):


  import matplotlib.pyplot as plt
  import numpy as np


  def alpha(R, beta):
    alpha= np.mean(R[1]) - ( beta * np.mean(R[0]) )
    return alpha

  def beta(R):

    n = len(R[0])

    sumxx=0
    sumxy=0

    for i in range(1,n):
      sumxy += ( R[0][i] - np.mean(R[0]) ) * ( R[1][i] - np.mean(R[1]) )
      sumxx += ( R[0][i] - np.mean(R[0]) )**2

    beta = ( sumxy ) / ( sumxx )

    return beta

  def linear(x, alpha, beta):

    n = len(x)

    linear = []

    for i in range(len(x)):
      linear.append( ( alpha + beta * x[i] ) )

    return linear

  def rxy(R,linear):

    SS_res = np.sum(( R[1] - linear )**2 )

    SS_tot = np.sum( ( R[1] - np.mean(R[1]) )**2 )

    rxy=1-(SS_res/SS_tot)

    return abs(rxy)


  if len(c)<1:
    c=[]
    names=[]
    time=[]

    c=list(eval(input(f"\nEnter a list of concentrations ( M ): ")))
    time=list(eval(input(f"\nEnter a list of timesteps ( s ): ")))
    names.append(str(input("Enter name of reaction: ")))

  print('\n')



  font = {'family': 'serif',
          'color':  'teal',
          'weight': 'bold',
          'size': 20,

          }

  font1 = {'family': 'serif',
          'color':  'teal',
          'weight': 'bold',
          'size': 14,
          }

  font2 = {'family': 'serif',
        'color':  'teal',
        'weight': 'bold',
        'size': 8,
        }

  order=plt.figure(facecolor='paleturquoise',figsize=(8,12))

  ax=plt.axes()
  ax.remove()

  legend_ncols=1

  cinv=[1/(c[k]) for k in range(len(c))]
  clog=[np.log(c[j]) for j in range(len(c))]

  R1=np.array([time,c])
  R2=np.array([time,clog])
  R3=np.array([time,cinv])

  b1, b2, b3 = beta(R1), beta(R2), beta(R3)
  a1, a2, a3 = alpha(R1,b1), alpha(R2,b2), alpha(R3,b3)
  l1, l2, l3 = linear(time, a1, b1), linear(time,a2,b2), linear(time,a3,b3)
  rxy1, rxy2, rxy3 = rxy(R1,l1), rxy(R2,l2), rxy(R3,l3)

  plt.subplot(3,1,1)
  plt.scatter(time,c,label=f'0. Order\nConcentrations\nR$^2$ = {round(round(rxy1,2)*100,2)} %\nSlope = k = {round(b1,4)} M/s \nIntercept = {round(a1,4)}')
  plt.plot(time,l1)
  plt.legend(loc='center left',bbox_to_anchor=(1, 0,legend_ncols*(0.5),1.1), bbox_transform=None,mode="expand", borderpad=1, fontsize=12,facecolor='lightcyan',edgecolor='teal', shadow=True, fancybox=True,labelcolor='teal', framealpha=1,ncols=legend_ncols,columnspacing=1000)
  plt.grid(color='paleturquoise')
  plt.title('\nLinear regression for the first 3 reaction orders\n', fontdict=font,ha='center')
  plt.text((legend_ncols*0.5)+0.9,-0.1,f'©Chem.Mod', fontdict=font2, ha='center',verticalalignment='center', transform=ax.transAxes)
  plt.ylabel(f'Concentrations ( $mol/L$ )\n\n',fontdict=font1)


  plt.subplot(3,1,2)
  plt.scatter(time,clog,color='red',label=f'1. Order\nln(Concentrations)\nR$^2$ = {round(round(rxy2,2)*100,2)} %\nSlope = k = {round(b2,4)} 1/s \nIntercept = {round(a2,4)}')
  plt.plot(time,l2,color='red')
  plt.legend(loc='center left',bbox_to_anchor=(1, 0,legend_ncols*(0.5),1.1), bbox_transform=None,mode="expand", borderpad=1, fontsize=12,facecolor='lightcyan',edgecolor='teal', shadow=True, fancybox=True,labelcolor='teal', framealpha=1,ncols=legend_ncols,columnspacing=1000)
  plt.grid(color='paleturquoise')
  plt.ylabel(f'Concentrations ( $ln(mol/L)$ )\n\n',fontdict=font1)


  plt.subplot(3,1,3)
  plt.scatter(time,cinv,color='green',label=f'2. Order\nConcentrations$^-$$^1$\nR$^2$ = {round(round(rxy3,2)*100,2)} %\nSlope = k = {round(b3,4)} 1/(M \u22C5 s) \nIntercept = {round(a3,4)}')
  plt.plot(time,l3,color='green')
  plt.legend(loc='center left',bbox_to_anchor=(1, 0,legend_ncols*(0.5),1.1), bbox_transform=None,mode="expand", borderpad=1, fontsize=12,facecolor='lightcyan',edgecolor='teal', shadow=True, fancybox=True,labelcolor='teal', framealpha=1,ncols=legend_ncols,columnspacing=1000)
  plt.grid(color='paleturquoise')
  plt.xlabel('\nTime ( $s$ )\n',fontdict=font1)
  plt.ylabel(f'Concentrations ( $1/(mol/L)$ )\n\n',fontdict=font1)

  return order
  
#arrhenius_plot - Calculate activation energy for reaction by linear reaction of rate constant and temperature. 

def arrhenius_plot(k=[],temperature=[],R=8.314,names=['Reaction1','Reaction2','Reaction3','Reaction4','Reaction5','Reaction6','Reaction7']):

  import matplotlib.pyplot as plt
  import numpy as np


  def alpha(R, beta):
    alpha= np.mean(R[1]) - ( beta * np.mean(R[0]) )
    return alpha

  def beta(R):

    n = len(R[0])

    sumxx=0
    sumxy=0

    for i in range(1,n):
      sumxy += ( R[0][i] - np.mean(R[0]) ) * ( R[1][i] - np.mean(R[1]) )
      sumxx += ( R[0][i] - np.mean(R[0]) )**2

    beta = ( sumxy ) / ( sumxx )

    return beta

  def linear(x, alpha, beta):

    n = len(x)

    linear = []

    for i in range(len(x)):
      linear.append( ( alpha + beta * x[i] ) )

    return linear

  def rxy(R,linear):

    SS_res = np.sum(( R[1] - linear )**2 )

    SS_tot = np.sum( ( R[1] - np.mean(R[1]) )**2 )

    rxy=1-(SS_res/SS_tot)

    return abs(rxy)

  if len(k)<1 or len(temperature)<1:

    k=[]
    temperature=[]

    k=list(eval(input(f"\nEnter a list of reaction rates ( s^-1 ): ")))
    temperature=list(eval(input(f"\nEnter a list of temperatures ( K ): ")))


  print('\n')

  viridis = plt.colormaps['viridis'].resampled(len(temperature))

  font = {'family': 'serif',
          'color':  'teal',
          'weight': 'bold',
          'size': 20,

          }

  font1 = {'family': 'serif',
          'color':  'teal',
          'weight': 'bold',
          'size': 15,
          }

  font2 = {'family': 'serif',
        'color':  'teal',
        'weight': 'bold',
        'size': 8,
        }

  arrhenius=plt.figure(facecolor='paleturquoise')

  ax=plt.axes()

  lnk = [np.log(k[i]) for i in range(len(k))]

  invT = [1/(temperature[i]) for i in range(len(temperature))]

  R1=np.array([lnk,invT])


  b = beta(R1)
  a = alpha(R1,b)
  l = linear(lnk, a, b)
  rxy = rxy(R1,l)


  ax.set_facecolor('lightcyan')
  ax.set_alpha(0.1)
  ax.spines["top"].set_color("teal")
  ax.spines["bottom"].set_color("teal")
  ax.spines["left"].set_color("teal")
  ax.spines["right"].set_color("teal")
  ax.tick_params(axis='x', colors='teal',labelsize=10)
  ax.tick_params(axis='y', colors='teal',labelsize=10)
  ax.set_xlabel('',fontdict=font1)
  ax.set_ylabel('',fontdict=font1)

  legend_ncols=1
  n_labels=0

  plt.plot(l,lnk,label=f'R$^2$ = {round(rxy,2)*100} %\nSlope = {round(b,4)} \nIntercept = {round(a,4)} \nE$_a$ = {round(-b*R,5)} J/mol \nA = {round(np.exp(a),5)}')

  for i in range(len(lnk)):
    plt.plot(invT[i],lnk[i],'o',c=viridis(i,1))

  plt.legend(loc='center left',bbox_to_anchor=(1, 0,legend_ncols*(0.5),1.1), bbox_transform=None,mode="expand", borderpad=1, fontsize=9, title='Reactions',title_fontsize=12,facecolor='lightcyan',edgecolor='teal', shadow=True, fancybox=True,labelcolor='teal', framealpha=1,ncols=legend_ncols,columnspacing=1000)
  plt.grid(color='paleturquoise')
  plt.ylabel(f'ln(k)\n\n',fontdict=font1)
  plt.xlabel('\n1/Temperature ( $1/K$ )\n',fontdict=font1)
  plt.title('\nLogaritmic rate constant as a function of Temperature\n', fontdict=font,ha='center')
  plt.text((legend_ncols*0.5)+0.9,-0.3,f'©Chem.Mod', fontdict=font2, ha='center',verticalalignment='center', transform=ax.transAxes)

  return arrhenius



