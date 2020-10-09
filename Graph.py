class Graph:

    def __init__(self, number_of_vertices):
        self.Matrix = [[-1] * number_of_vertices for x in range(number_of_vertices)]
        self.number_of_vertices = number_of_vertices
        self.vertices = dict()
        self.verticeslist = [0] * number_of_vertices

    def set_vertex(self, vertex_index, vertex_name):
        if 0 <= vertex_index <= self.number_of_vertices:
            self.vertices[vertex_name] = vertex_index
            self.verticeslist[vertex_index] = vertex_name

    def set_edge(self, from_, to, cost=0):
        from_ = self.vertices[from_]
        to = self.vertices[to]
        self.Matrix[from_][to] = cost
        self.Matrix[to][from_] = cost

    def get_vertex(self):
        return self.verticeslist

    def get_edges(self):
        edges = []
        for i in range(self.number_of_vertices):
            for j in range(self.number_of_vertices):
                if self.Matrix[i][j] != -1:
                    edges.append((self.verticeslist[i], self.verticeslist[j], self.Matrix[i][j]))
        return edges

    def get_matrix(self):
        return self.Matrix


class ConnectedNode:
    def __init__(self, data):
        self.node = data
        self.next = None

class Graph2:

    def __init__(self, nodes):
        self.nodes = nodes
        self.graph = [None] * self.nodes

    def add_edge(self, source, destination):
        # Adding destination node to the source node
        node = ConnectedNode(destination)
        node.next = self.graph[source]
        self.graph[source] = node

        # Adding source node to the destination node (undirected graph)
        node = ConnectedNode(source)
        node.next = self.graph[destination]
        self.graph[destination] = node

        # Function to print the graph

    def print_graph(self):
        for i in range(self.nodes):
            print(f"Node {i}\n", end="")
            temp = self.graph[i]
            while temp:
                print(f" -> {temp.node}", end="")
                temp = temp.next
            print(" \n")
