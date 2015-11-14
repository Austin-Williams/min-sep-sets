# The MIT License (MIT)

# Copyright (c) 2015 Austin Williams

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# ================================================================================

#Dev Notes:
	#Search for 'TODO's
	#Leave 'REMOVES' inline with temporary code so I can clean up easily.

import igraph
import numpy
import math

def generateCandidateGraphs():
	global g
	C_g = []
	temp = [] # Used to hold discovered candiate graphs until checking for and removing isomorphic copies.
	## (1) Find all graphs G for which:
	#		1a. V <= 2g
	#		1b. V <= E <= 2g + V
	#		1c. G has no vertex of odd degree
	#		1d. The only vertices of G with degree two are boomerangs
	#		1e. G has at most g+1 boomerangs

	# 1a. V <= 2g
	for V in range(1, 2*g+1):
		# 1b. V <= E <= 2g + V
		for E in range(V, 2*g+V+1):
			# Generate all graphs with V vertices and E edges
			allGraphs = generateAllGraphs(V, E)
			# Check each of these graphs for properties 1c, 1d, and 1e.
			while len(allGraphs) > 0:
				graph = allGraphs.pop()
				# 1c. G has no vertex of odd degree
				# 1d. The only vertices of G with degree two are boomerangs
				# 1e. G has at most g+1 boomerangs
				if hasNoVertexOfOddDegree(graph) and allDegreeTwoVerticesAreBoomerangs(graph) and atMostGPulsOneBoomerangs(graph):
					temp.append(graph.copy()) # Store this candidate graph in the list named 'temp'.
	## (2) Remove any isomorphic duplicates.
		C_g = removeIsomorphicCopies(temp)
	return C_g

def removeIsomorphicCopies(temp):
	#TODO
	C_g = []
	return C_g

def atMostGPulsOneBoomerangs(graph):
	#TODO - boolean
	return

def allDegreeTwoVerticesAreBoomerangs(graph):
	#TODO - boolean
	return

def hasNoVertexOfOddDegree(graph):
	#TODO - boolean
	return
def generateAllGraphs(V, E):
	#TODO
	# Goal: Return a list of all graphs on V vertices with E edges.
	return

def findMinimalSeparatingGraphsIn(C_g):
	# The input C_g is a list of candidate graphs.
	# Goal: Check each graph in C_g to see if it has a minimal separating embedding in a surface of genus g.
	G_g = []
	for candidateGraph in C_g:
		if thereExistsAMinimalSeparatingEmbeddingOf(candidateGraph):
			G_g.append(candidateGraph)
	return G_g

def reportResults(G_g):
	#TODO
	return

def thereExistsAMinimalSeparatingEmbeddingOf(candidateGraph):
	# Description: Returns True if and only if there exists a minimal separating embedding of candidateGraph into a genus 2 surface.
	## (1) Generate all rotation systems on candidateGraph
	rotationSystems = generateAllRotationSystemsOn(candidateGraph)
	## (2) Check whether any of them have a minimal separating embedding into a surface of genus 2.
	for rotationSystem in rotationSystems:
		if isTwoSided(rotationSystem) and SatisfiesTheorem4(rotationSystem,candidateGraph):
			return True
	return False

def isTwoSided(rotationSystem):
	#TODO
	return

def SatisfiesTheorem4(rotationSystem,candidateGraph):
	global g
	## Check whether g >= (E-V+n)/2 - 1
	n = len(getBoundaryComponenets(rotationSystem)) # Number of boundary components
	E = candidateGraph.ecount()	# Number of edges 
	V = candidateGraph.vcount()	# Number of vertices
	if g >= (E-V+n)/2 - 1:
		return True
	return False

def getBoundaryComponenets(rotationSystem):
 	#TODO - apply the boundary-walk algorithm and return a list of boundary components
 	return

def generateAllRotationSystemsOn(candidateGraph):
	#TODO
	# Generate all rotation systems on candidateGraph.
	rotationSystems = []
	return rotationSystems

def main():
	global g
	g = 2 # Note: g must be greater than 0.
	## (1) Generate the finite set, C_g, of candidate graphs for genus g.
	C_g = generateCandidateGraphs()
	## (2) Check each graph in C_g to determine whether or not it has a minimal separating embedding in a surface of genus g.
	G_g = findMinimalSeparatingGraphsIn(C_g)
	## (3) Log and display the results.
	reportResults(G_g)
	return

if __name__ == '__main__':
  main()
