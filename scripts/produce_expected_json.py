import json
import os
import random

from GraphAlgo import GraphAlgo
from Node import Node

COMP_DIR = '../data/comparison/'
PATH_EXPECTED = '../data/expected.json'

KEY_RUN_TIME = 'run_time'
KEY_TEST_TYPE_LOAD = 'load'
KEY_TEST_TYPE_SHORTEST_PATH = 'shortest_path'
KEY_TEST_TYPE_CONNECTED_COMPONENTS = 'connected_components'
KEY_TEST_TYPE_CONNECTED_COMPONENT = 'connected_component'
KEY_RESULT = 'result'
KEY_EXPECTED_RESULT = 'expected_result'
KEY_CONF = 'conf'
KEY_SRC = 'src'
KEY_DEST = 'dest'
KEY_NODE_ID = 'node_id'


def produce_expected_file() -> dict:
    '''
    Produces an expected.json file with randomly chosen nodes for each graph in the _COMP_DIR.
    For each tested algo it produces the results expected to be compared against Java impl and Networkx.
    :return: expected results dict
    '''
    data = {}

    for f in os.listdir(COMP_DIR):
        algo = GraphAlgo()
        algo.load_from_json('{}{}'.format(COMP_DIR, f))

        data[f] = {}

        # Not memory optimal
        nodes = list(algo.get_graph().get_all_v().values())

        first_node = random.choice(nodes)
        second_node: Node = None
        while second_node is None or second_node.key == first_node.key:
            second_node = random.choice(nodes)

        shortest_path = algo.shortest_path(first_node.key, second_node.key)

        data[f][KEY_TEST_TYPE_SHORTEST_PATH] = {KEY_CONF: {KEY_SRC: first_node.key,
                                                           KEY_DEST: second_node.key},
                                                KEY_EXPECTED_RESULT: shortest_path}

        data[f][KEY_TEST_TYPE_CONNECTED_COMPONENTS] = {KEY_CONF: None,
                                                       KEY_EXPECTED_RESULT: algo.connected_components()}

        data[f][KEY_TEST_TYPE_CONNECTED_COMPONENT] = {KEY_CONF: {KEY_NODE_ID: first_node.key},
                                                      KEY_EXPECTED_RESULT: algo.connected_component(first_node.key)}

    with open(PATH_EXPECTED, 'w') as f:
        f.write(json.dumps(data))

    return data


if __name__ == "__main__":
    produce_expected_file()
