# New function for 3 graphs
def plot_overlay_three(a,b,c,d,x,y,z,e,f,g):
  plt.figure(figsize=(9, 7)) #this may have to be altered depending on the kinetics if the legend gets in the way
  plt.xlabel('Time')
  plt.ylabel('% Concentration')
  plt.title('Product Dynamics of CrossBridge States')
  plt.xlim(0, 0.3) #this MUST be modified when changing time constraints
  plt.grid(True)
  plt.plot(a, b, label= c, linestyle=d)
  plt.plot(a, x, label= y, linestyle=z)
  plt.plot(a, e, label=f, linestyle=g)
  plt.legend()
  plt.tight_layout()
  return
  
# ex of how to run function
#plot_overlay_three(time, CB1, '[COCKED MYOSIN w ADP + Pi]', '--', NewCB1, '[PRE ACTOMYOSIN COMPlEX w ADP] w R403Q', ':', NewerCB1, '[COCKED MYOSIN w ADP + Pi] w S532P', '-.')
