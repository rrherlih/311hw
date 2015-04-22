 #!/usr/bin/env python3

"""	Ryan Herlihy
	CS 311
	Graph Two-Colorability
"""

import sys

""" The Graphs class takes in the graph file and does the work to figure out if the graph can be
	two-colored. The functions within this class open the graph file, create an adjacency list 
	for the graph, breadth first search to color the graph, and find odd cycles."""

class Graphs:

	def __init__(self, graph):
		self.graph = graph

	def open_file(self, filename):
		try:
			return(open(filename))
		except:
			print("Error opening the graph.")
			usage()

	""" This function opens the graph file, then reads the first line to determine how many
		vertices there are. The array adj_list places the number of vertices in the 0th index.
		Then a Vertex object is appended to the array for however many vertices there are.
		A Vertex object has a few attributes including a color, if its been visited or not,
		and a list of vertices it is adjacent to. The Vertex number corresponds to its index
		in the array."""

	def create_adj_list(self):
		self.fd = self.open_file(self.graph)
		num = int(self.fd.readline())
		adj_list = [num]
		for i in range(1, num + 1):
			adj_list.append(Vertex())

		""" A while loop reads in each edge in the graph file. Since there are two vertices 
			in each edge and the graphs are undirected, the second vertex is added to the
			adjacency list of the first vertex and vice versa. In the end, every Vertex will
			have a complete adjacency list of all the vertices it is adjacent to. """

		while True:
			line = self.fd.readline().strip()
			if not line:
				break
			else:
				edge = self.edge_to_tuple(line)
				adj_list[edge[0]].add_adj(edge[1])
				adj_list[edge[1]].add_adj(edge[0])
		return(adj_list)

	""" This function is basically a breadth first search algorithm, but it also colors each
		vertex the color opposite of its parent. If it tries to color a vertex that has already
		been colored, a different color, then it knows that this graph is not two-colorable.
		It begins by creating a queue and enqueues the starting vertex that is passed to it.
		Then the vertex color is set to 1 and the visit attribute is set to 1(visited, but
		not finished)."""

	def bfs(self, vertex, adj_list):
		q = Queue()
		q.enqueue(vertex)
		adj_list[vertex].set_color(1)
		adj_list[vertex].set_visit(1)

		""" A while loop continues until the queue is empty. The first element of the queue
			id retrieved and its color is set to c. A for loop then gets each of vertices
			adjacent to u. If v hasn't been seen yet(visited = 0), then v's parent is set
			to u, its visit attribute is set to 1, its colored 1 or 0 depending on c, and
			finally enqueued.
			If v has already been visited, then we check to see if its color is different from
			c. If it is, then we don't do anything. If its the same as c, then that means there
			is a conflict and the graph cannot be two colored. The function odd_cycle() then
			is run to find the odd cycle in the graph.
			At the end of the for loop, the queue is dequeued and u's visit attribute id set
			to 2 (finished)"""

		while q.is_empty() == False:
			u = q.get_front()
			c = adj_list[u].get_color()
			for v in adj_list[u].get_adjs():
				
				if adj_list[v].get_visit() == 0:
					adj_list[v].set_parent(u)	
					adj_list[v].set_visit(1)
					if c == 1:
						adj_list[v].set_color(0)
					if c == 0:
						adj_list[v].set_color(1)
					q.enqueue(v)	
				if adj_list[v].get_visit() == 1:
					if c == 1:
						if adj_list[v].get_color() == 1:
							self.odd_cycle(u, v, adj_list)
							sys.exit()

					if c == 0:
						if adj_list[v].get_color() == 0:
							self.odd_cycle(u, v, adj_list)
							sys.exit()			
					
			q.dequeue()
			adj_list[u].set_visit(2)

		""" Adjacency list is returned with correct coloring."""

		return(adj_list)

	""" This function takes the u and v vertex from the bfs function that were involved
		in the coloring conflict. An array is created with the two vertices. Since we
		know there is an odd cycle, these two vertices much share an ancestor. The while
		loop gets the parents of u and v and compares them, then recursively compares each
		vertex's parent until we find the common ancestor. Each run through the while loop, 
		u is added to the front of the array and v is added to the end so that in the end
		the vertices in the odd cycle are in order."""

	def odd_cycle(self, u, v, adj_list):
		cycle = [u, v]
		while True:
			u = adj_list[u].get_parent()
			v = adj_list[v].get_parent()
			if u == v:
				cycle = [u] + cycle
				break
			cycle = [u] + cycle
			cycle = cycle + [v]	

		""" A file OddCycle.txt is created and each vertex in the cycle array is written.
			A second file named after the graph file is created with 'no' written."""

		target = open('OddCycle.txt', 'w')
		for i in cycle:
			target.write("{}\n".format(i))	
		target2 = self.output_name()
		target2.write("no\n\nodd cycle")	
	
	""" The variable a gets the adjacency list created in create_adj_list(). s is set to 1, 
		and will be the starting vertex. A while loop runs the bfs function to color the graph.
		disconnect_check() then makes sure there aren't any unconnected portions of the graph
		that haven't been colored. The while loop will continue using an unvisited vertex as
		the starting point for the next bfs."""

	def color_graph(self):
		a = self.create_adj_list()
		s = 1
		while True:
			adj_list = self.bfs(s, a)
			a = adj_list
			s = self.disconnect_check(adj_list)
			if s == 0:
				break

		""" A file is created named after the graph file and in it 'yes' is written along
			with the coloring of each vertex in the graph."""

		target = self.output_name()
		target.write("yes\n\nColoring:\n")
		for i in range(1, len(adj_list)):
			target.write("{} {}\n".format(i, adj_list[i].get_color()))

	""" Takes the graph filename inputted and returns a file with a name corresponding
		to the input filename to be written to."""

	def output_name(self):
		path = self.graph.split('/')
		name = "{}-Output".format(path[-1])
		target = open(name, 'w')
		return(target)
		
	""" This function takes an edge from the graph and returns a tuple. (The if statement
		just puts the smaller vertex first, but is not really necessary)"""

	def edge_to_tuple(self, edge):
		l = edge.split()
		v1 = int(l[0])
		v2 = int(l[1])
		if v1 < v2:
			return(v1, v2)
		else:
			return(v2, v1)

	""" Loops through vertices trying to find any unconnected portions of the graph by checking
		to see if it hasn't been colored yet. It then returns the vertex or 0 if all the vertices
		are colored.""" 

	def disconnect_check(self, adj_list):
		for i in range(1, len(adj_list)):
			if adj_list[i].get_color() == -1:
				return(i)
		return(0)
	
