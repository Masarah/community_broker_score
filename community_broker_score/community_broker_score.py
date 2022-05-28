import numpy as np
import pandas as pd
import networkx as nx


def determine_nodes_in_same_group(edges):
    if edges["community_id_A"] == edges["community_id_B"]:
        return 0
    else:
        return 1


def detect_brokering_edges(nodes, edges):
    """This function detects edges of two nodes in different communities.

    Parameters:
        - nodes : Dataframe with columns 'id' and 'community_id'.
        - edges : Dataframe with columns source 'A' and target 'B', undirected.

    Returns:
        - edges_only_community_bridge : Dataframe with only brokering edges
    """

    #  Get membership of A and membership of B for each pair of edges
    edges_A_with_cid = edges.merge(nodes, left_on="A", right_on="id", how="inner").drop(columns=["id"])
    edges_A_with_cid_renamed = edges_A_with_cid.rename(columns={"community_id": "community_id_A"})
    edges_B_with_cid = edges_A_with_cid_renamed.merge(nodes, left_on="B", right_on="id", how="inner").drop(
        columns=["id"]
    )
    edges_B_with_cid_renamed = edges_B_with_cid.rename(columns={"community_id": "community_id_B"})

    #  Rename edge dataframe
    edges_AB_with_cid = edges_B_with_cid_renamed

    #  Determine if the edge is a bridging edge or not
    edges_AB_with_cid["community_broker"] = edges_AB_with_cid.apply(determine_nodes_in_same_group, axis=1)

    #  Get all the community brokers (CB) from the pairs and tag them as community brokers (CB)
    edges_only_community_bridge = edges_AB_with_cid.loc[edges_AB_with_cid["community_broker"] == 1]

    return edges_only_community_bridge


def detect_community_brokers(nodes, edges):
    """This function detects community brokers and counts the number of times they hold this position in the network.

    Parameters:
        - nodes : Dataframe with columns 'id' and 'community_id'.
        - edges : Dataframe with columns source 'A' and target 'B', undirected.

    Returns:
        - nodes_with_characteristics : Node dataframe with 4 columns:
            - id
            - community_id
            - community_broker: Boolean, is a the node a broker.
            - n_community_broker: Int. The number of times a community broker bridges two communities.
    """

    #  Find ties that are bridges between two communities
    edges_only_community_bridge = detect_brokering_edges(nodes, edges)

    #  Get all the community brokers (CB) from the pairs and tag them as community brokers (CB)
    those_who_are_CB_in_A = edges_only_community_bridge[["A", "community_broker"]].rename(columns={"A": "id"})
    those_who_are_CB_in_B = edges_only_community_bridge[["B", "community_broker"]].rename(columns={"B": "id"})
    community_brokers_list = pd.concat([those_who_are_CB_in_A, those_who_are_CB_in_B]).drop_duplicates()

    #  Merge community_brokers_list with nodes dataframe and fill empty rows with 0 (for non-CB)
    nodes = nodes.merge(community_brokers_list, on="id", how="outer")
    nodes["community_broker"] = nodes["community_broker"].fillna(0)

    #  Same process as above but now groupby by count so as to have a count column (the number of time a CB is a CB)
    community_brokers_list_duplicates = pd.concat([those_who_are_CB_in_A, those_who_are_CB_in_B])
    community_brokers_list_count = (
        community_brokers_list_duplicates.groupby("id")
        .count()
        .reset_index()
        .rename(columns={"community_broker": "n_community_broker"})
    )

    #  Merge community_brokers_list_count with nodes dataframe and fill empty rows with 0 (for non-CB)
    nodes_with_characteristics = nodes.merge(community_brokers_list_count, on="id", how="outer")
    nodes_with_characteristics["n_community_broker"] = nodes_with_characteristics[
        "n_community_broker"
    ].fillna(0)

    #  Return nodes dataframe with community_broker and n_community_broker columns
    return nodes_with_characteristics


def find_community_characteristics(nodes, edges):
    """This function computes community characteristics required for the community broker score calculation

    Parameters:
        - nodes : Dataframe with columns 'id' and 'community_id'.
        - edges : Dataframe with columns source 'A' and target 'B', undirected.

    Returns:
        - communities : Community dataframe with each row a community and with columns:
            - community_id: id of the community
            - community_cohesion: integer representing average_shortest_path_length.
            - community_n_people: integer number of people in the community.
            - community_n_brokers: integer number of community brokers in each community.
    """
    nodes_with_characteristics = detect_community_brokers(nodes, edges)
    nodes_without_count_var = nodes_with_characteristics.drop(columns=["n_community_broker"])

    #  Extract the number of commmunity brokers and people for each community based on nodes dataframe
    group_nodes_per_community = (
        nodes_without_count_var.groupby("community_id")
        .agg({"id": "count", "community_broker": "sum"})
        .rename(columns={"id": "community_n_people"})
        .reset_index()
    )

    assert (
        group_nodes_per_community.community_n_people > 1
    ).all(), "Number of people in communities has to be larger than 1"

    #  Create a graph object and set community_id as nodes attributes
    graph = nx.from_pandas_edgelist(edges, source="A", target="B")
    extra_community_id_as_attribute = pd.Series(
        nodes_with_characteristics.community_id.values,
        index=nodes_with_characteristics.id,
    ).to_dict()
    nx.set_node_attributes(graph, extra_community_id_as_attribute, "community_id")

    #  Compute score for each community
    cohesion_score = []
    for each_community_id in nodes_with_characteristics.community_id.unique():
        nodes_per_community = nodes_with_characteristics.loc[
            nodes_with_characteristics["community_id"] == each_community_id
        ]
        graph_per_community = graph.subgraph(nodes_per_community.id)
        cohesion_per_community = nx.average_shortest_path_length(graph_per_community)
        extract_info_cohesion_score_per_community = {
            "community_id": each_community_id,
            "community_cohesion": cohesion_per_community,
        }
        cohesion_score.append(extract_info_cohesion_score_per_community)

    #  Merge to have a dataframe with communities information
    communities = (
        pd.DataFrame(cohesion_score)
        .merge(group_nodes_per_community, on="community_id", how="outer")
        .rename(columns={"community_broker": "community_n_brokers"})
    )

    return communities


