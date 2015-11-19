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
	#Leave 'REMOVE's inline with temporary code so I can clean up easily.
	#META TODO's:
				# getBoundaryComponenets(rotationSystem) (implement boundary walk algo.)
				# isTwoSided(rotationSystem)
				# debug.
				# (optional) write unit tests.

import igraph
import itertools
import numpy

def generateCandidateGraphs():
	global g
	C_g = []
	temp = [] # Used to hold discovered candiate graphs until checking for and removing isomorphic copies.
	## (1) Find all graphs G for which:
	#		1a. V <= 2g.
	#		1b. V <= E <= 2g + V  #REMOVE - change back to 0 < E <= 2g + V.
	#		1c. G has no vertex of odd degree.
	#		1d. The only vertices of G with degree two are boomerangs.
	#		1e. G has at most g+1 boomerangs.

	# 1a. V <= 2g
	for V in range(1, 2*g+1):
		# 1b. V <= E <= 2g + V.
		for E in range(V, 2*g+V+1): #REMOVE - change back to 0 < E <= 2g + V.
			# Generate all graphs with V vertices and E edges.
			allGraphs = generateAllGraphs(V, E)
			# Check each of these graphs for properties 1c, 1d, and 1e.
			while len(allGraphs) > 0:
				graph = allGraphs.pop()
				# 1c. G has no vertex of odd degree.
				# 1d. The only vertices of G with degree two are boomerangs.
				# 1e. G has at most g+1 boomerangs.
				if hasNoVertexOfOddDegree(graph) and allDegreeTwoVerticesAreBoomerangs(graph) and atMostGPlusOneBoomerangs(graph):
					temp.append(graph.copy()) # Store this candidate graph in the list named 'temp'.
	## (2) Remove any isomorphic duplicates.
		C_g = removeIsomorphicCopies(temp)
	return C_g

def removeIsomorphicCopies(temp):
	C_g = []
	while len(temp) > 0:
		# Remove the first graph from temp and insert it at the begining of C_g.
		C_g.insert(0, temp.pop(0))
		# Remove from temp all graphs isomorphic to C_g[0].
		temp = [x for x in temp if not C_g[0].isomorphic(x)]
	return C_g

def atMostGPlusOneBoomerangs(graph):
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
		# If it's not a boomerange return False.
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
	# Goal: Return a list of all graphs on V vertices with E edges.
	allGraphs=[]
	# IMPORTANT: DO NOT return any graphs with isolated vertices!
	## (1) List every edge that can possibly occur on the V vertices.
	allPossibleEdges = list(itertools.combinations_with_replacement(range(0,V),2))
	## (2) List every possible way of choosing E edges from allPossibleEdges with replacement.
	allPossibleWaysOfChoosingTheEdges = itertools.combinations_with_replacement(allPossibleEdges,E)
	## (3) For each choice in allPossibleWaysOfChoosingTheEdges, create a graph on V vertices with those edge choices.
	for choice in allPossibleWaysOfChoosingTheEdges:
		# Create a graph, g, with with V vertices and the chosen edges.
		g = igraph.Graph(V)
		g.add_edges(list(choice))
		# If the resulting graph does not contain any isolated vertices then store it.
		if g.degree().count(0) == 0:
			allGraphs.append(g)
	return allGraphs

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
	## (1) Generate all rotation systems on candidateGraph.
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
	## Check whether g >= (E-V+n)/2 - 1.
	n = len(getBoundaryComponenets(rotationSystem)) # Number of boundary components
	E = candidateGraph.ecount()	# Number of edges 
	V = candidateGraph.vcount()	# Number of vertices
	if g >= (E-V+n)/2 - 1:
		return True
	return False

def getBoundaryComponenets(rotationSystem):
 	#TODO
 	# Goal: Apply the boundary-walk algorithm and return a list of boundary components for the reduced band decomposition corresponding to rotationSystem.
 	return

