from setuptools import setup, find_packages

setup(
   name='neuron_simulator',
   version='2.1.2',
   description='a visualization tool for neuron spiking graph',
   author='Sophia Shan',
   author_email='shanyufei2001@gmail.com',
   python_requires= ">3.11.6",
   include_package_data = True, 
   package_data = {"neuron_simulator": ['theme.json']},
   packages= find_packages(['neuron', 'pygame-ce', 'pygame_gui', 'pygame_chart']), 
   dependencies = [
    "neuron == 8.2.6"
  ]
   
     #same as name
   # install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
)