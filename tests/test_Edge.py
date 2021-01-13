from unittest import TestCase

from Edge import Edge


class TestEdge(TestCase):
    def test_from_dict_ok_vals(self):
        data = {'src': 1,
                'dest': 2,
                'weight': 3,
                'info': "yuri",
                'tag': 4655}

        e = Edge.from_dict(data)

        self.assertEqual(e.src, data.get('src'))
        self.assertEqual(e.dest, data.get('dest'))
        self.assertEqual(e.weight, data.get('weight'))
        self.assertEqual(e.info, data.get('info'))
        self.assertEqual(e.tag, data.get('tag'))

    def test_from_dict_default_vals(self):
        data = {'src': 1,
                'dest': 2,
                'w': 3}

        e = Edge.from_dict(data)
        self.assertEqual(e.src, data.get('src'))
        self.assertEqual(e.dest, data.get('dest'))
        self.assertEqual(e.weight, data.get('w'))
        self.assertEqual(e.info, "")
        self.assertEqual(e.tag, Edge.INVALID_ENTRY)

    def test_from_dict_throws_errors(self):
        data = {}

        with self.assertRaises(ValueError):
            Edge.from_dict(data)

        data.update({'src': 1})

        with self.assertRaises(ValueError):
            Edge.from_dict(data)

        data.update({'dest': 1})

        with self.assertRaises(ValueError):
            Edge.from_dict(data)

        data.update({'weight': 1})

        Edge.from_dict(data)

    def test_to_dict(self):
        e = Edge(1, 2, 3, "info", 4655)
        data = e.to_dict()
        self.assertEqual(e.src, data.get('src'))
        self.assertEqual(e.dest, data.get('dest'))
        self.assertEqual(e.weight, data.get('weight'))
        self.assertEqual(e.info, data.get('info'))
        self.assertEqual(e.tag, data.get('tag'))
