

def content():
  '''
  \n Content is a function that returns a list of content in ChemMod.
  \n You can see all relevant directories and functions
  \n--------------------------------------------------------------------
  \n Example:
  \n\t content()
  \n\t --- Returns:

  \n\tcontent:
  \n\tequation:
  \n\t  - M
  \n\t  - element_data
  \n\t  - equilibrium
  \n\thelp:
  \n\t  - content_data
  \n\t  - info
  \n\tplot:
  \n\t  - arrhenius_plot
  \n\t  - bjerrum_plot
  \n\t  - gibbs_plot
  \n\t  - order_plot
  \n\t  - theme
  \n\t  - theme_data
  \n\t  - theme_list_for_formatting_of_plots 
  '''
  
  import ChemMod as chemM
  
  contents = dict()

  for i in dir(chemM):
    if i.startswith('_') == False and i != 'plt' and i != 'np':
      jliste = []
      for j in dir(eval(f'chemM.{i}')):
        
        if j.startswith('_') == False and j != 'plt' and j != 'np':
        
          jliste.append(f"""\t - {j}""")
      
      contents[f'{i}'] = jliste

  for k in contents:
    print(f'{k}:')
    for l in range(len(eval(f"""contents['{k}']"""))):
      print(eval(f"""contents['{k}'][{l}]"""))
  
  return



