from unittest import TestCase

from DiGraph import DiGraph
from Node import Node


class TestDiGraph(TestCase):
    def test_from_dict(self):
        data = {"modeCount": 9, "edgeCount": 5,
                "links": {"0": {"1": {"src": 0, "dest": 1, "weight": 1, "info": "", "tag": -1}},
                          "1": {"0": {"src": 1, "dest": 0, "weight": 1.1, "info": "", "tag": -1},
                                "2": {"src": 1, "dest": 2, "weight": 1.3, "info": "", "tag": -1},
                                "3": {"src": 1, "dest": 3, "weight": 1.8, "info": "", "tag": -1}},
                          "2": {"3": {"src": 2, "dest": 3, "weight": 1.1, "info": "", "tag": -1}},
                          "3": {}},
                "nodes": {"0": {"key": 0, "weight": 0, "info": "", "tag": 0},
                          "1": {"key": 1, "weight": 0, "info": "0", "tag": 0},
                          "2": {"key": 2, "weight": 0, "info": "1", "tag": 0},
                          "3": {"key": 3, "weight": 0, "info": "1", "tag": 0}}}

        g = DiGraph.from_dict(data)
        self.assertEqual(g.e_size(), data['edgeCount'])
        self.assertEqual(g.get_mc(), data['modeCount'])
        self.assertEqual(len(g.get_all_v()), len(data['nodes']))

        node: Node = g.get_all_v().get(1)
        self.assertEqual(node.info, "0")
        self.assertEqual(len(g.all_out_edges_of_node(1)), 3)

    def test_to_dict(self):
        g = DiGraph()
        g.add_node(1, (1, 2, 3))
        g.add_node(2, (3, 2, 1))
        g.add_edge(1, 2, 4)
        data = g.to_dict()

        self.assertEqual(3, data.get('modeCount'))
        self.assertEqual(1, data.get('edgeCount'))
        self.assertEqual(2, len(data.get('nodes')))
        self.assertEqual(4, data.get('links').get(1).get(2).get('weight'))

    def test_v_size(self):
        g = DiGraph()
        g.add_node(1, (1, 2, 3))
        g.add_node(2, (3, 2, 1))
        self.assertEqual(2, g.v_size())

    def test_e_size(self):
        g = DiGraph()
        g.add_node(1, (1, 2, 3))
        g.add_node(2, (3, 2, 1))
        g.add_edge(1, 2, 4)
        g.add_edge(2, 1, 4)
        self.assertEqual(2, g.e_size())

    def test_get_all_v(self):
        g = DiGraph()
        g.add_node(1, (1, 2, 3))
        self.assertTrue(1 in g.get_all_v())

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        g.add_node(1, (1, 2, 3))
        g.add_node(2, (3, 2, 1))
        g.add_edge(1, 2, 4)

        in_e = g.all_in_edges_of_node(2)

        self.assertEqual(len(in_e), 1)
        self.assertTrue(1 in in_e)

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        g.add_node(1, (1, 2, 3))
        g.add_node(2, (3, 2, 1))
        g.add_edge(1, 2, 4)

        out_e = g.all_out_edges_of_node(1)

        self.assertEqual(len(out_e), 1)
        self.assertTrue(2 in out_e)

    def test_get_mc(self):
        g = DiGraph()
        self.assertEqual(0, g.get_mc())

        g.add_node(1, (1, 2, 3))

        self.assertEqual(1, g.get_mc())

        g.add_node(1, (1, 2, 3))
        self.assertEqual(1, g.get_mc())

    def test_add_edge(self):
        g = DiGraph()

        g.add_node(1, (1, 2, 3))
        g.add_node(2, (1, 2, 3))

        added = g.add_edge(1, 2, 4)
        self.assertTrue(added)

        added = g.add_edge(1, 2, 4)
        self.assertFalse(added)

    def test_add_node(self):
        g = DiGraph()

        added = g.add_node(1, (1, 2, 3))
        self.assertTrue(added)
        added = g.add_node(1, (1, 2, 3))
        self.assertFalse(added)

    def test_remove_node(self):
        g = DiGraph()
        g.add_node(1, (1, 2, 3))
        removed = g.remove_node(1)
        self.assertTrue(removed)
        removed = g.remove_node(1)
        self.assertFalse(removed)

    def test_remove_edge(self):
        g = DiGraph()
        g.add_node(1, (1, 2, 3))
        g.add_node(2, (1, 2, 3))

        g.add_edge(1, 2, 5)
        removed = g.remove_edge(1, 2)
        self.assertTrue(removed)
        removed = g.remove_edge(1, 2)
        self.assertFalse(removed)
