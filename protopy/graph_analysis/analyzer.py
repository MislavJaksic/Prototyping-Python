import sys
import networkx


def read_graph_edges(filename):
    return networkx.read_edgelist(filename)


def get_graph_descendants_at_distance(graph, vertex, distance):
    descendants = list(networkx.descendants_at_distance(graph, vertex, distance))
    descendants.sort()
    return descendants


def get_graph_descendants_up_to_distance(graph, vertex, max_distance):
    list = []
    for distance in range(max_distance + 1):
        descendants = get_graph_descendants_at_distance(graph, vertex, distance)
        list.extend(descendants)
    list.sort()
    return list


def print_graph(graph):
    print("V:{}".format(graph.number_of_nodes()))
    print("E:{}".format(graph.number_of_edges()))


def fun():
    graph = read_graph_edges("protopy/graph_analysis/data/null-jumps.csv")
    with open("output.csv", "w") as output:
        with open("protopy/graph_analysis/data/arc-jove-null-jumps.csv", "r") as joves:
            for jove in joves:
                vertex = str(jove.strip())
                descendants = get_graph_descendants_up_to_distance(graph, vertex, 5)

                output.write(",".join([vertex] + descendants) + "\n")


def main(args):
    """main() will be run if you run this script directly"""
    fun()


def run():
    """Entry point for the runnable script."""
    sys.exit(main(sys.argv[1:]))


if __name__ == "__main__":
    """main calls run()."""
    run()
