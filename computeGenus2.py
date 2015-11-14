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

import igraph
import numpy
import math

def generateCandidateGraphs():
	global g
	C_g =[]
	## (2) Find all graphs G for which:
	#		V <= 2g
	#		0 < E <= 2g + V
	#		G has no vertex of odd degree
	#		The only vertices of G with degree two are boomerangs
	#		G has at most g+1 boomerangs
	## (2) Remove any isomorphic duplicates
	return C_g

def findMinimalSeparatingGraphsIn(C_g):
	# The input C_g is a list of candidate graphs.
	G_g = []
	# Goal: Check each graph in C_g to see if it has a minimal separating embedding in a surface of genus g.
	for candidateGraph in C_g:
		if thereExistsAMinimalSeparatingEmbeddingOf(candidateGraph):
			G_g.append(candidateGraph)
	return G_g

def reportResults(G_g):
	return

def thereExistsAMinimalSeparatingEmbeddingOf(candidateGraph):
	# Returns true if and only if there exists a minimal separating embedding of candidateGraph into a genus 2 surface.
	return

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
