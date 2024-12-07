# import all the necessary functions
import tellurium as te
import roadrunner
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.image as mpimg

def myosinCK(multiplier,selected_rate_constants, rate_multipliers):
  # This is the complete cardiac myosin function that produces wildtype and mutated graph outputs
  # The first part simulates the wildtype control
  # The following part of the code will then allow users to apply parameter changes that effect species concentration
  # The following part will then allow users to select any rate constant of the biochemcial process and alter it as well

  r = te.loada('''
      # Reactions
          J0: CB0 -> CB1; (k1 * CB0 + k20 * CB2 - (k10 + k2) * CB1);
          J1: CB1 -> CB2; (k2 * CB1 + k30 * CB3 - (k20 + k3) * CB2);
          J2: CB2 -> CB3; (k3 * CB2 + k40 * CB4 - (k30 + k4) * CB3);
          J3: CB3 -> CB4; (k4 * CB3 + k50 * CB5 - (k40 + k5) * CB4);
          J4: CB4 -> CB5; (k5 * CB4 + k60 * CB6 - (k50 + k6) * CB5);
          J5: CB5 -> CB6; (k6 * CB5 + k70 * CB0 - (k60 + k7) * CB6);
          J6: CB6 -> CB0; (k7 * CB6 + k10 * CB1 - (k70 + k1) * CB0);

      # Initial conditions
          CB0 = 0.478;
          CB1 = 0.0;
          CB2 = 0.014;
          CB3 = 0.143;
          CB4 = 0.0;
          CB5 = 0.144;
          CB6 = 0.221;

      # Rate Constant Parameters
          k1 = 40; k10 = 70;
          k2 = 140; k20 = 80;
          k3 = 150; k30 = 15;
          k4 = 20; k40 = 0.2;
          k5 = 10; k50 = 0.1;
          k6 = 25; k60 = 0.25;
          k7 = 200; k70 = 50;
      ''')

      # Simulate the model
  result = r.simulate(0, 0.3, 500)
  time = result[:, 0]

      # Extract CB species
  CB0 = result[:, 1]
  CB1 = result[:, 2]
  CB2 = result[:, 3]
  CB3 = result[:, 4]
  CB4 = result[:, 5]
  CB5 = result[:, 6]
  CB6 = result[:, 7]

  # Plot each species using Matplotlib w unique customized labels
  plt.figure(figsize=(9, 7))  # this may have to be altered depending on the kinetics if the legend gets in the way
  plt.xlabel('Time')
  plt.ylabel('% Concentration')
  plt.title('Product Dynamics of CrossBridge States')
  plt.xlim(0, 0.3)  # this MUST be modified when changing time constraints
  plt.grid(True)
  plt.plot(time, CB0, label='[MYOSIN + ATP / MYOSIN w ADP + Pi]', linestyle='-')
  plt.plot(time, CB1, label='[COCKED MYOSIN w ADP + Pi]', linestyle='--')
  plt.plot(time, CB2, label='[ACTOMYOSIN COMPLEX w ADP + Pi]', linestyle='-.')
  plt.plot(time, CB3, label='[PRE ACTOMYOSIN COMPLEX w ADP]', linestyle=':')
  plt.plot(time, CB4, label='[POST ACTOMYOSIN COMPLEX w ADP]', linestyle='-')
  plt.plot(time, CB5, label='[ISO ACTOMYOSIN COMPLEX w ADP]', linestyle='--')
  plt.plot(time, CB6, label='[ACTOMYOSIN COMPLEX]', linestyle='-.')
  plt.legend()
  plt.tight_layout()
  plt.show()
  

  # This code manipulates the intial conditions of CB0 and compensates the rest of the reactants accordingly. However, any reactant can be manipulated but you would just need to adjust the code accordingly to which reactant is being initally changed.
  # Initial conditions from WT cardiac CB cycling

  iCB0 = 0.478
  iCB1 = 0.0
  iCB2 = 0.014
  iCB3 = 0.143
  iCB4 = 0.0
  iCB5 = 0.144
  iCB6 = 0.221

  # Depending on how the mutation or drug therapy effects myosin avilibility, insert the multiplier here
  # multiplier = 1.67 because for my example R403Q activates 67.7% more myosion, CB0 increases by 67%
  # Below is the code to calculate how the changes in myosin concentration needs to be accounted for and scaled for the rest of the parameters.
  initial_total = iCB0 + iCB1 + iCB2 + iCB3 + iCB4 + iCB5 + iCB6
  new_CB0 = iCB0 * multiplier
  remaining = initial_total - new_CB0
  other_total = iCB1 + iCB2 + iCB3 + iCB4 + iCB5 + iCB6
  scaling_factor = remaining / other_total if other_total != 0 else 0

  new_CB1 = iCB1 * scaling_factor
  new_CB2 = iCB2 * scaling_factor
  new_CB3 = iCB3 * scaling_factor
  new_CB4 = iCB4 * scaling_factor
  new_CB5 = iCB5 * scaling_factor
  new_CB6 = iCB6 * scaling_factor

  # After the scaling factor calculations, now users can simulate this reaction with adjusted concentrations

  r = te.loada(f'''
  # Reactions
      J0: NewCB0 -> NewCB1; (k1 * NewCB0 + k20 * NewCB2 - (k10 + k2) * NewCB1);
      J1: NewCB1 -> NewCB2; (k2 * NewCB1 + k30 * NewCB3 - (k20 + k3) * NewCB2);
      J2: NewCB2 -> NewCB3; (k3 * NewCB2 + k40 * NewCB4 - (k30 + k4) * NewCB3);
      J3: NewCB3 -> NewCB4; (k4 * NewCB3 + k50 * NewCB5 - (k40 + k5) * NewCB4);
      J4: NewCB4 -> NewCB5; (k5 * NewCB4 + k60 * NewCB6 - (k50 + k6) * NewCB5);
      J5: NewCB5 -> NewCB6; (k6 * NewCB5 + k70 * NewCB0 - (k60 + k7) * NewCB6);
      J6: NewCB6 -> NewCB0; (k7 * NewCB6 + k10 * NewCB1 - (k70 + k1) * NewCB0);

  # Adjusted Initial Conditions
      NewCB0 = {new_CB0};
      NewCB1 = {new_CB1};
      NewCB2 = {new_CB2};
      NewCB3 = {new_CB3};
      NewCB4 = {new_CB4};
      NewCB5 = {new_CB5};
      NewCB6 = {new_CB6};

  # Rate Constant Parameters
      k1 = 40; k10 = 70;
      k2 = 140; k20 = 80;
      k3 = 150; k30 = 15;
      k4 = 20; k40 = 0.2;
      k5 = 10; k50 = 0.1;
      k6 = 25; k60 = 0.25;
      k7 = 200; k70 = 50;
  ''')

  # Simulate the model
  result = r.simulate(0, 0.3, 500)
  time = result[:, 0]

  # Extract CB species
  NewCB0 = result[:, 1]
  NewCB1 = result[:, 2]
  NewCB2 = result[:, 3]
  NewCB3 = result[:, 4]
  NewCB4 = result[:, 5]
  NewCB5 = result[:, 6]
  NewCB6 = result[:, 7]

  # Plot species altering kinetics (for my case R403Q)
  plt.figure(figsize=(9, 7)) 
  plt.xlabel('Time')
  plt.ylabel('% Concentration')
  plt.title('Product Dynamics of CrossBridge States with R403Q mutated species concentrations')
  plt.xlim(0, 0.3) 
  plt.grid(True)
  plt.plot(time, NewCB0, label='[MYOSIN + ATP / MYOSIN w ADP + Pi]', linestyle='-')
  plt.plot(time, NewCB1, label='[COCKED MYOSIN w ADP + Pi]', linestyle='--')
  plt.plot(time, NewCB2, label='[ACTOMYOSIN COMPLEX w ADP + Pi]', linestyle='-.')
  plt.plot(time, NewCB3, label='[PRE ACTOMYOSIN COMPLEX w ADP]', linestyle=':')
  plt.plot(time, NewCB4, label='[POST ACTOMYOSIN COMPLEX w ADP]', linestyle='-')
  plt.plot(time, NewCB5, label='[ISO ACTOMYOSIN COMPLEX w ADP]', linestyle='--')
  plt.plot(time, NewCB6, label='[ACTOMYOSIN COMPLEX]', linestyle='-.')
  plt.legend()
  plt.tight_layout()
  plt.show()
   

  # This part of the code accounts for pertubajens that effect rate constants
  rate_constants = {
      "ik1": 40, "ik10": 70,
      "ik2": 140, "ik20": 80,
      "ik3": 150, "ik30": 15,
      "ik4": 20, "ik40": 0.2,
      "ik5": 10, "ik50": 0.1,
      "ik6": 25, "ik60": 0.25,
      "ik7": 200, "ik70": 50
  }

  # This for loop iterates through the dictionary and see if there is a multiplier that needs to be applied
  # Then prints out the updated rates and manually puts it into tellerium simulation 

  for rate_constant, rate_multipliers in zip(selected_rate_constants, rate_multipliers):
      if rate_constant in rate_constants:
          rate_constants[rate_constant] *= rate_multipliers
          print(f"Updated {rate_constant}: {rate_constants[rate_constant]}")

  r = te.loada(f'''
  # Reactions
      J0: NewerCB0 -> NewerCB1; (ik1 * NewerCB0 + ik20 * NewerCB2 - (ik10 + ik2) * NewerCB1);
      J1: NewerCB1 -> NewerCB2; (ik2 * NewerCB1 + ik30 * NewerCB3 - (ik20 + ik3) * NewerCB2);
      J2: NewerCB2 -> NewerCB3; (ik3 * NewerCB2 + ik40 * NewerCB4 - (ik30 + ik4) * NewerCB3);
      J3: NewerCB3 -> NewerCB4; (ik4 * NewerCB3 + ik50 * NewerCB5 - (ik40 + ik5) * NewerCB4);
      J4: NewerCB4 -> NewerCB5; (ik5 * NewerCB4 + ik60 * NewerCB6 - (ik50 + ik6) * NewerCB5);
      J5: NewerCB5 -> NewerCB6; (ik6 * NewerCB5 + ik70 * NewerCB0 - (ik60 + ik7) * NewerCB6);
      J6: NewerCB6 -> NewerCB0; (ik7 * NewerCB6 + ik10 * NewerCB1 - (ik70 + ik1) * NewerCB0);

  # Initial conditions
      NewerCB0 = 0.478;
      NewerCB1 = 0.0;
      NewerCB2 = 0.014;
      NewerCB3 = 0.143;
      NewerCB4 = 0.0;
      NewerCB5 = 0.144;
      NewerCB6 = 0.221;

  # Rate Constant Parameters
      ik1 = {rate_constants["ik1"]}; ik10 = {rate_constants["ik10"]};
      ik2 = {rate_constants["ik2"]}; ik20 = {rate_constants["ik20"]};
      ik3 = {rate_constants["ik3"]}; ik30 = {rate_constants["ik30"]};
      ik4 = {rate_constants["ik4"]}; ik40 = {rate_constants["ik40"]};
      ik5 = {rate_constants["ik5"]}; ik50 = {rate_constants["ik50"]};
      ik6 = {rate_constants["ik6"]}; ik60 = {rate_constants["ik60"]};
      ik7 = {rate_constants["ik7"]}; ik70 = {rate_constants["ik70"]};
  '''
  )

  # Simulate the model
  result = r.simulate(0, 0.3, 500)
  time = result[:, 0]

  # Extract CB species
  NewerCB0 = result[:, 1]
  NewerCB1 = result[:, 2]
  NewerCB2 = result[:, 3]
  NewerCB3 = result[:, 4]
  NewerCB4 = result[:, 5]
  NewerCB5 = result[:, 6]
  NewerCB6 = result[:, 7]


  # Plot rate altering kinetics (in my case S532P)
  plt.figure(figsize=(9, 7))
  plt.xlabel('Time')
  plt.ylabel('% Concentration')
  plt.title('Product Dynamics of CrossBridge States with S532P Mutated Rate Constants')
  plt.xlim(0, 0.3)
  plt.grid(True)
  plt.plot(time, NewerCB0, label='[MYOSIN + ATP / MYOSIN w ADP + Pi]', linestyle='-')
  plt.plot(time, NewerCB1, label='[COCKED MYOSIN w ADP + Pi]', linestyle='--')
  plt.plot(time, NewerCB2, label='[ACTOMYOSIN COMPLEX w ADP + Pi]', linestyle='-.')
  plt.plot(time, NewerCB3, label='[PRE ACTOMYOSIN COMPLEX w ADP]', linestyle=':')
  plt.plot(time, NewerCB4, label='[POST ACTOMYOSIN COMPLEX w ADP]', linestyle='-')
  plt.plot(time, NewerCB5, label='[ISO ACTOMYOSIN COMPLEX w ADP]', linestyle='--')
  plt.plot(time, NewerCB6, label='[ACTOMYOSIN COMPLEX]', linestyle='-.')
  plt.legend()
  plt.tight_layout()
  plt.show()
  

  return {
        "time": time,
        "CB0": CB0, "CB1": CB1, "CB2": CB2, "CB3": CB3, "CB4": CB4, "CB5": CB5, "CB6": CB6,
        "NewCB0": NewCB0, "NewCB1": NewCB1, "NewCB2": NewCB2, "NewCB3": NewCB3, "NewCB4": NewCB4, "NewCB5": NewCB5, "NewCB6": NewCB6,
        "NewerCB0": NewerCB0, "NewerCB1": NewerCB1, "NewerCB2": NewerCB2, "NewerCB3": NewerCB3, "NewerCB4": NewerCB4, "NewerCB5": NewerCB5, "NewerCB6": NewerCB6,
        }


# example of how to run it and also set up for plot comparison and percent change
#results = myosinCK(1.67,["ik2"], [.4])
#time = results["time"] 
#CB0 = results["CB0"] 
#CB1 = results["CB1"]
#CB2 = results["CB2"]
#CB3 = results["CB3"]
#CB4 = results["CB4"]
#CB5 = results["CB5"]
#CB6 = results["CB6"]
#NewCB0 = results["NewCB0"]
#NewCB1 = results["NewCB1"]
#NewCB2 = results["NewCB2"]
#NewCB3 = results["NewCB3"]
#NewCB4 = results["NewCB4"]
#NewCB5 = results["NewCB5"]
#NewCB6 = results["NewCB6"]
#NewerCB0 = results["NewerCB0"]
#NewerCB1 = results["NewerCB1"]
#NewerCB2 = results["NewerCB2"]
#NewerCB3 = results["NewerCB3"]   
#NewerCB4 = results["NewerCB4"]
#NewerCB5 = results["NewerCB5"]
#NewerCB6 = results["NewerCB6"]