def local_community_broker_score(nodes, edges):
    """This function calculates the community broker score for one network partition
    (thus the local community broker score)

    Parameters:
        - nodes : Dataframe with columns 'id' and 'community_id'.
        - edges : Dataframe with columns source 'A' and target 'B', undirected.

    Returns:
        - nodes_with_broker_score : Node dataframe with local community broker score.

    Note that the local community broker score is the score for one community structure.
    When the community-detection algorithm chosen yields different partitioning every time it is computed,
    to find the global score one has to compute the average of local scores over multiple possible network partitionings.

    """
    #  Recompute each prior functions
    edges_only_community_bridge = detect_brokering_edges(nodes, edges)
    nodes_with_characteristics = detect_community_brokers(nodes, edges)
    communities = find_community_characteristics(nodes, edges)

    #  Create inverse dataframe --the goal is to get a dataframe with id, community_id_A, community_id_B for each node
    edges_only_community_bridge_inversed = edges_only_community_bridge.rename(
        columns={
            "A": "B",
            "B": "A",
            "community_id_A": "community_id_B",
            "community_id_B": "community_id_A",
        }
    )

    #  Drop duplicates because sometimes one community broker bridges the same community many times
    all_broker_ties = pd.concat(
        [edges_only_community_bridge, edges_only_community_bridge_inversed]
    ).drop_duplicates()
    all_broker_ties_unique_in_one_column = all_broker_ties[
        ["A", "community_id_A", "community_id_B", "community_broker"]
    ].rename(columns={"A": "id"})

    #  Detect cobridgers for based on community source (A) towards community target (B) for each broker tie
    n_CB_A_towards_B = (
        all_broker_ties_unique_in_one_column.groupby(["community_id_A", "community_id_B"])
        .agg({"id": "count"})
        .rename(columns={"id": "n_cobrokers"})
        .reset_index()
    )

    #  Merge with all_broker_ties_unique_in_one_column to get info alltogether
    all_broker_ties_info = all_broker_ties_unique_in_one_column.merge(
        n_CB_A_towards_B, on=["community_id_A", "community_id_B"], how="outer"
    )

    #  Since we will merge info from cohesion dataframe, keep only interesting columns from the dataframe
    interesting_columns_communities = communities[
        ["community_id", "community_cohesion", "community_n_people"]
    ]

    #  Create large dataframe with all info to calculate local community broker score for each briding tie created
    info_community_A = (
        all_broker_ties_info.merge(
            interesting_columns_communities,
            left_on="community_id_A",
            right_on="community_id",
            how="outer",
        )
        .rename(
            columns={
                "community_cohesion": "community_cohesion_CA",
                "community_n_people": "community_n_people_CA",
            }
        )
        .drop("community_id", axis=1)
    )
    info_community_AB = (
        info_community_A.merge(
            interesting_columns_communities,
            left_on="community_id_B",
            right_on="community_id",
            how="outer",
        )
        .rename(
            columns={
                "community_cohesion": "community_cohesion_CB",
                "community_n_people": "community_n_people_CB",
            }
        )
        .drop("community_id", axis=1)
    )

    #  Calculate Score for community targeted (CB)
    info_community_AB_with_score_CB = info_community_AB.assign(
        score_CB=info_community_AB.community_n_people_CB
        / (info_community_AB.community_cohesion_CB * np.sqrt(info_community_AB.n_cobrokers))
    )
    info_community_AB_with_scores_CB_summed = info_community_AB_with_score_CB.groupby("id").agg(
        {
            "id": "first",
            "community_cohesion_CA": "first",
            "community_n_people_CA": "first",
            "score_CB": "sum",
        }
    )

    #  Calculate score for boker's own community
    info_community_AB_with_scores_CB_CA = info_community_AB_with_scores_CB_summed.assign(
        score_CA=info_community_AB_with_scores_CB_summed.community_n_people_CA
        / info_community_AB_with_scores_CB_summed.community_cohesion_CA
    )

    #  Calculate final score
    final_scores = info_community_AB_with_scores_CB_CA.assign(
        community_broker_score=(
            info_community_AB_with_scores_CB_CA.score_CB + info_community_AB_with_scores_CB_CA.score_CA
        )
    ).reset_index(drop=True)

    #  Merge final score with nodes dataframe
    final_scores_relevant_columns_for_merge = final_scores[["id", "community_broker_score"]]
    nodes_with_broker_score = nodes_with_characteristics.merge(
        final_scores_relevant_columns_for_merge, on="id", how="left"
    )
    nodes_with_broker_score["community_broker_score"] = nodes_with_broker_score[
        "community_broker_score"
    ].fillna(0)

    return nodes_with_broker_score
