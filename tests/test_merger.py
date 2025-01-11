# tests/test_merger.py

import pytest
import pandas as pd
from community_clustering_merge import ClusterMerger

def test_cluster_merger_simple():
    """
    Simple test case where some entities are grouped into different clusters.
    """
    address_list = ['A','B','C','D','E','F','G']
    id_1 = [1,1,3,3,0,0,7]
    id_2 = [0,2,2,2,2,0,7]
    df = pd.DataFrame({'address': address_list, 'id_1': id_1, 'id_2': id_2})
    df['expect_id'] = pd.Series([1,1,1,1,1,0,7])

    merger = ClusterMerger()
    result_df = merger.process(df.copy(), ['id_1', 'id_2'], entity_col='address')

    assert all(result_df['id'] == df['expect_id']), "Merged IDs do not match expected IDs."

def test_cluster_merger_complex():
    """
    Complex test case where multiple id columns intertwine clusters,
    resulting in all entities being merged into a single cluster.
    Additionally, includes an entity with 0 in all cluster columns.
    """
    address_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

    # Define clustering assignments
    id_1 = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 0]   # 'K' has 0 in all cluster columns
    id_2 = [1, 4, 5, 1, 4, 5, 1, 4, 5, 6, 0]
    id_3 = [1, 4, 5, 7, 1, 8, 5, 5, 1, 9, 0]
    id_4 = [1, 10, 11, 1, 12, 1, 11, 13, 14, 1, 0]

    # Create DataFrame
    df = pd.DataFrame({
        'address': address_list,
        'id_1': id_1,
        'id_2': id_2,
        'id_3': id_3,
        'id_4': id_4
    })

    # Expected final id: 1 for all entities except 'K' which should be 0
    df['expect_id'] = [1,1,1,1,1,1,1,1,1,1,0]

    merger = ClusterMerger()
    result_df = merger.process(df.copy(), ['id_1', 'id_2', 'id_3', 'id_4'], entity_col='address')

    # Validate that all 'id' are 1 except 'K' which should be 0
    assert all(result_df['id'] == df['expect_id']), "Merged IDs do not match expected IDs in complex test case."

    # Optional: Print the results for visual verification
    print("\nComplex Test Case Results:")
    print(result_df[['address', 'id_1', 'id_2', 'id_3', 'id_4', 'id', 'expect_id']])

if __name__ == "__main__":
    pytest.main()
