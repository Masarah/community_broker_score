from community_broker_score import (
    detect_brokering_edges,
    detect_community_brokers
    )
import pandas as pd


def test_detect_brokering_edges_returns():

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
    assert 'community_broker' in result.columns
    assert len(result) == 2

    assert result.iloc[0]['A'] == 1
    assert result.iloc[0]['B'] == 2
    assert result.iloc[1]['A'] == 5
    assert result.iloc[1]['B'] == 1

def test_detect_community_brokers_returns():

    #  We create 2 brokering edges, (1,2) and (5,1)
    nodes = pd.DataFrame({
    'id': [1, 2, 3, 4, 5],
    'community_id': ['a', 'b', 'c', 'c', 'b']}
    )
    edges = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [2, 5, 4, 3, 1]}
    )
    result = detect_community_brokers(nodes, edges)
    print(result)
    assert type(result) == pd.DataFrame
    assert 'n_community_broker' in result.columns
    assert False
