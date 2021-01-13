import json

import matplotlib.pyplot as plt
import numpy

from scripts.produce_expected_json import PATH_EXPECTED, KEY_RESULT, KEY_TEST_TYPE_SHORTEST_PATH, KEY_RUN_TIME, \
    KEY_TEST_TYPE_LOAD
from scripts.produce_results_networkx import PATH_RESULTS_NETWORKX
from scripts.produce_results_python import PATH_RESULTS_PYTHON

PATH_RESULTS_JAVA = '../data/results_java.json'
PATH_PLOTS = '../data/plots/'

IMPL_PYTHON = 'python'
IMPL_NETWORKX = 'networkx'
IMPL_JAVA = 'java'


def ensure_valid_data_and_produce_plots():
    with open(PATH_EXPECTED, 'r') as _:
        results_expected = json.loads(_.read())

    with open(PATH_RESULTS_JAVA, 'r') as _:
        results_java = json.loads(_.read())

    with open(PATH_RESULTS_PYTHON, 'r') as _:
        results_python = json.loads(_.read())

    with open(PATH_RESULTS_NETWORKX, 'r') as _:
        results_networkx = json.loads(_.read())

    for tested_graph_file, tests in results_expected.items():
        algos_tests = list(tests.keys())
        algos_tests.append(KEY_TEST_TYPE_LOAD)

        implementation_run_times = {}
        implementation_run_times[IMPL_PYTHON] = []
        implementation_run_times[IMPL_NETWORKX] = []
        implementation_run_times[IMPL_JAVA] = []


        # Iterate over test type and ensure validity and produce a plot for the specific graph.
        for test_type, test_info in tests.items():
            implementation_run_times[IMPL_PYTHON].append(results_python[tested_graph_file][test_type][KEY_RUN_TIME])
            implementation_run_times[IMPL_JAVA].append(results_java[tested_graph_file][test_type][KEY_RUN_TIME])

            if test_type == KEY_TEST_TYPE_SHORTEST_PATH:
                # Index [1] is set for path testing only
                assert results_java[tested_graph_file][test_type][KEY_RESULT] == \
                       results_python[tested_graph_file][test_type][KEY_RESULT][1]

                assert results_networkx[tested_graph_file][test_type][KEY_RESULT][1] == \
                       results_python[tested_graph_file][test_type][KEY_RESULT][1]

                implementation_run_times[IMPL_NETWORKX].append(
                    results_networkx[tested_graph_file][test_type][KEY_RUN_TIME])
            else:
                assert results_java[tested_graph_file][test_type][KEY_RESULT] == \
                       results_python[tested_graph_file][test_type][KEY_RESULT]
                implementation_run_times[IMPL_NETWORKX].append(0)



        # Add graph loading times manually as they are not part of the expected json.
        implementation_run_times[IMPL_PYTHON].append(
            results_python[tested_graph_file][KEY_TEST_TYPE_LOAD][KEY_RUN_TIME])
        implementation_run_times[IMPL_JAVA].append(results_java[tested_graph_file][KEY_TEST_TYPE_LOAD][KEY_RUN_TIME])
        implementation_run_times[IMPL_NETWORKX].append(
            results_networkx[tested_graph_file][KEY_TEST_TYPE_LOAD][KEY_RUN_TIME])

        produce_plot(tested_graph_file + '.png', tested_graph_file + " - Lower is better", algos_tests,
                     implementation_run_times)


def produce_plot(png_fname, title, algorithms: list, impl_results: dict):
    print(impl_results)
    x = numpy.arange(len(algorithms))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    for impl, run_times in impl_results.items():
        ax.bar(x - width / len(impl_results), run_times, width, label=impl)

    ax.set_ylabel('Run time MS')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)
    ax.legend()
    fig.tight_layout()

    plt.gcf().set_size_inches(10, 8)

    plt.savefig("{}{}".format(PATH_PLOTS, png_fname), dpi=None, facecolor='w', edgecolor='w',
                orientation='portrait', format=None,
                transparent=False, bbox_inches=None, pad_inches=0.1, metadata=None)


if __name__ == "__main__":
    ensure_valid_data_and_produce_plots()
