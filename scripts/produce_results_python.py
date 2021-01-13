import json
import time

from GraphAlgo import GraphAlgo
from scripts.produce_expected_json import PATH_EXPECTED, COMP_DIR, KEY_TEST_TYPE_SHORTEST_PATH, KEY_DEST, KEY_CONF, \
    KEY_SRC, KEY_RESULT, KEY_TEST_TYPE_CONNECTED_COMPONENTS, KEY_RUN_TIME, KEY_TEST_TYPE_CONNECTED_COMPONENT, \
    KEY_NODE_ID, KEY_TEST_TYPE_LOAD

PATH_RESULTS_PYTHON = '../data/results_python.json'


def produce_python_results():
    with open(PATH_EXPECTED, 'r') as f:
        expected_data = json.loads(f.read())

    results = {}

    for f, tests in expected_data.items():
        algo = GraphAlgo()
        start = time.time()
        algo.load_from_json('{}{}'.format(COMP_DIR, f))
        end = time.time()

        f_results = {KEY_TEST_TYPE_LOAD: {KEY_RUN_TIME: (end - start) * 1000}}

        for test_type, test_info in tests.items():
            t_result = {}
            t_result[KEY_CONF] = test_info[KEY_CONF]

            if test_type == KEY_TEST_TYPE_SHORTEST_PATH:
                src = test_info[KEY_CONF][KEY_SRC]
                dest = test_info[KEY_CONF][KEY_DEST]
                start = time.time()
                t_result[KEY_RESULT] = algo.shortest_path(src, dest)
                end = time.time()
                t_result[KEY_RUN_TIME] = (end - start) * 1000

            if test_type == KEY_TEST_TYPE_CONNECTED_COMPONENTS:
                start = time.time()
                t_result[KEY_RESULT] = algo.connected_components()
                end = time.time()
                t_result[KEY_RUN_TIME] = (end - start) * 1000

            if test_type == KEY_TEST_TYPE_CONNECTED_COMPONENT:
                node_id = test_info[KEY_CONF][KEY_NODE_ID]
                start = time.time()
                t_result[KEY_RESULT] = algo.connected_component(node_id)
                end = time.time()
                t_result[KEY_RUN_TIME] = (end - start) * 1000

            f_results[test_type] = t_result

        results[f] = f_results

    with open(PATH_RESULTS_PYTHON, 'w') as f:
        f.write(json.dumps(results))


if __name__ == "__main__":
    produce_python_results()
