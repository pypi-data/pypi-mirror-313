from .BookNLP_fr_number import assign_number_to_PER_entities
from .BookNLP_fr_gender import assign_gender_to_PER_entities

import pkg_resources
import numpy as np
from tqdm.auto import tqdm
import pandas as pd
from collections import Counter

def add_mention_number_and_gender_infos(entities_df):
    # Locate the CSV file within the package
    insee_path = pkg_resources.resource_filename('BOOK_NLP_fr', 'data/insee_names_fr_1900_2023.csv')
    # print("Insee_data Loaded successfully.")

    entities_df['number'] = assign_number_to_PER_entities(entities_df)['number']
    entities_df['gender'] = assign_gender_to_PER_entities(entities_df, insee_path=insee_path)['gender']

    not_PER_entities = entities_df[entities_df['cat'] != "PER"].copy()
    entities_df.loc[not_PER_entities.index, 'number'] = 'Not_Assigned'
    entities_df.loc[not_PER_entities.index, 'gender'] = 'Not_Assigned'

    return entities_df

## General entities_df functions
def add_mention_paragraphe_and_sentence_infos(entities_df, tokens_df):
    start_token_ids = entities_df['start_token'].tolist()
    entities_df['paragraph_ID'] = tokens_df.loc[start_token_ids, 'paragraph_ID'].tolist()
    entities_df['sentence_ID'] = tokens_df.loc[start_token_ids, 'sentence_ID'].tolist()
    entities_df['start_token_ID_within_sentence'] = tokens_df.loc[start_token_ids, 'token_ID_within_sentence'].tolist()
    return entities_df
def get_outer_to_inner_nesting_level(entities_df):
    # Step 1: Extract start and end tokens
    start_tokens = entities_df['start_token'].values
    end_tokens = entities_df['end_token'].values
    N = len(entities_df)

    # Step 2: Create a boolean matrix for nesting
    nested_matrix = (start_tokens[:, np.newaxis] >= start_tokens) & (end_tokens[:, np.newaxis] <= end_tokens)

    # Step 3: Set diagonal to False (a mention cannot be nested in itself)
    np.fill_diagonal(nested_matrix, False)

    # Step 4: Initialize nested levels
    nested_levels = np.zeros(N, dtype=int)

    # Iterate through each mention and calculate its nested level based on the nested matrix
    for i in range(N):
        # Get indices of mentions that are nested within mention i
        nested_indices = np.where(nested_matrix[i])[0]

        # Only calculate max if there are nested mentions
        if nested_indices.size > 0:
            nested_levels[i] = nested_levels[nested_indices].max() + 1

    # Step 5: Assign the calculated nested levels back to the DataFrame
    entities_df['out_to_in_nested_level'] = nested_levels

    return entities_df
def get_inner_to_outer_nesting_level(entities_df):
    # Step 1: Extract start and end tokens
    start_tokens = entities_df['start_token'].values
    end_tokens = entities_df['end_token'].values
    N = len(entities_df)

    # Step 2: Create a boolean matrix for nesting (inner-to-outer)
    nested_matrix = (start_tokens[:, np.newaxis] >= start_tokens) & (end_tokens[:, np.newaxis] <= end_tokens)

    # Step 3: Set diagonal to False (a mention cannot be nested in itself)
    np.fill_diagonal(nested_matrix, False)

    # Step 4: Initialize nested levels
    nested_levels = np.zeros(N, dtype=int)

    # Iterate in reverse to accumulate nesting levels from the innermost to the outermost level
    for i in range(N - 1, -1, -1):  # Start from the last mention and move backwards
        # Get indices of mentions that are nested within mention i
        nested_indices = np.where(nested_matrix[:, i])[0]

        # Only calculate max if there are nested mentions
        if nested_indices.size > 0:
            nested_levels[i] = nested_levels[nested_indices].max() + 1

    # Step 5: Assign the calculated nested levels back to the DataFrame
    entities_df['in_to_out_nested_level'] = nested_levels

    return entities_df
def get_nested_entities_count(entities_df):
    # Step 1: Extract start and end tokens and categories
    start_tokens = entities_df['start_token'].values
    end_tokens = entities_df['end_token'].values
    categories = entities_df['cat'].values
    N = len(entities_df)

    # Step 2: Create a boolean matrix for nesting
    nested_matrix = (start_tokens[:, np.newaxis] <= start_tokens) & (end_tokens[:, np.newaxis] >= end_tokens)

    # Step 3: Set diagonal to False (an entity cannot be nested within itself)
    np.fill_diagonal(nested_matrix, False)

    # Step 4: Get the filtered indices for entities with in_to_out_nested_level > 0
    nested_indices = entities_df[entities_df['in_to_out_nested_level'] > 0].index.values

    # Step 5: Initialize nested entities count with zeros for all entities
    nested_entities_count = np.zeros(N, dtype=int)

    # Step 6: Vectorized counting of same-category nested entities
    if len(nested_indices) > 0:
        # Filter the nested matrix to only rows corresponding to nested_indices
        filtered_nested_matrix = nested_matrix[nested_indices]

        # Compare categories in a vectorized manner
        category_comparison = categories[nested_indices][:, np.newaxis] == categories

        # Use element-wise multiplication to only count same-category nested entities
        same_category_nested_count = np.sum(filtered_nested_matrix & category_comparison, axis=1)

        # Assign the counts back to the corresponding positions in the full count array
        nested_entities_count[nested_indices] = same_category_nested_count

    # Step 7: Assign the nested entities count back to the DataFrame
    entities_df['nested_entities_count'] = nested_entities_count

    return entities_df
