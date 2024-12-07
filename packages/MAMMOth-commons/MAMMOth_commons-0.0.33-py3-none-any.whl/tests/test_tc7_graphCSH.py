from mammoth import testing
from mammoth.models.empty import EmptyModel
from catalogue.dataset_loaders.graph_from_csv import data_graph_csv
from catalogue.metrics.ma_graph_connection import connection_properties


def test_fair_graph_filtering():
    with testing.Env(data_graph_csv, connection_properties) as env:
        graph = env.data_graph_csv(
            path_nodes="./data/multisoc/nodes_dummy.csv",
            path_edges="./data/multisoc/edges_dummy.csv",
            attributes=["shape", "color", "number"],
        )

        model = EmptyModel()

        analysis_outcome = env.connection_properties(graph, model, [])
        analysis_outcome.show()


if __name__ == "__main__":
    test_fair_graph_filtering()
