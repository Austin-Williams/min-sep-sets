# min-sep-sets
Classifying Minimal Separating Sets of Low Genus Surfaces

TODO: Explain coding style.
TODO: Give high level overview of rotationsUpToCyclicPermutation(listOfEdgeEnds).

## Getting Started
#### If you DO have admin priveleges on your machine then use this method:

Install python-igraph:

`$ sudo pip install python-igraph`

Install NetworkX:

`$ sudo pip install networkx`

Fork this repository:

`$ git clone https://github.com/Austin-Williams/min-sep-sets.git`

Move into the min-sep-sets folder:

`$ cd min-sep-sets`

Run the program:

`$ python findMinSepGraphs.py`

Done!

#### If you DO NOT have admin priveleges on your machine then use this method:
If you don't have admin rights to your machine then you may not be able to install python-igraph and NetworkX using the above method. Instead, try using virtualenv as follows.

Start the virtual environment:

`$ virtualenv minsepsets`

Activate it:

`$ source minsepsets/bin/activate`

Install python-igraph:

`$ easy_install python-igraph`

Install NetworkX:

`$ easy_install networkx`

Fork this repository:

`$ git clone https://github.com/Austin-Williams/min-sep-sets.git`

Move into the min-sep-sets folder:

`$ cd min-sep-sets`

Run the program:

`$ python findMinSepGraphs.py`

The program will display the results in the command line, and will also store the results in a text file on your machine.

When you are finished running the program, deactivate the virtual environment:

`$ deactivate`

Then delete the virtual envirnoment by delting its folder:

`rm -rf envname`

Done!
