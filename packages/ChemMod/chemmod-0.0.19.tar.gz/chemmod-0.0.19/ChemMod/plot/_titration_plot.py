 
def titration_plot(pKa=[],optimalpH=7,pHvalues=[],Ka=[],acidname=['...','...','...','...','...','...','...','(: No names?']):

  import matplotlib.pyplot as plt
  import numpy as np
  from ChemMod.equation import element_data
  from ChemMod.equation import M
  from ChemMod.plot import theme_list_for_formatting_of_plots


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
          'color':  theme_list_for_formatting_of_plots[2],
          'weight': 'bold',
          'size': 20,
          #'backgroundcolor':'lightblue'
          }

  font1 = {'family': 'serif',
          'color':  theme_list_for_formatting_of_plots[2],
          'weight': 'bold',
          'size': 15,
          }

  font2 = {'family': 'serif',
        'color':  theme_list_for_formatting_of_plots[2],
        'weight': 'bold',
        'size': 8,
        }

  bjerrum=plt.figure(facecolor=theme_list_for_formatting_of_plots[7])
  ax=plt.axes()


  ax.set_facecolor(theme_list_for_formatting_of_plots[8])
  ax.set_alpha(0.1)
  ax.spines["top"].set_color(theme_list_for_formatting_of_plots[0])
  ax.spines["bottom"].set_color(theme_list_for_formatting_of_plots[0])
  ax.spines["left"].set_color(theme_list_for_formatting_of_plots[0])
  ax.spines["right"].set_color(theme_list_for_formatting_of_plots[0])
  ax.spines["top"].set_linewidth(theme_list_for_formatting_of_plots[1])
  ax.spines["bottom"].set_linewidth(theme_list_for_formatting_of_plots[1])
  ax.spines["left"].set_linewidth(theme_list_for_formatting_of_plots[1])
  ax.spines["right"].set_linewidth(theme_list_for_formatting_of_plots[1])
  ax.tick_params(axis='x', colors=theme_list_for_formatting_of_plots[0],labelsize=10)
  ax.tick_params(axis='y', colors=theme_list_for_formatting_of_plots[0],labelsize=10)
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