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
				# debug.
				# (optional) write unit tests.

import igraph
import itertools
import numpy
import logging

# Using basic logger configuration.
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def generateCandidateGraphs():
	logger.info('Generating candidate graphs.')
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
	logger.info('Completed generation of candidtate graphs.')
	logger.debug('Total number of candidate graphs: %s.', len(C_g))
	return C_g

def removeIsomorphicCopies(temp):
	C_g = []
	while len(temp) > 0:
		# Pop the first graph from temp and insert it at the begining of C_g.
		C_g.insert(0, temp.pop(0))
		# Remove from temp all graphs isomorphic to C_g[0].
		temp = [x for x in temp if not C_g[0].isomorphic_vf2(x)]
	C_g.reverse()
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
		newGraph = igraph.Graph(V)
		newGraph.add_edges(list(choice))
		# If the resulting graph does not contain any isolated vertices then store it.
		if newGraph.degree().count(0) == 0:
			allGraphs.append(newGraph)
			del newGraph

	# TODO add the single isolated loop to this list if needed. Alternatiecly, we could add it at the end.
	return allGraphs

def findMinimalSeparatingGraphsIn(C_g):
	logger.info('Searching through C_g for minimal separating graphs.')
	# The input C_g is a list of candidate graphs.
	# Goal: Check each graph in C_g to see if it has a minimal separating embedding in a surface of genus g.
	G_g = []
	for candidateGraph in C_g:
		logger.debug('\n Checking graph with edge list %s', candidateGraph.get_edgelist())
		if thereExistsAMinimalSeparatingEmbeddingOf(candidateGraph):
			logger.debug('Found a minimal separating embedding')
			G_g.append(candidateGraph)
	return G_g

def reportResults(G_g):
	#TODO
	logger.info('G_g is %s', G_g)
	for graph in G_g: #REMOVE 
		print graph.get_edgelist()  #REMOVE 
	logger.info('G_g has size %s', len(G_g))
	return

def thereExistsAMinimalSeparatingEmbeddingOf(candidateGraph):
	global g
	logger.debug('Searching rotation systems on this graph for minsep embeddings')
	# Description: Returns True if and only if there exists a minimal separating embedding of candidateGraph into a genus 2 surface.
	## (1) Generate all rotation systems on candidateGraph.
	rotationSystems = generateAllRotationSystemsOn(candidateGraph)
	logger.debug('Number of rotation systems on this graph: %s ', len(rotationSystems))
	## (2) Check whether any of them have a minimal separating embedding into a surface of genus 2.
	for rotationSystem in rotationSystems:
		if satisfiesTheorem4(rotationSystem,candidateGraph):
			if isTwoSided(rotationSystem, candidateGraph):
				logger.debug('Found a rotation system that is both two-sided and satisfiestheorem 4')
				return True
			else:
				logger.debug('DID NOT find a two-sided rotation system')
		else:
			logger.debug('DOES NOT satisfy Theorem4')
	logger.debug('This graph DOES NOT have a minimal separating embedding in genus %s \n\n', g)
	return False

def isTwoSided(rotationSystem, candidateGraph):
	# Goal: Return True is rotationSystem is two-sided, and return False otherwise.
	# Get the number of edges in the graph.
	numOfEdges = len(list(candidateGraph.es()))
	# Get the list of boundary components of the reduced band decomposition corresponding to rotationSystem.
	boundaryComponents = getBoundaryComponents(rotationSystem)
	# Consider every possible partition of the boundary components into two cells (which we'll call 'black' and 'white').
	partitionTypes = list(itertools.combinations_with_replacement(['black','white'],len(boundaryComponents)))
	# Each partition assigns every boundary component to either blackList or whiteList.
	for partType in partitionTypes:
		partitions = list(itertools.permutations(partType))
		for partition in partitions:
			blackList=[]
			whiteList=[]
			for componentNumber in range(len(boundaryComponents)):
				if partition[componentNumber] == 'black':
					blackList+=boundaryComponents[componentNumber]
				else: 
					whiteList+=boundaryComponents[componentNumber]
			# Check to see if each edge of candidateGraph appears in both the blackList and the White list.
			if all([((edge in blackList) and (edge in whiteList)) for edge in range(numOfEdges)]):
				# If so, then the rotationSystem is two-sided.
				logger.debug('Found a two-sided rotation system')
				return True
	return False

def satisfiesTheorem4(rotationSystem,candidateGraph):
	global g
	## Check whether g >= (E-V+n)/2 - 1.
	n = len(getBoundaryComponents(rotationSystem)) # Number of boundary components
	E = candidateGraph.ecount()	# Number of edges 
	V = candidateGraph.vcount()	# Number of vertices
	if g >= (E-V+n)/2 - 1:
		logger.debug('satisfies Theorem4')
		return True
	return False

