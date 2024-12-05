
  #order_plot - Raction Kinetics. Find the order of the reaction by linear regression.

def order_plot(c=[],time=[],names=['Reaction1','Reaction2','Reaction3','Reaction4','Reaction5','Reaction6','Reaction7']):

  import matplotlib.pyplot as plt
  import numpy as np
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


  if len(c)<1:
    c=[]
    names=[]
    time=[]

    c=list(eval(input(f"\nEnter a list of concentrations ( M ): ")))
    time=list(eval(input(f"\nEnter a list of timesteps ( s ): ")))
    names.append(str(input("Enter name of reaction: ")))

  print('\n')



  font = {'family': 'serif',
          'color':  theme_list_for_formatting_of_plots[2],
          'weight': 'bold',
          'size': 20,

          }

  font1 = {'family': 'serif',
          'color':  theme_list_for_formatting_of_plots[2],
          'weight': 'bold',
          'size': 14,
          }

  font2 = {'family': 'serif',
        'color':  theme_list_for_formatting_of_plots[2],
        'weight': 'bold',
        'size': 8,
        }

  order=plt.figure(facecolor=theme_list_for_formatting_of_plots[7],figsize=(8,12))

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
  