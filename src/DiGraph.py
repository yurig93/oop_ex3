from typing import Dict, List

from Edge import Edge
from GraphInterface import GraphInterface
from LinkAttributes import LinkAttributes
from Node import Node
from location.GeoLocation import GeoLocation


class DiGraph(GraphInterface):
    def __init__(self):
        self.__mode_count = 0
        self.__nodes: Dict[int, Node] = {}

        # {<node_id>: {'LINKS_OUT': {<other_id>: Edge}, 'LINKS_IN': {<other_id>: Edge}}}
        self.__links: Dict[int, Dict[str, Dict[int, Edge]]] = {}
        self.__edge_count: int = 0

    @classmethod
    def from_dict(cls, data) -> GraphInterface:
        g = cls()

        nodes = data.get("nodes") or data.get("Nodes")
        edges = data.get("links") or data.get("Edges")

        if nodes is None or edges is None:
            raise ValueError("Malformed JSON.")

        nodes = nodes.values() if isinstance(nodes, dict) else nodes
        for node in nodes:
            n = Node.from_dict(node)
            g.__add_node_by_instance(n)

        # if of type links (our data structure)
        if 'links' in data:
            actual_edges: List[dict] = []
            for l in edges.values():
                actual_edges += l.values()
            edges = actual_edges

        for e in edges:
            new_edge = Edge.from_dict(e)
            g.__add_edge_by_instance(new_edge)

        mode_count = data.get('modeCount')
        if mode_count is not None:
            g.__set_mode_count(mode_count)

        return g

    def to_dict(self) -> dict:
        res = {'modeCount': self.get_mc(),
               'edgeCount': self.e_size(),
               'links': {},
               'nodes': {}}

        for node in self.__nodes.values():
            res['nodes'][node.key] = node.to_dict()

        for node_id in self.__links:
            link_info = {}
            out_links = self.__links[node_id][LinkAttributes.ATTR_LINKS_OUT]
            for other_node_id, edge in out_links.items():
                link_info[other_node_id] = edge.to_dict()
            res['links'][node_id] = link_info

        return res

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return len(self.__nodes)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return self.__edge_count

    def get_all_v(self) -> Dict[int, Node]:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return self.__nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        return {connected_node_id: v.weight for connected_node_id, v in
                self.__links.get(id1).get(LinkAttributes.ATTR_LINKS_IN).items()}

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        return {connected_node_id: v.weight for connected_node_id, v in
                self.__links.get(id1).get(LinkAttributes.ATTR_LINKS_OUT).items()}

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.__mode_count

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.

        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """

        if (id1 != id2 and id1 in self.__nodes and id2 in self.__nodes
                and id2 not in self.__links.get(id1).get(LinkAttributes.ATTR_LINKS_OUT)):
            e = Edge(src=id1, dest=id2, weight=weight)

            self.__links.get(id1).get(LinkAttributes.ATTR_LINKS_OUT)[id2] = e
            self.__links.get(id2).get(LinkAttributes.ATTR_LINKS_IN)[id1] = e
            self.__mode_count += 1
            self.__edge_count += 1
            return True
        return False

    def __add_node_by_instance(self, node: Node):
        self.add_node(node.key)
        self.__nodes[node.key] = node
        node.set_links_dict(self.__links.get(node.key))

    def __add_edge_by_instance(self, edge: Edge):
        self.add_edge(edge.src, edge.dest, edge.weight)
        self.__links.get(edge.src).get(LinkAttributes.ATTR_LINKS_OUT)[edge.dest] = edge
        self.__links.get(edge.dest).get(LinkAttributes.ATTR_LINKS_IN)[edge.src] = edge

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.

        Note: if the node id already exists the node will not be added
        """

        if node_id not in self.__nodes:
            geo = GeoLocation(*pos) if pos is not None else None
            node = Node(node_id, geo)
            self.__nodes[node_id] = node

            links_container: Dict[str, Dict[int, Edge]] = {LinkAttributes.ATTR_LINKS_OUT: {},
                                                           LinkAttributes.ATTR_LINKS_IN: {}}
            self.__links[node_id] = links_container
            node.set_links_dict(links_container)
            self.__mode_count += 1

            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.

        Note: if the node id does not exists the function will do nothing
        """

        if node_id in self.__nodes:
            for other_node_id in self.__links.get(node_id).get(LinkAttributes.ATTR_LINKS_OUT).keys():
                self.remove_edge(node_id, other_node_id)

            del self.__links[node_id]
            del self.__nodes[node_id]
            return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.

        Note: If such an edge does not exists the function will do nothing
        """
        if node_id1 in self.__links and node_id2 in self.__links.get(node_id1).get(LinkAttributes.ATTR_LINKS_OUT):
            del self.__links.get(node_id1).get(LinkAttributes.ATTR_LINKS_OUT)[node_id2]
            del self.__links.get(node_id2).get(LinkAttributes.ATTR_LINKS_IN)[node_id1]
            self.__mode_count += 1
            self.__edge_count -= 1
            return True
        return False

    def __set_mode_count(self, mode_count: int):
        self.__mode_count = mode_count

    def __repr__(self) -> str:
        return "Graph: |V|={} , |E|={}".format(self.v_size(), self.e_size())