def getBoundaryComponents(rotationSystem):
 	# Goal: Apply the boundary-walk algorithm and return a list of boundary components for the reduced band decomposition corresponding to rotationSystem.
 	boundaryComponents = []
 	## (1) First list, for each vertex v, all the edge-end-connections at that vertex in edgeEndConnectionsAt[v].
 	edgeEndConnectionsAt = [[] for x in rotationSystem]
 	for v in range(len(rotationSystem)):
 		#Create list of edgeEndConnections[v] at each vertex.
 		for connection in range(len(rotationSystem[v])):
 			# NOTE: The boolean False will be changed to True later on, after this edgeEndConnection is traversed in the boundaryWalk algorithm.
 			edgeEndConnectionsAt[v].append([rotationSystem[v][connection],rotationSystem[v][(connection+1)%len(rotationSystem[v])],False])
 	## (2) Perform the boundaryWalk algorithm until all edge-end-connections have been traversed.
 	while (not all([all([c for [a,b,c] in edgeEndConnectionsAt[x]]) for x in range(len(edgeEndConnectionsAt))])): # This loops until all edge-end connections have been marked 'True'.
 		# Find the first edge-end connection that hasn't been traversed yet (that is, the first edge-end connection that is still marked False).
 		# Check each vertex one at a time, looking for an edge-end-connection that is marked false.
 		for v in range(len(rotationSystem)):
 			# Check if there is an edge-end-connection still marked False.
 			if False in [c for [a,b,c] in edgeEndConnectionsAt[v]]:
 				# If so then let edgeEndConnection be the first one.
 				edgeEndConnection = edgeEndConnectionsAt[v][[c for [a,b,c] in edgeEndConnectionsAt[v]].index(False)]
 				break
 		# Perform the boundaryWalk algorithm starting with this edge-end-connection and store the traversed edge-end-connections.
 		boundaryComponent = boundaryWalk(edgeEndConnection, edgeEndConnectionsAt)
 		# Append this new boundary component to the list of BoundaryComponents.
 		boundaryComponents.append(boundaryComponent)
 	# TODO: Create an explaination with images exaplaining how the boundary walk algorithm works in the README.md.
 	return boundaryComponents

def boundaryWalk(inputEdgeEndConnection, edgeEndConnectionsAt):
	# Goal: Perform the boundary walk algorithm begining at inputEdgeEndConnection. Mark the edge-end connections traversed True.
	# Goal: Return the boundaryComponent as a list of all edges traversed.
	# Begin with edgeEndConnection.
	traversedEdgeEndConnections = []
	currentEdgeEndConnection = inputEdgeEndConnection

	traversedEdgeEndConnections.append(currentEdgeEndConnection)
	outgoingEdgeEnd = currentEdgeEndConnection[1]
	nextIncomingEdgeEnd = [outgoingEdgeEnd[0],(outgoingEdgeEnd[1]+1)%2]
	# Find the edgeEndConnection that has nextIncomingEdgeEnd as it's incoming edge-end. We'll search one vertex at a time.
	for v in range(len(edgeEndConnectionsAt)):
		if nextIncomingEdgeEnd in [a for [a,b,c] in edgeEndConnectionsAt[v]]:
			index = [a for [a,b,c] in edgeEndConnectionsAt[v]].index(nextIncomingEdgeEnd)
			# Make that edgeEndConnection the new currentEdgeEndConnection.
			currentEdgeEndConnection = edgeEndConnectionsAt[v][index]
			break
	# Repeat until we end up back at the inputEdgeEndConnection.
	while currentEdgeEndConnection is not inputEdgeEndConnection:
		traversedEdgeEndConnections.append(currentEdgeEndConnection)
		outgoingEdgeEnd = currentEdgeEndConnection[1]
		nextIncomingEdgeEnd = [outgoingEdgeEnd[0],(outgoingEdgeEnd[1]+1)%2]
		# Find the edgeEndConnection that has nextIncomingEdgeEnd as it's incoming edge-end. We'll search one vertex at a time.
		for v in range(len(edgeEndConnectionsAt)):
			if nextIncomingEdgeEnd in [a for [a,b,c] in edgeEndConnectionsAt[v]]:
				index = [a for [a,b,c] in edgeEndConnectionsAt[v]].index(nextIncomingEdgeEnd)
				# Make that edgeEndConnection the new currentEdgeEndConnection.
				currentEdgeEndConnection = edgeEndConnectionsAt[v][index]
				break
	# Store the set of edges traversed in the variable named boundaryComponent.
	edgesTraversed = []
	for connection in traversedEdgeEndConnections:
		edgesTraversed += [connection[0][0], connection[1][0]]
	# Remove duplicate edges from the list edgesTraversed.
	boundaryComponent = list(set(edgesTraversed))
	#  For each edge-end-connection that was traversed, mark that connection True in edgeEndConnections.
	for connection in traversedEdgeEndConnections:
		# Find that connection in edgeEndConnectionsAt. We'll search one vertex at a time.
		for v in range(len(edgeEndConnectionsAt)):
			if connection in edgeEndConnectionsAt[v]:
				indexOfTraversedEdgeEnd = edgeEndConnectionsAt[v].index(connection)
				edgeEndConnectionsAt[v][indexOfTraversedEdgeEnd][2] = True
				break
	return boundaryComponent

