# community_clustering_merge/merger.py

import pandas as pd
from .config import Config

class ClusterMerger(Config):
    """
    ClusterMerger is used to merge the results of multiple clustering algorithms.

    Methods:
        find(parent, x): Finds the root of the set containing x with path compression.
        union(parent, x, y): Merges the sets containing x and y.
        process(clustered_data, id_list, entity_col): Processes and merges clustering results.
    """

    def __init__(self) -> None:
        super().__init__()

    def find(self, parent: dict, x) -> str:
        """
        Finds the root of the set containing x and applies path compression.

        Args:
            parent (dict): Dictionary mapping each entity to its parent.
            x (str): The entity to find.

        Returns:
            str: The root of the set containing x.
        """
        if parent[x] != x:
            parent[x] = self.find(parent, parent[x])
        return parent[x]

    def union(self, parent: dict, x: str, y: str) -> None:
        """
        Merges the sets containing x and y.

        Args:
            parent (dict): Dictionary mapping each entity to its parent.
            x (str): First entity.
            y (str): Second entity.
        """
        root_x = self.find(parent, x)
        root_y = self.find(parent, y)
        if root_x < root_y:
            parent[root_y] = root_x
        else:
            parent[root_x] = root_y

    def process(self, clustered_data: pd.DataFrame, id_list: list, entity_col: str = 'address') -> pd.DataFrame:
        """
        Merges the results of multiple clustering algorithms to generate a final clustering ID.

        Args:
            clustered_data (pd.DataFrame): DataFrame containing clustering results with multiple ID columns.
            id_list (list): List of column names representing different clustering results.
            entity_col (str): The column name representing unique entities.

        Returns:
            pd.DataFrame: DataFrame with an additional 'id' column representing the merged clustering result.
        """
        # Initialize Union-Find structure with entities
        unique_entities = clustered_data[entity_col].unique()
        parent = {entity: entity for entity in unique_entities}

        # Merge clusters from each clustering algorithm
        for id_col in id_list:
            # Exclude invalid clusters (assuming 0 is invalid)
            valid_clusters = clustered_data[clustered_data[id_col] != 0].groupby(id_col)

            for cluster_id, group in valid_clusters:
                # Ensure cluster_id is integer
                if not isinstance(cluster_id, int):
                    try:
                        cluster_id = int(cluster_id)
                    except ValueError:
                        continue  # skip non-integer cluster IDs

                group_entities = group[entity_col].tolist()
                if len(group_entities) > 1:
                    first_entity = group_entities[0]
                    for entity in group_entities[1:]:
                        self.union(parent, first_entity, entity)

        # Apply path compression to find final roots
        for entity in parent:
            parent[entity] = self.find(parent, entity)

        # Group entities by root
        groups = {}
        for entity, root in parent.items():
            if root not in groups:
                groups[root] = []
            groups[root].append(entity)

        # Assign the smallest cluster ID from all clusters in the group as the final cluster ID
        root_to_min_id = {}
        for root, entities in groups.items():
            min_id = float('inf')
            for id_col in id_list:
                # Get all cluster IDs for entities in the group, excluding 0
                cluster_ids = clustered_data.loc[clustered_data[entity_col].isin(entities), id_col]
                valid_ids = cluster_ids[cluster_ids != 0]
                if not valid_ids.empty:
                    current_min = valid_ids.min()
                    if current_min < min_id:
                        min_id = current_min
            # Assign min_id if found; otherwise, assign 0
            root_to_min_id[root] = int(min_id) if min_id != float('inf') else 0

        # Map each entity to its group's minimal cluster ID
        clustered_data['id'] = clustered_data[entity_col].map(parent).map(root_to_min_id)

        return clustered_data
