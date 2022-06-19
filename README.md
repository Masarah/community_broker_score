# Community Broker Score

The community broker score quantifies brokers reach and control at the meso level in social networks. The measure was developed in: Paquet-Clouston, M., Bouchard, M. (2022) A Robust Measure to Uncover Community Brokerage in Illicit Networks. _Journal of Quantitative Criminology_ https://doi.org/10.1007/s10940-022-09549-6

All information about the measure can be found here: https://link.springer.com/article/10.1007/s10940-022-09549-6. This repository allows one to calculate the community broker score as presented in the study on one's own networks, as explained below. 


Local Community Broker Score:
> The *local community broker score* is calculated for each partition (also known as a community structure) found through a community detection algorithm (in the paper, we used the Leiden algorithm). This local score quantifies, for each bridge created between two different communities, the bridge’s size (the number of people connected through the bridge), efficiency (how easily these people can be reached (i.e., cohesion) and exclusivity (whether other brokers connect these two communities).

Global Community Broker Score:
> The *global community broker score* is an average of all local scores, making it robust to the inherent randomness of community partitioning. The averaged global score thus follows the partition distribution found when running the community detection algorithm thousands of times. This implies that a partition that emerges more often has more weight than an outlier partition (although the outlier partitions are still considered).

This package allows one to calculate the *local community broker score* given a known partition. Info package: https://pypi.org/project/Community-Broker-Score/

Format of edge and node files:

    A node dataframe with two mandatory columns:
      - Column 1: id of each unique node
      - Column 2: id of the community in which each unique node belongs

    An undirected edge dataframe in which each row in the edge dataframe represents a relationship (a tie or an edge) between two nodes.

## Procedure

Package info: https://pypi.org/project/Community-Broker-Score/

Install Package
  ```
  pip install Community-Broker-Score
  ```

  Import package in environment:
  ```
  from community_broker_score import community_broker_score as cb 
  ```
  Needed Python libraries:
  ```
  pandas as pd
  numpy as np
  networkx as nx
  ```

## Package Functions:

  ### Calculate the local community broker score
  ```
  cb.local_community_broker_score(nodes, edges)

  ```

  ### Extract the cohesion score (average_shortest_path_length from networkx), number of people and number of brokers for each community
  ```
  cb.find_community_characteristics(nodes, edges)
  ```

  ### Detect each edge that is a bridge between two communities and create a dataframe with only these edges
  ```
  cb.detect_brokering_edges(nodes, edges)
  ```

  ### Detect community brokers and tag them as such in the node dataframe
  ```
  cb.detect_community_brokers(nodes, edges)
  ```


## Testing
Using pytest
 ```
 python -m pytest tests/test_broker_score.py
 ```