def generateAllRotationSystemsOn(candidateGraph):
	# Goal: Generate all rotation systems on candidateGraph.
	## (1) For each vertex, v, find the list of edge-ends incident to that vertex and store that list of edges in incidentEdgeEnds[v].
	incidentEdgeEnds = []	# incidentEdgeEnds[v] will return a list of edges incident to vertex v.
							# NOTE: Edges are labeled by thier index in candidateGraph.get_edgelist(). 
							# NOTE: For example, edge '4' refers to candidateGraph.get_edgelist()[4].
	for v in range(0, len(candidateGraph.vs())):
		edgeEndsIncidentToV = [[edgeIndex, 0] for edgeIndex, (edgeEndZero, edgeEndOne) in enumerate(candidateGraph.get_edgelist()) if edgeEndZero==v]
		edgeEndsIncidentToV += [[edgeIndex, 1] for edgeIndex, (edgeEndZero, edgeEndOne) in enumerate(candidateGraph.get_edgelist()) if edgeEndOne==v]
		incidentEdgeEnds.insert(v, edgeEndsIncidentToV)
		# NOTE: Edges are stored in candidateGraph.get_edgelist() as ordered pairs (a,b). We refer to 'a' and 'b' as 'edgeEndZero' and 'edgeEndOne', respectively.
	## (2) For each vertex, v, generate a list of all possible rotations at v. Store this list at allPossibleRotationsAt[v].
	# Initiate empty list.

	allPossibleRotationsAt = []

	for v in range(0,len(candidateGraph.vs())):
		allPossibleRotationsAt.insert(v, rotationsUpToCyclicPermutation(incidentEdgeEnds[v]))
	## (3) Generate all rotation systems on candidateGraph.
	listOfRotationOptions = [allPossibleRotationsAt[v] for v in range(0, len(candidateGraph.vs()))]
	allRotationSystems = [list(rotationSystem) for rotationSystem in itertools.product(*listOfRotationOptions)]
	# Return the list.
	return allRotationSystems

def allLoopsOptimisation(R_B, P, rotationsToReturn):
	# TODO : leave goal for this.
	if len(P) == 0:
		rotationsToReturn.append(R_B)
		return
	# Else there are edges to place.
	Pcopy = list(P)
	e_lowest = min(Pcopy)
	Pcopy.remove(e_lowest)
	R_Bcopy = list(R_B)
	R_Bcopy[R_Bcopy.index([])] = e_lowest
	## Place the other end of e_lowest.
	e_lowestOtherEnd = [e_lowest[0], e_lowest[1]+1%2]
	Pcopy.remove(e_lowestOtherEnd)
	# List indices of the unfilled slots in R_B
	indicies = [i for i,j in enumerate(R_Bcopy) if j ==[]]
	for index in indicies:
		R_BcopyCopy = list(R_Bcopy)
		R_BcopyCopy[index]=e_lowestOtherEnd
		allLoopsOptimisation(R_BcopyCopy, Pcopy, rotationsToReturn)
		del R_BcopyCopy
	del R_Bcopy
	del Pcopy
	return

