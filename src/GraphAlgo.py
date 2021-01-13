import json
import math
import sys
import traceback
from heapq import heappush, heappop
from typing import List, Dict

from DiGraph import DiGraph
from GraphAlgoInterface import GraphAlgoInterface
from Node import Node
from location.GeoLocation import GeoLocation
from location.Range import Range
from location.Range2D import Range2D
from src import GraphInterface
import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):
    __STATUS_NODE_NOT_VISITED = 0
    __STATUS_NODE_VISITED = 1
    __STATUS_NODE_QUEUED = 2

    __NUM_NODES_IN_CIRCLE = 25
    __MULTIPLIER_DIST_X = 1.1
    __MULTIPLIER_DIST_Y = 1.1
    __NUM_NODES_IN_X_AXIS = 10
    __RADIUS_EPS_DIVIDER = 2
    __SEARCH_RADIUS_MULTIPLIER = 1.5
    __RAD_ARC = 0.15
    __Z_ORDER = 99
    __COLOR_TEXT = 'midnightblue'
    __COLOR_BOX = 'yellow'
    __DEGREES = 360

    def __init__(self, g: GraphInterface = None):
        self.__g: DiGraph = g
        sys.setrecursionlimit(99999999)

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.__g

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        try:
            with open(file_name, 'r') as f:
                data = json.loads(f.read())
            self.__g = DiGraph.from_dict(data)
            return True
        except:
            traceback.print_exc()
            return False

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            with open(file_name, 'w') as f:
                f.write(json.dumps(self.get_graph().to_dict()))
            return True
        except:
            traceback.print_exc()
        return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through

        Example:
#      >>> from GraphAlgo import GraphAlgo
#       >>> g_algo = GraphAlgo()
#        >>> g_algo.addNode(0)
#        >>> g_algo.addNode(1)
#        >>> g_algo.addNode(2)
#        >>> g_algo.addEdge(0,1,1)
#        >>> g_algo.addEdge(1,2,4)
#        >>> g_algo.shortestPath(0,1)
#        (1, [0, 1])
#        >>> g_algo.shortestPath(0,2)
#        (5, [0, 1, 2])

        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """

        for n in self.get_graph().get_all_v().values():
            n.tag = self.__STATUS_NODE_NOT_VISITED

        src = id1
        dest = id2

        distances: Dict[int, float] = {}
        pq: [Node] = []
        visited_nodes: [Node] = []

        actual_distance = float(('inf'))
        actual_path = []

        heappush(pq, (0.0, self.get_graph().get_all_v().get(src)))
        distances[src] = 0.0

        needed_node: Node = None

        while (len(pq) > 0):
            node_distance, node = heappop(pq)
            visited_nodes.append(node) # Save node for cleaning up

            node.tag = self.__STATUS_NODE_VISITED
            needed_node = node if node.key == dest else needed_node

            # Traverse neighbours
            for neighbour_id, weight in self.get_graph().all_out_edges_of_node(node.key).items():
                neighbour: Node = self.get_graph().get_all_v().get(neighbour_id)
                if neighbour.tag == self.__STATUS_NODE_VISITED:
                    continue

                new_neighbour_distance = distances.get(node.key) + weight

                # Found a shorter distance, update the map.
                if new_neighbour_distance < distances.get(neighbour_id, float("inf")):
                    distances[neighbour_id] = new_neighbour_distance
                    heappush(pq, (new_neighbour_distance, neighbour))
                    neighbour.tag = self.__STATUS_NODE_QUEUED
                    neighbour.info = "{}".format(node.key)

        if needed_node:
            actual_distance = distances.get(dest)
            actual_path = self.__backtrack_path(src, needed_node)

        # Restore previous state.
        for n in visited_nodes:
            n.tag = self.__STATUS_NODE_NOT_VISITED

        return (actual_distance, actual_path)

    def __backtrack_path(self, src: int, needed_node: Node) -> List[Node]:
        '''
        Produce a path after path building is done.
        :param src: From node.
        :param needed_node: To node.
        :return: list of node ids.
        '''
        path: List[Node] = []

        backtracking_node: Node = needed_node
        while backtracking_node.key != src:
            path.insert(0, backtracking_node.key)
            if backtracking_node.info:
                backtracking_node = self.get_graph().get_all_v().get(int(backtracking_node.info))
        path.insert(0, backtracking_node.key)

        return path

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC

        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """

        res = self.__tarjan(self.get_graph().get_all_v().get(id1))
        for scc in res:
            if id1 in scc:
                return scc
        return []

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC

        Notes:
        If the graph is None the function should return an empty list []
        """
        res = self.__tarjan()
        self.__set_all_nodes_unvisited()
        return res

    def __set_all_nodes_unvisited(self):
        for n in self.get_graph().get_all_v().values():
            n.tag = self.__STATUS_NODE_NOT_VISITED

    def __tarjan(self, node: Node = None):
        components: list = []
        node_id_to_lowlink: dict = {}
        seen_stack: list = []

        self.__counter_lowlink: int = 0

        run_on_nodes = [node] if node else self.get_graph().get_all_v().values()

        for n in run_on_nodes:
            if n.tag == self.__STATUS_NODE_NOT_VISITED:
                self.__tarjan_DFS(node=n,
                                  components=components,
                                  node_id_to_lowlink=node_id_to_lowlink,
                                  seen_stack=seen_stack)

        return components

    def __next_lowlink_val(self) -> int:
        '''
        Incr next lowlink val.
        :return:
        '''
        res = self.__counter_lowlink
        self.__counter_lowlink += 1
        return res

    def __tarjan_DFS(self, node: Node, components: list, node_id_to_lowlink: dict,
                     seen_stack: list):
        node.tag = self.__STATUS_NODE_VISITED
        seen_stack.append(node.key)
        node_id_to_lowlink[node.key] = self.__next_lowlink_val()

        is_root: bool = True

        for neighbour_id, weight in self.get_graph().all_out_edges_of_node(node.key).items():
            neighbour: Node = self.get_graph().get_all_v().get(neighbour_id)

            # Traverse neighbours
            if neighbour.tag == self.__STATUS_NODE_NOT_VISITED:
                self.__tarjan_DFS(neighbour, components, node_id_to_lowlink, seen_stack)

            # Check lowlink
            my_low_link = node_id_to_lowlink.get(node.key)
            neighbour_low_link = node_id_to_lowlink.get(neighbour_id)

            if neighbour_id in seen_stack and neighbour_low_link < my_low_link:
                node_id_to_lowlink[node.key] = neighbour_low_link
                is_root = False

        if is_root:
            scc = []
            while True:
                node_id = seen_stack.pop()
                scc.append(node_id)
                node_id_to_lowlink[node_id] = node_id_to_lowlink[node.key]
                if node_id == node.key:
                    break

            scc.reverse()
            components.append(scc)

    def set_missing_positions(self):
        '''
        Set missing positions for node by a growing spiral and radius. Takes into account if other node are place in
        the radius too.
        :return: None
        '''
        nodes = self.get_graph().get_all_v()
        self.__set_all_nodes_unvisited()

        sccs_positioned = 0
        initial_world_range = self.__get_current_world_range()
        spiral_scc_factor = 1

        for scc in self.connected_components():

            starting_location: GeoLocation = initial_world_range.from_ratio(
                GeoLocation(self.__MULTIPLIER_DIST_X * spiral_scc_factor, 0, 0))

            if sccs_positioned % 3 == 0:
                starting_location: GeoLocation = initial_world_range.from_ratio(
                    GeoLocation(self.__MULTIPLIER_DIST_X * spiral_scc_factor,
                                self.__MULTIPLIER_DIST_Y * spiral_scc_factor, 0))

                spiral_scc_factor += 0.5
            elif sccs_positioned % 3 == 1:
                starting_location: GeoLocation = initial_world_range.from_ratio(
                    GeoLocation(0, self.__MULTIPLIER_DIST_Y * spiral_scc_factor, 0))

            sccs_positioned += 1

            for node_id in scc:
                node: Node = nodes.get(node_id)
                self.__position_neighbours(node, starting_location, initial_world_range)

    def __is_position_free(self, geo, neigh: Node, init_r: float):
        '''
        Check if position is ok for node to be place in.
        :param geo: GeoLocation point.
        :param neigh: Node.
        :param init_r: Initial radius.
        :return: True if ok else False.
        '''
        for n in self.get_graph().get_all_v().values():
            if n.geo_location:
                if geo.distance(n.geo_location) <= init_r / self.__RADIUS_EPS_DIVIDER:
                    return False
        return True

    def __position_neighbours(self, node: Node, starting_point: GeoLocation, initial_world_range: Range2D, angle=0):
        '''
        Position neighbours by finding them a free location in a growing circle.
        :param node: Starting node.
        :param starting_point:  Starting GeoLocation.
        :param initial_world_range: Initial x a y ranges for world.
        :param angle: Starting angle.
        :return: None
        '''
        if node.tag == self.__STATUS_NODE_NOT_VISITED:
            node.tag = self.__STATUS_NODE_VISITED

            if not node.geo_location:
                node.geo_location = starting_point

            actual_angle = angle
            for neighbour_id in self.get_graph().all_out_edges_of_node(node.key).keys():
                init_r = initial_world_range.x_range.length / self.__NUM_NODES_IN_X_AXIS
                r = init_r
                neigh = self.get_graph().get_all_v().get(neighbour_id)

                if not neigh.geo_location:
                    new_location_found = False

                    while not new_location_found:
                        for i in range(1, self.__NUM_NODES_IN_CIRCLE+1):
                            actual_angle = angle + self.__DEGREES / self.__NUM_NODES_IN_CIRCLE * i
                            actual_angle = actual_angle % self.__DEGREES

                            newx = node.geo_location.x + r * math.cos(actual_angle)
                            newy = node.geo_location.y + r * math.sin(actual_angle)

                            new_location = GeoLocation(newx, newy, 0)
                            if self.__is_position_free(new_location, neigh, init_r):
                                neigh.geo_location = new_location
                                new_location_found = True
                                break
                        r = r * self.__SEARCH_RADIUS_MULTIPLIER
                    self.__position_neighbours(neigh, neigh.geo_location, initial_world_range, actual_angle)

    def __get_current_world_range(self) -> Range2D:
        min_x = None
        max_x = None
        min_y = None
        max_y = None

        for node in self.get_graph().get_all_v().values():
            if node.geo_location:
                if min_x is None:
                    min_x = node.geo_location.x
                    max_x = min_x
                    min_y = node.geo_location.y
                    max_y = min_y
                else:
                    if node.geo_location.x < min_x:
                        min_x = node.geo_location.x
                    if node.geo_location.x > max_x:
                        max_x = node.geo_location.x

                    if node.geo_location.y < min_y:
                        min_y = node.geo_location.y
                    if node.geo_location.y > max_y:
                        max_y = node.geo_location.y

        if min_x is None:
            min_x = 0
            max_x = 1
            min_y = 0
            max_y = 1

        if min_x == max_x:
            min_x = 0 if min_x >= 0 else min_x
            max_x = 0 if max_x <= 0 else max_x

        if min_y == max_y:
            min_y = 0 if min_y >= 0 else min_y
            max_y = 0 if max_y <= 0 else max_y

        return Range2D(Range(min_x, max_x), Range(min_y, max_y))

    def plot_graph(self) -> None:
        self.set_missing_positions()
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """

        xs = []
        ys = []

        nodes = self.get_graph().get_all_v()

        for n in nodes.values():
            if not n.geo_location:
                continue

            xs.append(n.geo_location.x)
            ys.append(n.geo_location.y)

            plt.text(n.geo_location.x, n.geo_location.y, n.key,
                     va='top',
                     ha='right',
                     color=self.__COLOR_TEXT,
                     fontsize=9,
                     bbox=dict(boxstyle='square, pad=0.2', ec='gray', fc=self.__COLOR_BOX, alpha=0.65),
                     zorder=self.__Z_ORDER)

            for connected_node_id in self.get_graph().all_out_edges_of_node(n.key):
                connected_node = nodes.get(connected_node_id)

                if not connected_node.geo_location:
                    continue

                x = n.geo_location.x
                y = n.geo_location.y
                plt.annotate("",
                             xy=(connected_node.geo_location.x, connected_node.geo_location.y),
                             xycoords='data',
                             xytext=(x, y),
                             textcoords='data',
                             arrowprops=dict(arrowstyle="->",color='midnightblue',
                                             connectionstyle="arc3,rad={}".format(self.__RAD_ARC)),
                             )

        plt.scatter(xs, ys, color='gray')
        plt.draw()
        plt.show()
