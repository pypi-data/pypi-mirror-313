

#arrhenius_plot - Calculate activation energy for reaction by linear reaction of rate constant and temperature.
from ChemMod import plot

def arrhenius_plot(k=[],temperature=[],R=8.314,names=['Reaction1','Reaction2','Reaction3','Reaction4','Reaction5','Reaction6','Reaction7']):
  import numpy as np
  import matplotlib.pyplot as plt
  from ChemMod.plot import theme
  from ChemMod.plot import theme_list_for_formatting_of_plots


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

  viridis = plt.colormaps[theme_list_for_formatting_of_plots[4]].resampled(len(temperature))

  font = {'family': 'serif',
          'color': theme_list_for_formatting_of_plots[2],
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

  arrhenius=plt.figure(facecolor = theme_list_for_formatting_of_plots[7])

  ax=plt.axes()

  lnk = [np.log(k[i]) for i in range(len(k))]

  invT = [1/(temperature[i]) for i in range(len(temperature))]

  R1=np.array([lnk,invT])


  b = beta(R1)
  a = alpha(R1,b)
  l = linear(lnk, a, b)
  rxy = rxy(R1,l)


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

  plt.plot(l,lnk,label=f'R$^2$ = {round(rxy,2)*100} %\nSlope = {round(np.exp(b),4)} \nIntercept = {round(np.exp(a),4)} \nE$_a$ = {round(-b*R,5)} J/mol \nA = {round(np.exp(a),5)}',color = theme_list_for_formatting_of_plots[3])

  for i in range(len(lnk)):
    plt.plot(invT[i],lnk[i],'o',mec=theme_list_for_formatting_of_plots[5],c=viridis(i,1))

  plt.legend(loc='center left',bbox_to_anchor=(1, 0,legend_ncols*(0.5),1.1), bbox_transform=None,mode="expand", borderpad=1, fontsize=9,title_fontsize=12,facecolor=theme_list_for_formatting_of_plots[8],edgecolor=theme_list_for_formatting_of_plots[0], shadow=True, fancybox=True,labelcolor=theme_list_for_formatting_of_plots[6], framealpha=1,ncols=legend_ncols,columnspacing=1000)
  plt.grid(color=theme_list_for_formatting_of_plots[9])
  plt.ylabel(f'ln(k)\n\n',fontdict=font1)
  plt.xlabel('\n1/Temperature ( $1/K$ )',fontdict=font1)
  plt.title('\nLogaritmic rate constant as a function of Temperature\n', fontdict=font,ha='center')
  plt.text((legend_ncols*0.5)+0.9,-0.3,f'©Chem.Mod', fontdict=font2, ha='center',verticalalignment='center', transform=ax.transAxes)
  plt.show()
  return arrhenius