def assign_mention_head_id(entities_df, tokens_df):
    entities_df['head_id'] = entities_df['start_token']
    filtered_entities_df = entities_df[entities_df['mention_len'] != 1]

    # Prepare a dictionary to store the results
    mention_head_ids = []

    # Iterate over each entity in entities_df
    for start_token, end_token in tqdm(zip(filtered_entities_df['start_token'], filtered_entities_df['end_token']),
                                       total=len(filtered_entities_df), desc="Extracting Mention Head Infos",
                                       leave=False):
        # Get a subset of tokens_df directly for the token range
        mention_token_df = tokens_df.loc[start_token:end_token].copy()

        # Identify if the head is inside the mention
        mention_token_df['head_is_inside_mention'] = mention_token_df['syntactic_head_ID'].isin(
            mention_token_df['token_ID_within_document'])
        mention_token_df = mention_token_df.sort_values(by=['head_is_inside_mention'], ascending=[True])

        if np.array_equal(mention_token_df['head_is_inside_mention'].values[:2], [False, True]):
            pass

        else:
            # Calculate the count of each head ID directly using numpy
            head_id_counts = np.bincount(
                mention_token_df['syntactic_head_ID'].values, minlength=tokens_df['token_ID_within_document'].max() + 1
            )
            mention_token_df['head_count'] = mention_token_df['syntactic_head_ID'].map(lambda x: head_id_counts[x])

            # Sort based on 'head_is_inside_mention' and 'head_count'
            mention_token_df = mention_token_df.sort_values(by=['head_is_inside_mention', 'head_count'],
                                                            ascending=[True, False])

        # Get the head ID for the mention
        mention_head_id = mention_token_df.index[0]
        mention_head_ids.append(mention_head_id)

    entities_df.loc[filtered_entities_df.index, "head_id"] = mention_head_ids

    return entities_df
def mention_head_syntactic_infos(entities_df, tokens_df):
    head_token_ids = entities_df['head_id'].tolist()
    head_tokens_rows = tokens_df.loc[head_token_ids, ['word', 'dependency_relation', 'syntactic_head_ID']]
    entities_df[['head_word', 'head_dependency_relation', 'head_syntactic_head_ID']] = head_tokens_rows.values.tolist()
    return entities_df
def assign_mention_prop(entities_df, tokens_df):
    # Define the mapping dictionary
    mapping_dict = {
        'PROPN': 'PROP',
        'PRON': 'PRON',
        'DET': 'PRON',
        'ADP': 'PRON',
        'PUNCT': 'PRON',
        'NOUN': 'NOM',
    }
    default_value = "NOM"

    entities_df['POS_tag'] = pd.merge(entities_df['head_id'], tokens_df, left_on='head_id', right_index=True)['POS_tag']
    # Use map to apply the mapping dictionary, setting unmapped values to NaN

    # Apply the mapping dictionary to the 'POS_tag' column
    entities_df['prop'] = entities_df['POS_tag'].map(mapping_dict).fillna(default_value)

    special_pronouns_tokens = ['moi', 'mien', 'miens', 'mienne', 'miennes', 'tien', 'tiens', 'tienne', 'tiennes',
                               'vôtre', 'vôtres']
    special_pronouns_tokens_id = list(tokens_df[tokens_df['word'].str.lower().isin(special_pronouns_tokens)].index)
    head_id_in_special_tokens = list(entities_df[entities_df['head_id'].isin(special_pronouns_tokens_id)].index)
    entities_df.loc[head_id_in_special_tokens, ['prop']] = "PRON"

    # Propagate PROP tag to all
    occurrence_treshold = 5
    proper_name_mentions = dict(Counter(entities_df[entities_df['prop'] == 'PROP']['text']))
    proper_name_mentions = [key for key in proper_name_mentions.keys() if
                            proper_name_mentions[key] >= occurrence_treshold]
    proper_rows = entities_df[entities_df['text'].isin(proper_name_mentions)]
    entities_df.loc[proper_rows.index, 'prop'] = 'PROP'

    return entities_df

def add_features_to_entities(entities_df, tokens_df):
    entities_df['mention_len'] = entities_df['end_token'] + 1 - entities_df['start_token']
    entities_df = add_mention_paragraphe_and_sentence_infos(entities_df, tokens_df)
    entities_df = get_outer_to_inner_nesting_level(entities_df)
    entities_df = get_inner_to_outer_nesting_level(entities_df)
    entities_df = get_nested_entities_count(entities_df)
    entities_df = assign_mention_head_id(entities_df, tokens_df)
    entities_df = mention_head_syntactic_infos(entities_df, tokens_df)
    entities_df = assign_mention_prop(entities_df, tokens_df)
    entities_df = add_mention_number_and_gender_infos(entities_df)
    return entities_df