#M - Find molar masses of different atoms and molecules by inputting a string

def M(molecule):
  '''M is a function that calculates the molarmass of a given atom or molecule.
        \n It contains the following information about the elements:
        ---------------------------------------------------
        \n\t Atomic number
        \n\t Molar mass
        \n\t Valency
        \n\t Name
        \n\t Electronegativity
        ---------------------------------------------------
        \n\n The data is structured as follows:
        \n\n     "H": {
        \n\t"AtomicNumber": 1,
        \n\t"MolarMass": 1.008,
        \n\t"Valency": 1,
        \n\t"Name": "Hydrogen",
        \n\t"Electronegativity": 2.20
        \n\t},
        ---------------------------------------------------
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
        \n\telement_data['He']['Electronegativity']'''
  
  from ChemMod.equation import element_data

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