def rotationsUpToCyclicPermutation(listOfEdgeEnds):
	# Goal: Return a list of all rotations of listOfEdgeEnds -- unique up to cyclic permutations.
	rotationsToReturn = []
	## If listOfEdgeEnds consists entirely of loops, then we have a special optimisation that we can use.
	allEdgesAreLoops = True
	logger.debug("listOfEdgeEnds is %s \n\n", listOfEdgeEnds)
	for edgeEnd in listOfEdgeEnds:
		logger.debug('edgeEnd is %s \n\n', edgeEnd)
		if [edgeEnd[0], (edgeEnd[1]+1)%2] not in listOfEdgeEnds:
			allEdgesAreLoops = False
			break
	if allEdgesAreLoops:
		P = list(listOfEdgeEnds)
		R_B = [[] for n in range(0,len(P))]
		allLoopsOptimisation(R_B, P, rotationsToReturn)
		return rotationsToReturn
	# NOTE: Naively, we could simply return [x for x in itertools.permutations(listOfEdgeEnds)], and everything would work fine.
	# NOTE: While that would make code-verification easier, doing so results in burdensome runtime of the overall program.
	# NOTE: As a result, this is one area where I think the speedups are worth the increased code complexity.
	# NOTE: If the additional code complexity introduced by this function is burdensome to the referee, please let me know.
	# NOTE: I'm happy to refactor the code for this function to make its verification simpler -- at the cost of an increased runtime for the overall program.
	# NOTE: See README.md for a high level explination of how this function works.
	# (1) Find the smallest-labelled edge in listOfEdges.
	edgeLabels = [a for (a,b) in listOfEdgeEnds]
	smallestEdgeLabel = min(edgeLabels)
	# (2) Count how many edgeEnds in listOfEdges have this edge label (must be either 1 or 2).
	indicesOfSmallestEdgeLabel = [i for i,j in enumerate(edgeLabels) if j == smallestEdgeLabel]
	numberOfSmallestEdgeLabels = len(indicesOfSmallestEdgeLabel)
	if numberOfSmallestEdgeLabels == 1:
		# Make a copy of listOfEdges that we can manipulate locally. Remove smallest-labelled edge from the list.
		listOfEdgeEndsWithoutSmallest = list(listOfEdgeEnds)
		smallestLabelledEdge = listOfEdgeEndsWithoutSmallest.pop(indicesOfSmallestEdgeLabel[0])
		# List all possible permutations of listOfEdgeEndsWothoutSmallest.
		allPermutations = itertools.permutations(listOfEdgeEndsWithoutSmallest)
		# Attach smallestLbelledEdge to the begining of each of these permutations.
		for permutation in allPermutations:
			standardRepresentative = list(permutation)
			standardRepresentative.insert(0, smallestLabelledEdge)
			# Append the result to rotationsToReturn.
			rotationsToReturn.append(standardRepresentative)
	else: # Then both edge-ends of the smallest-labelled edge appear at this vertex.
		# Identify which of the smallest-labelled edge ends is edgeEndZero.
		if listOfEdgeEnds[indicesOfSmallestEdgeLabel[0]][1] == 0:
			indexOfSmallestEdgeEnd = indicesOfSmallestEdgeLabel[0]
		else:
			indexOfSmallestEdgeEnd = indicesOfSmallestEdgeLabel[1]
		# Make a copy of listOfEdges that we can manipulate locally. Remove smallest-labelled edge (with edgeEndZero) from the list.
		listOfEdgeEndsWithoutSmallest = list(listOfEdgeEnds)
		smallestLabelledEdge = listOfEdgeEndsWithoutSmallest.pop(indexOfSmallestEdgeEnd)
		# List all possible permutations of listOfEdgeEndsWothoutSmallest.
		allPermutations = itertools.permutations(listOfEdgeEndsWithoutSmallest)
		# Attach smallestLbelledEdge to the begining of each of these permutations.
		for permutation in allPermutations:
			# There are two options for representatives of the rotation associated with this permutation.
			# Option1 is just the smallestLabelledEdge followed by the rest of the edges in the permutation.
			option1 = list(permutation)
			option1.insert(0, smallestLabelledEdge)
			option1 = [list(element) for element in option1] # This converts option1 from a list of tuples to a list of lists so we can compare to option2 below.
			# option2 is option1 shifted so that the other edge-end of smallest-labelled edge appears in the first position of the rotation.
			option2 = list(permutation)
			option2.insert(0, smallestLabelledEdge)
			indexOfOtherEnd = option2.index([smallestEdgeLabel,1])
			option2 = numpy.roll(option2, -indexOfOtherEnd, 0).tolist()
			# Now choose which of the two options is lexicographically smaller (considering only the first entry of each tuple).
			if [a for [a,b] in option1] <= [a for [a,b] in option2]:
				standardRepresentative = option1
			else:
				standardRepresentative = option2
			# If we haven't already stored this rotation in rotationsToReturn, then do so now.
			if not [a for (a,b) in standardRepresentative] in [[a for (a,b) in rotation] for rotation in rotationsToReturn]:
				rotationsToReturn.append(standardRepresentative)
	return rotationsToReturn

def main():
	global g
	g = 2 # Note: g must be greater than 0.
	logger.info('Initiating search for minimal separating graphs in surfaces of genus %s', g)
	## (1) Generate the finite set, C_g, of candidate graphs for genus g.
	C_g = generateCandidateGraphs()
	## (2) Check each graph in C_g to determine whether or not it has a minimal separating embedding in a surface of genus g.
	G_g = findMinimalSeparatingGraphsIn(C_g)
	## (3) Log and display the results.
	reportResults(G_g)
	return

if __name__ == '__main__':
  main()
