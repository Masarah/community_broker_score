# Community Broker Score

The community broker score quantifies brokers reach and control at the meso level. It was developed in the paper: "A Robust Measure to Uncover Community Brokerage in Illicit Networks" and published in the Journal of Quantitative Criminology. 

Local Community Broker Score: 
> The *local community broker score* is calculated for each partition (also known as community structure) found through a community detection algorithm (in the paper, we used the Leiden algorithm). This local score quantifies, for each bridge created between two different communities, the bridge’s size (the number of people connected through the bridge), efficiency (how easily these people can be reached (i.e., cohesion) and exclusivity (whether other brokers connect these two communities).

Global Community Broker Score:
> The *global community broker score* is an average of all local scores, making it robust to the inherent randomness of community partitioning. The averaged global score thus follows the partition distribution found when running the community detection algorithm thousands of times. This implies that a partition that emerges more often has more weight than an outlier partition (although the outlier partitions are still considered).

This package allows one to calculate the *local community broker score* given a known partition. Info package: https://test.pypi.org/project/Community-Broker-Score/

Format of edge and node files: 

    A node dataframe with two mandatory columns: 
      - Name of column 1 in node dataframe: 'id' (id of each unique node) 
      - Name of column 2 in node dataframe: 'community_id' (community id to which each unique node belongs)
      
    An edge dataframe with two mandatory columns*:  
      - Name of column 1 in edge dataframe: 'A' 
      - Name of column 2 in edge dataframe: 'B'
  
*Each row in the edge dataframe represents a tie between two nodes 

## Procedure

Install Package 
  ```
  pip install -i https://test.pypi.org/simple/ Community-Broker-Score
  ```

  Import package in environment: 
  ```
  import community_broker_score as cb
  ```
  Needed Python libraries : 
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

  


