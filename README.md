# min-sep-sets
Classifying Minimal Separating Sets of Orientable Surfaces of Low Genus

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

`$ rm -rf minsepsets`

Done!

## Computing Minimal Separating Graphs for Orientable Surfaces of Genus Other Than Two
The program is written for arbitrary genus g. The global variable, g, declared in the *main()* function determines the genus of the surface for whose minimal separating graphs this program searches. It is set to `g = 2` by default.

To find the minimal separating graphs for genus 1, for example, simply set `g =  1` in the *main()* function in *findMinSepGraphs.py*. Be aware, though, that the time this program takes to run is superexponential in g. So anything beyond genus 3 may be unrealistic without big-O improvements to the underlying algorithm.

## A Note on the Programming Style
This program is an implementation of an algorithm that can be found in a formal mathematics paper being submitted for peer-review.  As a result, this program is written with the intention of being *easy to verify*. It is *not* written for *optimal efficiency*. Whenever a choice between clarity and efficiency must be made, we always err on the side of clarity and ease of verification over space- or time-complexity. 

There is a single exception to this rule. The algorithm calls for the program to, given a graph, list all possible rotation sytems on that graph. Implemented naively, this could result in a runtime of several days for genus `g = 2`. By allowing ourselves to optimize this function (by not listing rotation systems that are equivalent to ones we've already listed), we are able to reduce the runtime for genus `g = 2` to less than a few minutes. Although the correctness of the naive implementation of this one function would be esier to verify, we think the trade-off between clarity and efficiency is worthwhile in this case.