def generateAllRotationSystemsOn(candidateGraph):
	# Goal: Generate all rotation systems on candidateGraph.
	## (1) For each vertex, v, find the list of edge-ends incident to that vertex and store that list of edges in incidentEdgeEnds[v].
	incidentEdgeEnds = []	# incidentEdgeEnds[v] will return a list of edges incident to vertex v.
							# NOTE: Edges are labeled by thier index in candidateGraph.get_edgelist(). 
							# NOTE: For example, edge '4' refers to candidateGraph.get_edgelist()[4].
	for v in range(0, len(candidateGraph.vs())):
		edgeEndsIncidentToV = [(edgeIndex, 0) for edgeIndex, (edgeEndZero, edgeEndOne) in enumerate(candidateGraph.get_edgelist()) if edgeEndZero==v]
		edgeEndsIncidentToV += [(edgeIndex, 1) for edgeIndex, (edgeEndZero, edgeEndOne) in enumerate(candidateGraph.get_edgelist()) if edgeEndOne==v]
		incidentEdgeEnds.insert(v, edgeEndsIncidentToV)
		# NOTE: Edges are stored in candidateGraph.get_edgelist() as ordered pairs (a,b). We refer to 'a' and 'b' as 'edgeEndZero' and 'edgeEndOne', respectively.
	## (2) For each vertex, v, generate a list of all possible rotations at v. Store this list at allPossibleRotationsAt[v].
	# Initiate empty list.
	allPossibleRotationsAt = []
	for v in range(0,len(candidateGraph.vs())):
		allPossibleRotationsAt.insert(v, rotationsUpToCyclicPermutation(incidentEdgeEnds(v)))
	## (3) Generate all rotation systems on candidateGraph.
	listOfRotationOptions = [allPossibleRotationsAt[v] for v in range(0, len(candidateGraph.vs()))]
	allRotationSystems = [list(rotationSystem) for rotationSystem in itertools.product(*listOfRotationOptions)]
	# Return the list.
	return allRotationSystems

def rotationsUpToCyclicPermutation(listOfEdgeEnds):
	# Goal: Return a list of all rotations of listOfEdgeEnds -- unique up to cyclic permutations.
	rotationsToReturn = []
	# NOTE: Naively, we could simply return [x for x in itertools.permutations(listOfEdgeEnds)], and everything would work fine.
	# NOTE: While that would make code-verification easier, doing so results in burdensome runtime of the overall program.
	# NOTE: As a result, this is one area where I think the speedups are worth the increased code complexity.
	# NOTE: If the additional code complexity introduced by this function is burdensome to the referee, please let me know.
	# NOTE: I'm happy to refactor the code for this function to make its verification simpler -- albeit at the cost of increased time complexity of the overall program.
	
	# (1) Cycle through every permutation of listOfEdgeEnds.
	allPermutations = itertools.permutations(listOfEdgeEnds)
	for permutation in allPermutations:
		# NOTE: This permutation has len(listOfEdges) equivalent permutations. Namely all the cyclic permutations of this one.
		# NOTE: From among these equivalent permutations, we'll choose one 'standard representative', and store it in rotationsToReturn.
		# NOTE: We choose this standard representative as follows.
		# (2) Choose a standard representative.
		# Identify the smallest labelled edge.
		EdgeLabels = [a for (a,b) in permutation]
		smallestEdgeLabel = min(EdgeLabels)
		# Count haw many edge ends of this edge show up at this vertex (must be either 1 or 2).
		indicesOfSmallestEdgeLabel = [i for i,j in enumerate(EdgeLabels) if j == smallestEdgeLabel]
		numberOfSmallestEdgeLabels = len(indicesOfSmallestEdgeLabel)
		# If there is only one of them, then shift (cyclically permute) permutation so that the smallest labelled edge is in postion [0] of the rotation.
		if numberOfSmallestEdgeLabels == 1:
			standardRepresentative = numpy.roll(permutation, -indicesOfSmallestEdgeLabel[0]).tolist()
		else:
			# Else if there are two smallest-labelled edges in the list, then look at the following to equivalent permutations.
			# (a) The permutation where the first of the smallest-labelled edge is shifted to position [0] of the rotation.
			firstOption = numpy.roll(permutation, -indicesOfSmallestEdgeLabel[0]).tolist()
			# (b) The permutation where the second of the smallest-labelled edge is shifted to position [0] of the rotation.
			secondOption = numpy.roll(permutation, -indicesOfSmallestEdgeLabel[1]).tolist()
			# Of these two, we choose the one that comes first lexicographically. 
			if firstOption <= secondOption:
				standardRepresentative = firstOption
			else:
				standardRepresentative = secondOption
		# (3) Check to see whether that standard representative has already been stored in rotationsToReturn. If it's not, append it.
		if not [a for (a,b) in permutation] in [[a for (a,b) in rotation] for rotation in rotationsToReturn]:
			rotationsToReturn.append(standardRepresentative)
	return rotationsToReturn

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
