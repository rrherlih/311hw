 #!/usr/bin/env python3

import sys

class Graphs:

	def __init__(self, graph):
		self.graph = graph

	def open_file(self, filename):
		try:
			return(open(filename))
		except:
			print("Error opening the graph.")
			sys.exit()

	def create_adj_list(self):
		self.fd = self.open_file(self.graph)
		num = int(self.fd.readline())
		adj_list = [num]
		for i in range(1, num + 1):
			adj_list.append(Vertex())

		while True:
			line = self.fd.readline().strip()
			if not line:
				break
			else:
				edge = self.edge_to_tuple(line)
				adj_list[edge[0]].add_adj(edge[1])
				adj_list[edge[1]].add_adj(edge[0])
		return(adj_list)

	def bfs(self, vertex, adj_list):
		q = Queue()
		q.enqueue(vertex)
		adj_list[vertex].set_color(1)
		adj_list[vertex].set_visit(1)

		while q.is_empty() == False:
			u = q.get_front()
			c = adj_list[u].get_color()
			for v in adj_list[u].get_adjs():
				
				if adj_list[v].get_visit() == 0:
					adj_list[v].set_parent(u)	
					print(v, u)
					adj_list[v].set_visit(1)
					if c == 1:
						adj_list[v].set_color(0)
					if c == 0:
						adj_list[v].set_color(1)
					q.enqueue(v)	
				if adj_list[v].get_visit() == 1:
					if c == 1:
						if adj_list[v].get_color() == 1:
							print("Not two-colorable")
							print(self.odd_cycle(u, v, adj_list))
							sys.exit()

					if c == 0:
						if adj_list[v].get_color() == 0:
							print("Not two-colorable")
							print(self.odd_cycle(u, v, adj_list))
							sys.exit()			
					
			q.dequeue()
			adj_list[u].set_visit(2)

		return(adj_list)

	def odd_cycle(self, u, v, adj_list):
		cycle = [u, v]
		while True:
			p1 = adj_list[u].get_parent()
			p2 = adj_list[v].get_parent()
			if p1 == p2:
				cycle = [p1] + cycle
				return(cycle)
			else:
				cycle = [p1] + cycle
				cycle = cycle + [p2]			
				u = adj_list[p1].get_parent()
				v = adj_list[p2].get_parent()
				cycle = [u] + cycle
				cycle.append(v)
	
	def color_graph(self):
		a = self.create_adj_list()
		s = 1
		while True:
			adj_list = self.bfs(s, a)
			a = adj_list
			s = self.disconnect_check(adj_list)
			if s == 0:
				break

		print("This graph is two-colorable")

		target = open('graph-colored', 'w')
		target2 = open('graph-adj', 'w')
		for i in range(1, len(adj_list)):
			target.write("{} {}\n".format(i, adj_list[i].get_color()))
		for i in range(1, len(adj_list)):
			target2.write("{} {}\n".format(i, adj_list[i].get_adjs()))

	def edge_to_tuple(self, edge):
		l = edge.split()
		v1 = int(l[0])
		v2 = int(l[1])
		if v1 < v2:
			return(v1, v2)
		else:
			return(v2, v1)

	def disconnect_check(self, adj_list):
		for i in range(1, len(adj_list)):
			if adj_list[i].get_color() == -1:
				return(i)
		return(0)
	
class Queue:

	def __init__(self):
		self.front = None
		self.back = None
		self.size = 0

	def enqueue(self, v):
		self.size += 1
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
		self.size -= 1
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

	def get_size(self):
		return(self.size)

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

def main():
	g = Graphs(sys.argv[1])
	g.color_graph()

if __name__ == '__main__':
	main()