""" Standard queue that has a pointer to the last element and the first element. enqueue puts
	an element in the back, dequeue removes and returns the first element. get_front returns
	first element."""

class Queue:

	def __init__(self):
		self.front = None
		self.back = None

	def enqueue(self, v):
		item = [v, None]
		if self.front == None:
			self.front = item
			self.back = item
		else:
			self.back[1] = item
			self.back = item

	def dequeue(self):
		if self.is_empty() == True:
			return
		v = self.front[0]
		self.front = self.front[1]
		return(v)

	def get_front(self):
		return(self.front[0])

	def is_empty(self):
		if self.front == None:
			return True
		else:
			return False

""" Vertex object is used to represent a vertex in the graph. It keeps all the info associated
	with the vertex such as: its color, parent, its visited/finished status, and adjacency
	list. All colors are initialized to -1, and colors can either be 0 or 1. For visited status,
	0 = not seen, 1 = visited but not finished, 2 = finished. Parent is the vertex that first
	discovered this vertex."""

class Vertex:

	def __init__(self):
		self.color = -1
		self.adjs = []
		self.parent = None
		self.visit = 0

	def get_color(self):
		return(self.color)

	def set_color(self, color):
		self.color = color

	def get_adjs(self):
		return(self.adjs)

	def add_adj(self, adjacency):
		self.adjs.append(adjacency)

	def set_parent(self, v):
		self.parent = v

	def get_parent(self):
		return(self.parent)

	def set_visit(self, c):
		self.visit = c

	def get_visit(self):
		return(self.visit)

def usage():
	print("Usage:\npython3 graphs.py filename")
	sys.exit()

""" Checks the arguments, creates a Graphs object then runs color_graph()"""

def main():
	if len(sys.argv) != 2:
		usage()
	g = Graphs(sys.argv[1])
	g.color_graph()

if __name__ == '__main__':
	main()