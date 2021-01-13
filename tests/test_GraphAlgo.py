from unittest import TestCase

from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        g = DiGraph()
        algo = GraphAlgo()

        self.assertIsNone(algo.get_graph())
        algo = GraphAlgo(g)
        self.assertEqual(algo.get_graph(), g)


    def test_load_from_json(self):
        algo = GraphAlgo()
        loaded = algo.load_from_json("../data/A0")
        self.assertTrue(loaded)
        self.assertEqual(11, algo.get_graph().v_size())
        self.assertEqual(22, algo.get_graph().e_size())

    def test_save_to_json(self):
        algo = GraphAlgo()
        loaded = algo.load_from_json("../data/A0")
        saved = algo.save_to_json("../data/A0-dumped.json")

        self.assertTrue(saved)

        algo2 = GraphAlgo()
        algo2.load_from_json("../data/A0-dumped.json")

        self.assertEqual(algo.get_graph().v_size(), algo2.get_graph().v_size())
        self.assertEqual(algo.get_graph().e_size(), algo2.get_graph().e_size())

    def test_shortest_path(self):
        algo = GraphAlgo()
        loaded = algo.load_from_json("../data/A0")
        dist, path = algo.shortest_path(0, 7)
        self.assertEqual(dist, 5.653293226161572)
        self.assertEqual([0, 10, 9, 8, 7], path)

        dist, path = algo.shortest_path(0, 8888887)
        self.assertEqual(dist, float('inf'))
        self.assertEqual(path, [])


    def test_connected_component(self):
        new_id = 123123
        algo = GraphAlgo()
        loaded = algo.load_from_json("../data/A5")
        algo.get_graph().add_node(new_id)

        self.assertEqual(1, len(algo.connected_component(new_id)))
        self.assertEqual(48, len(algo.connected_component(1)))

    def test_connected_components(self):
        algo = GraphAlgo()
        loaded = algo.load_from_json("../data/A5")
        algo.get_graph().add_node(123123)

        sccs = algo.connected_components()
        self.assertEqual(len(sccs), 2)

    def test_set_missing_positions(self):
        algo = GraphAlgo()
        loaded = algo.load_from_json("../data/A5")
        algo.get_graph().add_node(123123)
        algo.get_graph().add_node(131313)
        algo.set_missing_positions()

        for n in algo.get_graph().get_all_v().values():
            self.assertIsNotNone(n.geo_location)
