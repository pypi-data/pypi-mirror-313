from setuptools import setup, find_packages

setup(
   name='neuron_simulator',
   version='1.0',
   description='a visualization tool for neuron spiking graph',
   author='Sophia Shan',
   author_email='shanyufei2001@gmail.com',
   python_requires= ">3.11.6",
   packages= find_packages(['neuron', 'pygame-ce', 'pygame_gui', 'pygame_chart']), 
   
     #same as name
   # install_requires=['wheel', 'bar', 'greek'], #external packages as dependencies
)