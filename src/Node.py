from LinkAttributes import LinkAttributes
from location.GeoLocation import GeoLocation


class Node(object):
    __node_counter: int = 0

    def __init__(self, key: int = None, geo: GeoLocation = None):
        self.key: int = key if key is not None else self.__get_next_node_id()
        self.info: str = ""
        self.tag: int = 0
        self.weight: int = 0
        self._geo_location: GeoLocation = geo
        self.__links = None

        pass

    @classmethod
    def __get_next_node_id(cls) -> int:
        ret = cls.__node_counter
        cls.__node_counter += 1
        return ret

    @classmethod
    def from_dict(cls, data: dict) -> 'Node':
        '''
        Creates an instnace from dict. Supports optional fields and two similar json. (Java and Ariel).
        :param data: Data dict
        :return: Node
        '''

        if 'id' not in data and 'key' not in data:
            raise ValueError("Must at least have id or key in data dict.")

        # Ugly but this supports the million types of jsons that were produced..
        # :( Next time better have a unified Serializer/Deserializer for this.

        node_id = data.get('id')
        node_id = data.get('key') if node_id is None else node_id
        node_id = int(node_id)

        pos = data.get('pos')
        pos = data.get('geoLocation') if pos is None else pos

        if isinstance(pos, dict):
            if {"x", "y", "z"} - pos.keys():
                raise ValueError("Malformed geo location.")
            pos = "{},{},{}".format(pos['x'], pos['y'], pos['z'])

        if pos:
            pos = GeoLocation(*pos.split(','))

        weight = data.get("weight")
        tag = data.get("tag")
        info = data.get("info")

        n = Node(node_id, pos)

        # Load optional fields
        n.weight = weight if weight is not None else n.weight
        n.tag = tag if tag is not None else n.tag
        n.info = info if info is not None else n.info

        return n

    def to_dict(self) -> dict:
        res = {'key': self.key,
               'weight': self.weight,
               'info': self.info,
               'tag': self.tag}

        if self.geo_location:
            res.update({'geoLocation': {'x': self.geo_location.x,
                                        'y': self.geo_location.y,
                                        'z': self.geo_location.z}})

        return res

    @property
    def geo_location(self):
        return self._geo_location

    @geo_location.setter
    def geo_location(self, geo: GeoLocation):
        if not isinstance(geo, GeoLocation):
            raise ValueError("{} must be of type {}".format(type(geo), GeoLocation))
        self._geo_location = geo

    '''
    Not thread safe.
    '''
    def set_links_dict(self, links: dict):
        if LinkAttributes.ATTR_LINKS_IN not in links or LinkAttributes.ATTR_LINKS_OUT not in links:
            raise ValueError("links dict malformed.")
        self.__links = links

    def __repr__(self):
        return "{}: |edges out| {} |edges in| {}".format(self.key,
                                                         len(self.__links.get(LinkAttributes.ATTR_LINKS_OUT)),
                                                         len(self.__links.get(LinkAttributes.ATTR_LINKS_IN)))
