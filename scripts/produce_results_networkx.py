import json
import time

import networkx as nx

from scripts.produce_expected_json import PATH_EXPECTED, COMP_DIR, KEY_RUN_TIME, KEY_TEST_TYPE_LOAD, KEY_CONF, \
    KEY_TEST_TYPE_SHORTEST_PATH, KEY_DEST, KEY_RESULT, KEY_SRC

PATH_RESULTS_NETWORKX = '../data/results_networkx.json'


def load_data_dict_to_network_x(data: dict):
    nxg = nx.DiGraph()
    for n in data.get('Nodes', []):
        nxg.add_node(n['id'])

    for e in data.get('Edges', []):
        nxg.add_edge(e['src'], e['dest'], weight=e['w'])

    return nxg


def produce_networkx_results():
    with open(PATH_EXPECTED, 'r') as f:
        expected_data = json.loads(f.read())

    results = {}

    for f, tests in expected_data.items():
        start = time.time()
        with open('{}{}'.format(COMP_DIR, f), 'r') as _:
            nxg = load_data_dict_to_network_x(json.loads(_.read()))
        end = time.time()

        f_results = {KEY_TEST_TYPE_LOAD: {KEY_RUN_TIME: (end - start) * 1000}}

        for test_type, test_info in tests.items():
            t_result = {}
            t_result[KEY_CONF] = test_info[KEY_CONF]

            if test_type == KEY_TEST_TYPE_SHORTEST_PATH:
                src = test_info[KEY_CONF][KEY_SRC]
                dest = test_info[KEY_CONF][KEY_DEST]
                start = time.time()
                t_result[KEY_RESULT] = list(nx.single_source_dijkstra(nxg, src, dest, weight="weight"))
                end = time.time()
                t_result[KEY_RUN_TIME] = (end - start) * 1000

            f_results[test_type] = t_result

        results[f] = f_results

    with open(PATH_RESULTS_NETWORKX, 'w') as f:
        f.write(json.dumps(results))


if __name__ == "__main__":
    produce_networkx_results()
