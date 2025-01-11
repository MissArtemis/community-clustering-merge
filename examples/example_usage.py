# examples/example_usage.py

import pandas as pd
from community_clustering_merge import ClusterMerger

def main():
    # Simple test case
    address_list = ['A','B','C','D','E','F','G']
    id_1 = [1,1,3,3,0,0,7]
    id_2 = [0,2,2,2,2,0,7]
    df = pd.DataFrame({'address': address_list, 'id_1': id_1, 'id_2': id_2})
    df['expect_id'] = pd.Series([1,1,1,1,1,0,7])

    print("Original Data (Simple Test):")
    print(df)

    # Instantiate ClusterMerger and process data
    merger = ClusterMerger()
    result_df = merger.process(df.copy(), ['id_1', 'id_2'], entity_col='address')

    print("\nProcessed Data (Simple Test):")
    print(result_df[['address', 'id_1', 'id_2', 'id', 'expect_id']])

    # Validate results
    if all(result_df['id'] == df['expect_id']):
        print("\nValidation Passed: Processed 'id' column matches 'expect_id' column.")
    else:
        print("\nValidation Failed: Processed 'id' column does not match 'expect_id' column.")

    # Complex test case
    address_list_complex = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']

    # Define clustering assignments
    id_1_complex = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 0]
    id_2_complex = [1, 4, 5, 1, 4, 5, 1, 4, 5, 6, 0]
    id_3_complex = [1, 4, 5, 7, 1, 8, 5, 5, 1, 9, 0]
    id_4_complex = [1, 10, 11, 1, 12, 1, 11, 13, 14, 1, 0]

    # Create DataFrame
    df_complex = pd.DataFrame({
        'address': address_list_complex,
        'id_1': id_1_complex,
        'id_2': id_2_complex,
        'id_3': id_3_complex,
        'id_4': id_4_complex
    })

    # Expected final id: 1 for all entities except 'K' which should be 0
    df_complex['expect_id'] = [1,1,1,1,1,1,1,1,1,1,0]

    print("\nOriginal Data (Complex Test):")
    print(df_complex)

    # Instantiate ClusterMerger and process data
    merger_complex = ClusterMerger()
    result_df_complex = merger_complex.process(df_complex.copy(), ['id_1', 'id_2', 'id_3', 'id_4'], entity_col='address')

    print("\nProcessed Data (Complex Test):")
    print(result_df_complex[['address', 'id_1', 'id_2', 'id_3', 'id_4', 'id', 'expect_id']])

    # Validate results
    if all(result_df_complex['id'] == df_complex['expect_id']):
        print("\nValidation Passed: All entities have been merged into a single cluster.")
    else:
        print("\nValidation Failed: Merged IDs do not match the expected single cluster.")

if __name__ == "__main__":
    main()
