
  
#equilibrium - Calculate molar masses for reactants and products, creating equilibrium fraction and more to come....

def equilibrium(reaction=None,K=None,crea=[],cpro=[],R=8.314,T=25):
  '''\nEquilibrium is a function that calculates the equilibrium constant of a chemical reaction. 
      \nIt takes a reaction written as a string.
      \nFor instance PbCl2 (s) = Pb (aq)+ 2 Cl(aq).
      \nIt outputs the following information about the reaction:\n
  -------------------------------------------------------------------
      \n\t Equilibrium reaction
      \n\t Equilibrium fraction
      \n\t Equilibrium constant
      \n\t Molarmasses
      \n\t Concentrations
      \n\t Gibbs free energy
  -------------------------------------------------------------------
      \n The input is structured as follows:
      \n\nequilibrium(reaction=None,K=None,crea=[],cpro=[],R=8.314,T=25)
      \n\nThe reaction (reaction):
      \n\n\tPbCl2 (s) = Pb (aq)+ 2 Cl(aq)
      \n\n\tWrite everything as you normally would when calculating equilibria. 
      \n\n\tThe harpunes should be written as '=' and phases (liquid,solid etc.): (l), (s), (g) and (aq).
      \n\nThe equilibrium constant (K):
      \n\n\tIs optional, if you have K write the value of K here.
      \n\nThe concentrations of reactants (crea):
      \n\n\tIs optional, a list of the concentrations of the reactants.
      \n\nThe concentrations of products (cpro):
      \n\n\tIs optional, a list of the concentrations of the products.
      \n\nThe gas constant (R):
      \n\n\tIs optional, it has default value 8.314
      \n\nThe temperature (T):
      \n\n\tIs optional, it has default value 298 K or 25 degrees Celsius\n
  -------------------------------------------------------------------
      \n\nHow to use example:
      \n\tequilibrium(reaction,K,crea,cpro,R,T)
      \n\tequilibrium('PbCl2(s) =Pb (aq)+ 2 Cl(aq)', 1.00*10**4 ,[],[],8.314,100)
      \n\n\tReaction: 'PbCl2(s) =Pb (aq)+ 2 Cl(aq)' (Is a string)
      \n\n\tK:  1.00*10**4
      \n\n\tcrea: [] (are left empty, because we don't have the information)
      \n\n\tcpro: [] (are also left empty like above)
      \n\n\tR: 8.314
      \n\n\tT: 100 (in Celsius the function automatically converts to Kelvin)
      \n\t
      \n\tThe results are:
      \n\tPbCl2(s) ⇋Pb (aq)+ 2 Cl(aq)
      \n\tKsp = [Pb]⋅[Cl]^2 
      \n\tMolarmasses for reactants:
      \n\tPbCl2:	278.106 g/mol
      \n\tMolarmasses for products:
      \n\tPb:	207.2 g/mol
      \n\tCl:	70.906 g/mol
      \n\tConcentrations for products:
      \n\t34.19951893353393 M
      \n\tGibbs free energy:
      \n\t-28.562389155023524 kJ/mol
  '''
 
  restart=str(input('If you wish to restart equil enter r else enter any other symbol: ' ))

  if restart == 'r' or restart == 'R':
    crea=[]
    cpro=[]
    reaction=None
    K=None


  Ksp=None
  T+=273

  if reaction == None:
    reaction=str(input('Write the fancy equilibrium reaction: '))

  import numpy as np
  import copy
  import math as ma
  from ChemMod.equation import element_data
  from ChemMod.equation import M

  if type(reaction)!=str:
    raise TypeError(type(reaction),reaction,"STOP wtf I want a f*cking string with af reaction dumb ass")
  else:

    #Creating beautiful equilibrium reaction

    reaction1=copy.copy(reaction)
    reaction1=reaction1.replace('=','\u21CB')
    reaction1=reaction1.split()
    reaction1=" ".join(str(i) for i in reaction1)

    #Converting input to computable data

    fases=['(s)','(l)','(g)','(aq)']

    rea=copy.copy(reaction)

    for i in range(len(fases)):
      rea=rea.replace(fases[i],'')

    split_eq=rea.split('=')

    split_eq1=reaction.split('=')

    def phase(part):
        """Parse the molecules from a part of the reaction"""
        molecules = part.split('+')
        parsed_molecules = {}
        phases = []
        atoms = {}

        for molecule_part in molecules:
            # Extract phase and remove it from the molecule part
            phase = None
            for possible_phase in ['(s)', '(l)', '(g)', '(aq)']:
                if possible_phase in molecule_part:
                    phase = possible_phase.strip('()')
                    molecule_part = molecule_part.replace(possible_phase, '')
                    break

            phases.append(f"({phase})")

        return phases


    def reactionsplit(rea):
      ''' Splitting the reaction, returns list with reaction elements (either products or reactants)
      '''
      a=rea.replace(' ','+')
      b=a.split('+')
      c=[b[i] for i in range(len(b)) if len(b[i])!=0]
      return c

    reactants, products = reactionsplit(split_eq[0]),reactionsplit(split_eq[1])

    def reactionparts(pros):

      pro1=[]
      pro2=[]

      count_pro2=0

      for i in range(len(pros)):
        try:
          pro1.append(int(pros[i]))
          count_pro2+=1
        except ValueError:
          if count_pro2==0:
            pro1.append(int(1))
          pro2.append(pros[i])
          count_pro2=0

      return pro2, pro1

    reaction_phases={}

    reaction_phases['reactants'], reaction_phases['products'] = phase(split_eq1[0]), phase(split_eq1[1])

    reaction_molecules={}
    reaction_n_molecules={}

    reaction_molecules['reactants'], reaction_n_molecules['reactants'], reaction_molecules['products'], reaction_n_molecules['products'] = reactionparts(reactants) + reactionparts(products)

    if len(crea) == 0:
      answer=str(input('\nDo you have the concentrations of the reactants (yes/no): '))
      if answer == 'yes' or answer == 'Yes' or answer == 'YES' or answer == 'yess' or answer == 'Yess':
        for i in range(len(reaction_molecules['reactants'])):
          crea.append(float(eval(input(f"\nEnter concentration of {reaction_molecules['reactants'][i]}: "))))

    if len(cpro) == 0:
      answer=str(input('\nDo you have the concentrations of the products (yes/no): '))
      if answer == 'yes' or answer == 'Yes' or answer == 'YES' or answer == 'yess' or answer == 'Yess':
        for i in range(len(reaction_molecules['products'])):
          cpro.append(float(eval(input(f"\nEnter concentration of {reaction_molecules['products'][i]}: "))))

    def formatmolecules(a):

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



    #Saving elements in the reaction compounds for further calculation.

    reaction_atoms={}

    rea_atoms_rea_list=[]
    rea_atoms_pro_list=[]

    for z in range(len(reaction_molecules['reactants'])):
      rea_atoms_rea_list.append(formatmolecules(reaction_molecules['reactants'][z]))

    reaction_atoms['reactants']=rea_atoms_rea_list

    for z1 in range(len(reaction_molecules['products'])):
      rea_atoms_pro_list.append(formatmolecules(reaction_molecules['products'][z1]))

    reaction_atoms['products']=rea_atoms_pro_list



    #Creating K equilibrium fraction

    K_reactants=[ f"[{reaction_molecules['reactants'][i]}]" for i in range(len(reaction_molecules['reactants'])) if reaction_phases['reactants'][i]=='(aq)' or reaction_phases['reactants'][i]=='(None)']
    K_products= [ f"[{reaction_molecules['products'][i]}]" for i in range(len(reaction_molecules['products'])) if reaction_phases['products'][i]=='(aq)' or reaction_phases['products'][i]=='(None)']

    if len(K_reactants)>0:
      for i in range(len(K_reactants)):
        if reaction_n_molecules['reactants'][i]>1:
          K_reactants[i]=f"{K_reactants[i]}^{reaction_n_molecules['reactants'][i]} "

    if len(K_products)>0:
      for i in range(len(K_products)):
        if reaction_n_molecules['products'][i]>1:
          K_products[i]=f"{K_products[i]}^{reaction_n_molecules['products'][i]} "


    K_reactants="\u22C5".join(str(i) for i in K_reactants)
    K_products="\u22C5".join(str(i) for i in K_products)

    if len(K_reactants) > 0 and len(K_products) > 0:
      equilibrium = f"K = ( {K_products} ) / ( {K_reactants} )"

    elif len(K_reactants) == 0 and len(K_products) > 1:
      equilibrium = f"Ksp = {K_products}"
      Ksp = K

    elif len(K_reactants) > 1 and len(K_products) == 0:
      equilibrium = f"Ksp = {K_reactants}"
      Ksp = K

    elif len(K_reactants) == 0 and len(K_products) == 0:
      equilibrium = "This function only calculates equilibrium in solutions you sick MF"


    #Calculating K

    if len(crea)==0:
      crea=[]
      for i in range(len(reaction_molecules['reactants'])):
        crea.append(None)

    if len(cpro)==0:
      cpro=[]
      for i in range(len(reaction_molecules['products'])):
        cpro.append(None)

    reaction_concentrations={}

    reaction_concentrations['reactants'], reaction_concentrations['products'] = crea, cpro

    conc_rea=[ f"{reaction_concentrations['reactants'][i]}" for i in range(len(reaction_molecules['reactants'])) if reaction_phases['reactants'][i]=='(aq)' or reaction_phases['reactants'][i]=='(None)']
    conc_pro= [ f"{reaction_concentrations['products'][i]}" for i in range(len(reaction_molecules['products'])) if reaction_phases['products'][i]=='(aq)' or reaction_phases['products'][i]=='(None)']

    if len(conc_rea)>0:
      for i in range(len(conc_rea)):
        if reaction_n_molecules['reactants'][i]>1:
          conc_rea[i]=f"({conc_rea[i]}**{reaction_n_molecules['reactants'][i]}) "

    if len(conc_pro)>0:
      for i in range(len(conc_pro)):
        if reaction_n_molecules['products'][i]>1:
          conc_pro[i]=f"({conc_pro[i]}**{reaction_n_molecules['products'][i]}) "


    conc_rea="*".join(str(i) for i in conc_rea)
    conc_pro="*".join(str(i) for i in conc_pro)

    if K == None or K == 0 and len(conc_rea) > 0 and len(conc_pro) > 0:
      concentrations = f"( {conc_pro} ) / ( {conc_rea} )"
      try:
        K = eval(concentrations)
      except TypeError:
        K = 0

    elif len(conc_rea) == 0 and len(conc_pro) > 1:
      concentrations = f"{conc_pro}"
      try:
        Ksp = eval(concentrations)
      except TypeError:
        Ksp = K

    elif len(conc_rea) > 1 and len(conc_pro) == 0:
      concentrations = f"{conc_rea}"
      try:
        Ksp = eval(concentrations)
      except TypeError:
        Ksp = K

    elif len(conc_rea) == 0 and len(conc_pro) == 0:
      concentrations = "This function only calculates K in solutions you sick MF"

    if K != None:
      equil_KorKsp=f"K = {K}"

    if Ksp != None:
      equil_KorKsp=f"Ksp = {Ksp}"

    if Ksp == None and K == None:
      equil_KorKsp=f" "

    #Calculating Gibbs energi for the reaction

    gibbs = 0

    if K != None and K != 0:
      gibbs = - R * T * np.log(K)

    if Ksp != None and Ksp != 0:
      gibbs = - R * T * np.log(Ksp)


    #Calculating concentration

    if K != None:
      s_c_pro=0


    if Ksp != None:

      factor=[]

      for i in range(len(reaction_n_molecules['products'])):
        factor.append(reaction_n_molecules['products'][i]**reaction_n_molecules['products'][i])

      factor="*".join(str(i) for i in factor)
      exponent="+".join(str(i) for i in reaction_n_molecules['products'])

      s_c_pro_string=f"({Ksp}/{factor})**(1/({exponent}))"
      s_c_pro=eval(s_c_pro_string)


    if Ksp == None and K == None:
      s_c_pro=f" "

    #Calculating Molarmasses for the reaction

    molarmasses={}
    molarmass_rea_list=[]
    molarmass_pro_list=[]

    for z3 in range(len(reaction_atoms['reactants'])):
      molarmass_rea_list.append(M(reaction_atoms['reactants'][z3]))

    molarmasses['reactants']=molarmass_rea_list

    for z4 in range(len(reaction_atoms['products'])):
      molarmass_pro_list.append(M(reaction_atoms['products'][z4]))

    molarmasses['products']=molarmass_pro_list

    molarmass_rea_list_format=[]

    for z5 in range(len(molarmasses['reactants'])):
      molarmass_rea_list_format.append(f"{reaction_molecules['reactants'][z5]}:\t{round(molarmasses['reactants'][z5]*reaction_n_molecules['reactants'][z5],3)} g/mol")

    rea_M="\n\t\t".join(str(i) for i in molarmass_rea_list_format)

    molarmass_pro_list_format=[]

    for z6 in range(len(molarmasses['products'])):
      molarmass_pro_list_format.append(f"{reaction_molecules['products'][z6]}:\t{round(molarmasses['products'][z6]*reaction_n_molecules['products'][z6],3)} g/mol")

    pro_M="\n\t\t".join(str(i) for i in molarmass_pro_list_format)

    #Emptying lists

    #Output formatting

    Result=print(f"""\n\n
                 \n\n\tResults:
                 \n\n\t\t{reaction1.strip()}
                 \n\n\tEquilibrium:
                 \n\n\t\t{equilibrium}
                 \n\n\tEquilibrium constant:
                 \n\t\t{equil_KorKsp}
                 \n\n\tMolarmasses:
                 \n\n\t\tReactants:
                {rea_M}
                 \n\n\t\tProducts:
                {pro_M}
                 \n\n\tConcentrations:
                 \n\n\t\tProducts:
                {s_c_pro} M
                \n\n\tGibbs free energy:
                 \n\n\t\t{gibbs/1000} kJ/mol
                 \n\n\n\n\n\n\n\n{reaction_molecules} \n\n {reaction_n_molecules}  \n\n {reaction_atoms} \n\n {reaction_phases} \n\n """)

    return Result

