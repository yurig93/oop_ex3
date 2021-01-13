from unittest import TestCase

from Node import Node
from location.GeoLocation import GeoLocation


class TestNode(TestCase):
    def test_from_dict_ok_vals(self):
        data = {'id': 1,
                'pos': "1.0,2.0,3.0",
                'weight': 123,
                "info": "amazinginfo",
                "tag": 4655}

        n = Node.from_dict(data)
        self.assertEqual(n.key, data.get('id'))
        self.assertEqual(str(n.geo_location), data.get('pos'))
        self.assertEqual(n.weight, data.get('weight'))
        self.assertEqual(n.info, data.get('info'))
        self.assertEqual(n.tag, data.get('tag'))

    def test_from_dict_default_vals(self):
        data = {'id': 1}

        n = Node.from_dict(data)
        self.assertEqual(n.key, data.get('id'))
        self.assertEqual(n.geo_location, None)
        self.assertEqual(n.weight, 0)
        self.assertEqual(n.info, "")
        self.assertEqual(n.tag, 0)

    def test_from_dict_throws_errors(self):
        data = {}

        with self.assertRaises(ValueError):
            n = Node.from_dict(data)

        data.update({'id': 123})
        Node.from_dict(data)

    def test_to_dict(self):
        n = Node(1, GeoLocation(1.0, 2.0, 3.0))
        n.weight = 111
        n.info = "wow"
        n.tag = 4655

        data = n.to_dict()
        self.assertEqual(data['key'], n.key)
        self.assertEqual(data['info'], n.info)
        self.assertEqual(data['tag'], n.tag)
        self.assertEqual(data['weight'], n.weight)
        self.assertEqual(data['geoLocation'], {'x': 1.0,
                                               'y': 2.0,
                                               'z': 3.0})
