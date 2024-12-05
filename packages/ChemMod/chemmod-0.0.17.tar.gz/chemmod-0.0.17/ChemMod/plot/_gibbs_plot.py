

  
#gibbs_plot - Plot Gibbs energy as a function of temperature and calculate Gibbs energies from given temperature entries

def gibbs_plot(enthalpy=[],entropy=[],temperatures=[],initial_temperature=0,final_temperature=1000,names=['Reaction1','Reaction2','Reaction3','Reaction4','Reaction5','Reaction6','Reaction7']):

  import matplotlib.pyplot as plt
  import numpy as np
  from ChemMod.plot import theme_list_for_formatting_of_plots


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
          'color':  theme_list_for_formatting_of_plots[2],
          'weight': 'bold',
          'size': 20,

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

  gibbs=plt.figure(facecolor=theme_list_for_formatting_of_plots[7])
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
