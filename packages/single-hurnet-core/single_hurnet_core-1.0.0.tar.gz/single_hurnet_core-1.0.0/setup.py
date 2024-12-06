from setuptools import setup, find_packages
from setuptools.command.install import install
from os import path, remove, environ
from sys import modules
from py_compile import compile
from shutil import rmtree
package_name = 'single_hurnet_core'
version = '1.0.0'
setup(
    name=package_name,
    version=version,
    author='SAPIENS TECHNOLOGY',
    packages=find_packages(),
    install_requires=['numpy'],
    description = 'Example of construction of an Artificial Neural Network with the single-layer HurNet architecture for two-dimensional numerical matrices.',
    long_description = "This code is an algorithm designed, architected and developed by Sapiens Technology®️ and aims to build a simple Artificial Neural Network without hidden layers and with tabular data arranged in two-dimensional numerical matrices at the input and output. This is just a simplified example of the complete HurNet Neural Network architecture (created by Ben-Hur Varriano) that can be used and distributed in a compiled form by Sapiens Technology®️ members in seminars and presentations. HurNet Neural Networks use a peculiar architecture that eliminates the need for backpropagation in weights adjustment, making network training faster and more effective. In this example, we do not provide the network configuration structure for hidden layers and we reduce the dimensionality of the data to prevent potential market competitors from using our own technology against us. Although it is a simplified version of the HurNet network, it is still capable of assimilating simple patterns and some complex patterns that a conventional Multilayer Neural Network would not be able to abstract.",
    url='https://github.com/sapiens-technology/SingleLayerHurNet',
    license='Proprietary Software'
)
