class pxrd:
  def __init__(self,liste):
    self.liste = liste

  def peaks(self,factor):
    import numpy as np  
    peaks=[]

    liste = self.liste

    if int(len(liste)/factor) % 2 == 0:
      steps=int(len(liste)/factor)+1
    else:
      steps=int(len(liste)/factor)



    for i in range(steps+1,len(liste)-1):
      dataset=[]
      for j in range(steps):

        dataset.append(liste[(i-steps)+j])

      if dataset[int(steps/2)+1] == max(dataset) and 2+np.mean(dataset) < max(dataset):
        peaks.append((dataset[int(steps/2)+1],(i-steps)+(int(steps/2)+1)))

    return peaks


  def beta(peakx,peak,intensity,theta):
    import numpy as np

    intensity=[intensity[i]-150 for i in range(len(intensity))]

    count=0
    init_slut=0

    slut=[]
    start=[]

    limit=int(peak/40)

    for i in range(len(intensity)):
      if theta[i] > peakx-2 and theta[i] < peakx+2 and intensity[i] < (peak/2)+limit and intensity[i] > (peak/2)-limit:
        if init_slut!=0 or count!=0 and count+5<i:
          slut.append(theta[i])
          init_slut=1
        else:
          start.append(theta[i])
          count=i


    return np.mean(slut)-np.mean(start)

  def scherrer(beta,theta,lambdA = 1.5406, K = 0.9):
    
    import numpy as np
    
    t = ( K * lambdA ) / ( np.radians(beta) * np.cos( np.radians((theta)/2)) )

    tnm=t/10

    return tnm
