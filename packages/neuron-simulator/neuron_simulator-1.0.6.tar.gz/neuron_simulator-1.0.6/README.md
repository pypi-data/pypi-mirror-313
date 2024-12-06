# neuron_simulator

The aim of this project is to make a non-python user friendly interface for the python package 'neuron'. 
The user will be able to test different parameters of a neuron, including axon length, ion channels, and stimulation amplitude etc., and see the resulting membrane potential change 
produced by the simulation. This interface provides a interactive learning tool for users with little or no coding experience. 
This project contains the following files:

'main.py'
- Contains the main code. The main function 'run_simulation(cell_type)' will run the simulation for a neuron. There are two cell types you can choose: 
'soma': simulate just a soma
'dend_soma': simulate a dendrite and a soma 

'neuron_class.py': defines the class 'SOMA' which simulate just a soma, and 'DEND_SOMA' which simulate a dentrite and a soma


'setup.py;
- The file that contains the setup information for using this package 

'requirements.txt'
- text file that includes the specifications for package versions 

'theme.json'
- file that controls the text themes in the interface