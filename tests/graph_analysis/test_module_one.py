from tests import context

import pytest

from protopy.graph_analysis import analyzer


@pytest.fixture(scope="module")
def graph():
    edge_graph = analyzer.read_graph_edges("tests/graph_analysis/data/null-jumps.csv")
    yield edge_graph


class TestAtDistance:
    def test_get_graph_descendants_at_distance_0(self, graph):
        assert analyzer.get_graph_descendants_at_distance(graph, "30000219", 0) == [
            "30000219"
        ]

    def test_get_graph_descendants_at_distance_1(self, graph):
        assert analyzer.get_graph_descendants_at_distance(graph, "30000219", 1) == [
            "30000215",
            "30000216",
        ]

    def test_get_graph_descendants_at_distance_2(self, graph):
        assert analyzer.get_graph_descendants_at_distance(graph, "30000219", 2) == [
            "30000217",
            "30000221",
            "30000251",
        ]


class TestUpToDistance:
    def test_get_graph_descendants_up_to_distance_0(self, graph):
        assert analyzer.get_graph_descendants_up_to_distance(graph, "30000219", 0) == [
            "30000219"
        ]

    def test_get_graph_descendants_up_to_distance_1(self, graph):
        assert analyzer.get_graph_descendants_up_to_distance(graph, "30000219", 1) == [
            "30000215",
            "30000216",
            "30000219",
        ]

    def test_get_graph_descendants_up_to_distance_2(self, graph):
        assert analyzer.get_graph_descendants_up_to_distance(graph, "30000219", 2) == [
            "30000215",
            "30000216",
            "30000217",
            "30000219",
            "30000221",
            "30000251",
        ]
