# source: https://dev.to/mariamxl
# https://dev.to/mariamxl/dijkstras-algorithm-in-python-algorithms-for-beginners-dkc

from collections import deque, namedtuple


# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')


def make_edge(start, end, cost=1):
  return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))
        static_edges = [('map15', 'map16', 0), ('mp55', 'mp56', 0), ('mp56', 'mp55', 0), ('mpp98', 'out', 0),
                        ('mpp99', 'out', 0), ('map5', 'map6', 0), ('mp45', 'mp46', 0), ('mp46', 'mp45', 0),
                        ('mpp88', 'out', 0), ('mpp89', 'out', 0)]
        """static_edges = [('map15', 'map16', 0), ('mp55', 'mp56', 0), ('mp56', 'mp55', 0), ('mpp98', 'mpp99', 0),
                        ('mpp99', 'mpp98', 0), ('map5', 'map6', 0), ('mp45', 'mp46', 0), ('mp46', 'mp45', 0),
                        ('mpp88', 'mpp89', 0), ('mpp89', 'mpp88', 0), ('mpp1', 'out', 0), ('mpp2', 'out', 0),
                        ('mpp3', 'out', 0), ('mpp4', 'out', 0), ('mpp5', 'out', 0), ('mpp6', 'out', 0)]"""
        edges = edges + static_edges
        self.edges = [make_edge(*edge) for edge in edges]

    @property
    def vertices(self):
        return set(
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        
        try:
            path.pop()
            return list(path)
        except:
            return None
