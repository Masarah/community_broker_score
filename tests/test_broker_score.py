from community_broker_score import detect_brokering_edges, detect_community_brokers
import pandas as pd


def test_detect_brokering_edges_returns_dataframe():

    #  We create 2 brokering edges, (1,2) and (5,1)
    nodes = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'community_id': ['a', 'b', 'c', 'c', 'b']}
    )
    edges = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [2, 5, 4, 3, 1]}
    )
    result = detect_brokering_edges(nodes, edges)

    assert type(result) == pd.DataFrame
    assert result.columns == ['A', 'B', 'community_id_A', 'community_id_B', 'community_broker']

    assert len(result) == 2

    assert result.iloc[0]['A'] == 1
    assert result.iloc[0]['B'] == 2
    assert result.iloc[1]['A'] == 5
    assert result.iloc[1]['B'] == 1
