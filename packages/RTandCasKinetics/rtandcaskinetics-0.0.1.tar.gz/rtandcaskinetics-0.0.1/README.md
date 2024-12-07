# RTandCasKinetics
This is a tool that is used for creating a plot that investigates the combined kinetics of HIV reverse transcriptase

## Users
Users do not need to be familiar with python to use this program. The users will use the Graphical User Interface (GUI) to input variables reducing the need to be familiar with python

## Installation
* To install, first install `pdm`, and make sure it's accessible in your $PATH.
* You can install it by going to 'https://pdm-project.org/en/latest/' and following their instructions to download PDM.
Prepare the local python environment by running `pdm install` and follow the instructions provided

## Getting Started
* To access the package, go to your terminal and type `pip install RTandCasKinetics`
* If you cannot find the root directory, enter the following code: `find ~/ -name "RTandCasKinetics"`. It will give many things, but the last will show the root.
* To go to the root directory type in the results from the search and type `cd directory`
* To run this, go to the root directory `RTandCasKinetics/` and run the command `pdm run src/rtandcaskinetics/casmodel.py`
* Adding information

## Contributing
To add new packages (e.g. like pip) to your local python environment (like an anaconda environment) run `pdm add matplotlib` for example if you wanted to add matplotlib. 

## Documents
The documents contain three main folders: docs, src, and tests.
* Docs contain the functional and component specifications and a background presentation
* Src contains the functions (casmodel_func.py and probability_func.py) and the GUI interface (casmodel.py)
* Tests contain the two test modules for the functions: casmodel_func.py and probability_func.py.


