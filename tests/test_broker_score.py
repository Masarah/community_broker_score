from community_broker_score import (
    detect_brokering_edges,
    detect_community_brokers,
    find_community_characteristics,
    local_community_broker_score
)
import pandas as pd


def test_detect_brokering_edges_returns():

    #  We create 2 brokering edges, (1,2) and (5,1)
    nodes = pd.DataFrame({"id": [1, 2, 3, 4, 5], "community_id": ["a", "b", "c", "c", "b"]})
    edges = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [2, 5, 4, 3, 1]})
    result = detect_brokering_edges(nodes, edges)

    assert type(result) == pd.DataFrame
    assert "community_broker" in result.columns
    assert len(result) == 2

    assert result.iloc[0]["A"] == 1
    assert result.iloc[0]["B"] == 2
    assert result.iloc[1]["A"] == 5
    assert result.iloc[1]["B"] == 1


def test_detect_community_brokers_returns():

    #  We create 2 brokering edges, (1,2) and (5,1)
    nodes = pd.DataFrame({"id": [1, 2, 3, 4, 5], "community_id": ["a", "b", "c", "c", "b"]})
    edges = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [2, 5, 4, 3, 1]})
    result = detect_community_brokers(nodes, edges)

    assert type(result) == pd.DataFrame
    assert "n_community_broker" in result.columns
    assert result.iloc[0]["id"] == 1
    assert result.iloc[0]["community_broker"] == 1
    assert result.iloc[0]["n_community_broker"] == 2


def test_find_community_characteristics_returns():

    nodes = pd.DataFrame({"id": [1, 2, 3, 4, 5], "community_id": ["a", "b", "c", "c", "b"]})
    edges = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [2, 5, 4, 3, 1]})
    result = find_community_characteristics(nodes, edges)

    assert type(result) == pd.DataFrame
    assert len(result) == 3
    assert "community_cohesion" in result.columns
    assert "community_n_people" in result.columns
    assert "community_n_brokers" in result.columns

    assert result.iloc[0]["community_id"] == 'a'
    assert result.iloc[0]["community_cohesion"] == 0
    assert result.iloc[0]["community_n_people"] == 1
    assert result.iloc[0]["community_n_brokers"] == 1

    assert result.iloc[1]["community_id"] == 'b'
    assert result.iloc[1]["community_cohesion"] == 1
    assert result.iloc[1]["community_n_people"] == 2
    assert result.iloc[1]["community_n_brokers"] == 2

    assert result.iloc[2]["community_id"] == 'c'
    assert result.iloc[2]["community_cohesion"] == 1
    assert result.iloc[2]["community_n_people"] == 2
    assert result.iloc[2]["community_n_brokers"] == 0


def test_local_community_broker_score_returns():
    nodes = pd.DataFrame({"id": [1, 2, 3, 4, 5], "community_id": ["a", "b", "c", "c", "b"]})
    edges = pd.DataFrame({"A": [1, 2, 3, 4, 5], "B": [2, 5, 4, 3, 1]})
    result = local_community_broker_score(nodes, edges)

    assert len(result) == 5
    assert 'community_broker_score' in result.columns
    assert (result.community_broker_score >= 0).all()
    assert (result.community_broker_score <= len(result)).all()
