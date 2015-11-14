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
	#META TODO's:
		#decide on rotation system format (list of lists of integers or list of lists of ordered pairs)

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
	C_g = []
	while len(temp) > 0:
		# Remove the first graph from temp and insert it at the begining of C_g
		C_g.insert(0, temp.pop(0))
		# Compare the new graph, C_g[0], that we inserted at the begining of C_g to every graph remaining in temp.
		for indexOfTempGraph, tempGraph in reversed(list(enumerate(temp))): # We work through the temp list backwards.
		# Note: tempGraph is the graph in temp which we are currently examining, and indexOfTempGraph is it's index in temp. So temp[indexOfTempGraph] is tempGraph.
		# Compare C_g[0] to tempGraph and determine whether they are isomorpic.
			if C_g[0].isomorphic(tempGraph):
				# If they are isomorphic then remove tempGraph from temp.
				temp.remove(indexOfTempGraph)
	return C_g

def atMostGPulsOneBoomerangs(graph):
	global g
	# List the degrees of each vertex in graph.
	listOfDegrees = graph.degree()
	# Make a list of the vertices with degree 2.
	verticesWithDegreeTwo = [i for i, j in enumerate(listOfDegrees) if j==2]
	# Count the number of degree two vertices that are boomerangs.
	numberOfBoomerangs = [isABoomerang(vertex, graph) for vertex in verticesWithDegreeTwo].count(True)
	# Return True if numberOfBoomerangs is <= g+1
	if numberOfBoomerangs <= g + 1:
		return True
	# Otherwise return False
	return False

def allDegreeTwoVerticesAreBoomerangs(graph):
	# List the degrees of each vertex in graph.
	listOfDegrees = graph.degree()
	# Make a list of the vertices with degree 2.
	verticesWithDegreeTwo = [i for i, j in enumerate(listOfDegrees) if j==2]
	# Examine each vertex of degree two to see if it's a boomerang.
	while len(verticesWithDegreeTwo) > 0:
		vertexToExamine = verticesWithDegreeTwo.pop()
		# If it's not a boomerange return False
		if not isABoomerang(vertexToExamine,graph):
			return False
	# If all degree two vertices are boomerangs then return True.
	return True

def isABoomerang(vertexToExamine, graph):
	# Check that it has degree two. Return False if not.
	if graph.degree(vertexToExamine) != 2:
		return False
	# List all the neighbors of vertexToExamine.
	neighbors = graph.neighbors(vertexToExamine)
	# Count the number of neighbors of vertexToExamine that are not vertexToExamine itself.
	numberOfNonSelfNeighbors = len([i for i, j in enumerate(neighbors) if j!=vertexToExamine])
	# Return True if numberOfNonSelfNeighbors is 0.
	if numberOfNonSelfNeighbors == 0:
		return True
	# Return False otherwise.
	return False

def hasNoVertexOfOddDegree(graph):
	# Goal: This function returns True if graph has no vertex of odd degree, and returns False otherwise.
	# Get a list of the degrees of all the vertices in graph.
	listOfDegrees = graph.degree()
	# Count how many vertices have odd degree.
	numOfVerticesWithOddDegree = [x%2 for x in listOfDegrees].count(1)
	# Return True if and only if zero vertices have odd degree.
	return numOfVerticesWithOddDegree == 0

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
