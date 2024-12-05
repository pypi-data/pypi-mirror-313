from collections import Counter
import pandas as pd
import csv
import os
import torch
from transformers import CamembertModel, CamembertTokenizerFast
from tqdm.auto import tqdm  # notebook compatible
import numpy as np
import subprocess
import re
import gc
from thinc.api import set_gpu_allocator
from keras.utils import Sequence


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

    special_pronouns_tokens = ['moi', 'mien', 'miens', 'mienne', 'miennes', 'tien', 'tiens', 'tienne', 'tiennes', 'vôtre', 'vôtres']
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

def add_infos_to_entities(entities_df, tokens_df):
    entities_df['mention_len'] = entities_df['end_token'] + 1 - entities_df['start_token']
    entities_df = add_mention_paragraphe_and_sentence_infos(entities_df, tokens_df)
    entities_df = get_outer_to_inner_nesting_level(entities_df)
    entities_df = get_inner_to_outer_nesting_level(entities_df)
    entities_df = get_nested_entities_count(entities_df)
    entities_df = assign_mention_head_id(entities_df, tokens_df)
    entities_df = mention_head_syntactic_infos(entities_df, tokens_df)
    entities_df = assign_mention_prop(entities_df, tokens_df)
    return entities_df



## Get BERT embeddings from tokens_df
def load_tokenizer_and_embedding_model(model_name="almanach/camembert-base"):

    tokenizer = CamembertTokenizerFast.from_pretrained(model_name)
    model = CamembertModel.from_pretrained(model_name, output_hidden_states=True)
    print(f"Tokenizer and Embedding Model Initialized: {model_name}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    return tokenizer, model

def fast_tokennize_tokens_df(tokens_df, tokenizer):
    tokens_dict = []

    # List of words from the dataframe
    words = tokens_df["word"].astype(str).tolist()  # Ensure all words are strings
    token_ids = tokens_df["token_ID_within_document"].tolist()

    # Tokenize all words at once using the fast tokenizer
    batch_encoding = tokenizer.batch_encode_plus(words, add_special_tokens=False)

    # Preallocate the length to reduce append overhead
    for token_id, word_subwords in zip(token_ids, batch_encoding['input_ids']):
        tokens_dict.extend([{
            "token_id": token_id,
            "camembert_token_id": camembert_token_id
        } for camembert_token_id in word_subwords])

    return tokens_dict

def get_boudaries_list(max_token_id=0, sliding_window_size=0, sliding_window_overlap=0.5):
    # Parameters
    sliding_window_overlap = int(sliding_window_size * sliding_window_overlap)  # 50% overlap
    min_token_id = 0

    # Create the sliding window boundaries efficiently using NumPy
    # Step size accounts for the overlap, reducing redundant token IDs
    step_size = sliding_window_size - sliding_window_overlap

    # Create an array of starting boundaries
    min_boundaries = np.arange(min_token_id, max_token_id, step_size)

    # Create corresponding max boundaries (ensure they don't exceed max_token_id)
    max_boundaries = np.minimum(min_boundaries + sliding_window_size, max_token_id)

    # Combine min and max boundaries into a list of tuples and convert to int
    boundaries_list = [(int(min_boundary), int(max_boundary)) for min_boundary, max_boundary in
                       zip(min_boundaries, max_boundaries)]

    return boundaries_list

def compute_sub_word_embeddings(boundaries_list, tokens_dict, model, mini_batch_size=100, padding_token_id=0, sliding_window_size=0, device='cpu'):
    max_token_id = len(tokens_dict)  # You may want to adjust this based on your logic

    tokens_dict_df = pd.DataFrame(tokens_dict)

    # Precompute the padding tensor once
    padding_tensor = torch.tensor([padding_token_id] * sliding_window_size, dtype=torch.long).unsqueeze(0).to(device)

    batch_input_ids = []
    all_embeddings_batches = []

    with torch.no_grad():
        for start_boundary, end_boundary in tqdm(boundaries_list, desc='Embedding Tokens', leave=False):
            input_ids = tokens_dict_df[start_boundary:end_boundary]['camembert_token_id'].tolist()
            real_tokens_length = len(input_ids)

            # Convert to tensor and send to device
            input_tensor = torch.tensor(input_ids, dtype=torch.long).unsqueeze(0).to(device)

            # Check if padding is needed
            if real_tokens_length < sliding_window_size:
                # Pad the tensor to the right size
                padded_input = torch.cat([input_tensor, padding_tensor[:, real_tokens_length:]], dim=1)
            else:
                padded_input = input_tensor

            batch_input_ids.append(padded_input)

            # Process the batch based on the specified conditions
            if (len(batch_input_ids) == mini_batch_size) or (
                    end_boundary == max_token_id):  # Ensure end_boundary is a single value
                # Process the batch
                batch_input_ids_tensor = torch.cat(batch_input_ids,
                                                   dim=0)  # Concatenate all input tensors along the batch dimension
                attention_mask = (batch_input_ids_tensor != padding_token_id).long()  # Create attention mask

                # Move to device if not already
                batch_input_ids_tensor = batch_input_ids_tensor.to(device)
                attention_mask = attention_mask.to(device)

                # Get model outputs
                outputs = model(batch_input_ids_tensor, attention_mask=attention_mask)
                last_hidden_states = outputs.last_hidden_state  # Get last hidden states

                # Reshape last hidden states
                last_hidden_states = last_hidden_states.view(-1, last_hidden_states.shape[2])

                embedding_end_index = real_tokens_length - sliding_window_size
                if embedding_end_index != 0:
                    token_embeddings = last_hidden_states[:embedding_end_index, :]  # Shape: [num_tokens, 1024]
                else:
                    token_embeddings = last_hidden_states

                all_embeddings_batches.append(token_embeddings.cpu())

                # Reset the batch
                batch_input_ids = []

    # Concatenate all embeddings
    all_embeddings = torch.cat(all_embeddings_batches)

    subword_indices = []
    for start_boundary, end_boundary in boundaries_list:
        subword_indices += list(range(start_boundary, end_boundary))

    return subword_indices, all_embeddings

def average_embeddings_from_overlapping_sliding_windows(tokens_dict, subword_indices, all_embeddings):
    # Step 1: Collect embeddings and sum them directly
    for token in tokens_dict:
        token['embedding_sum'] = None
        token['embedding_count'] = 0

    # Step 2: Sum embeddings in place
    for embedding_index, embedding in zip(subword_indices, all_embeddings):
        token = tokens_dict[embedding_index]

        # Initialize sum if not set
        if token['embedding_sum'] is None:
            token['embedding_sum'] = embedding
        else:
            token['embedding_sum'] += embedding

        token['embedding_count'] += 1

    # Step 3: Calculate average embeddings
    for token in tqdm(tokens_dict, total=len(tokens_dict), desc="Calculating average embeddings", leave=False):
        if token['embedding_count'] > 0:
            token['average_embedding'] = token['embedding_sum'] / token['embedding_count']

        # Clean up
        del token['embedding_sum']
        del token['embedding_count']

    return tokens_dict

def get_token_embeddings_tensor_from_subwords(tokens_df, tokens_dict, hidden_size, first_last_average=True):
    ## Pre-allocate zero tensor to avoid creating it in each iteration
    zero_tensor = torch.zeros(hidden_size)

    # Pre-build the dictionary for collecting embeddings
    tokens_df_embeddings_dict = {token_id: [] for token_id in tokens_df['token_ID_within_document'].tolist()}

    # Populate the embeddings dictionary from tokens_dict
    for token in tokens_dict:
        token_id = token['token_id']
        tokens_df_embeddings_dict[token_id].append(token['average_embedding'])

    tokens_embeddings = []

    # Process each token's subword embeddings
    for token_id in tqdm(tokens_df_embeddings_dict.keys(), desc='Averaging subwords embeddings', leave=False):
        embeddings = tokens_df_embeddings_dict[token_id]

        if len(embeddings) == 0:
            embeddings = [zero_tensor]  # Use pre-allocated zero tensor

        if first_last_average:
            # Take only the first and last embedding
            first_last = torch.stack([embeddings[0], embeddings[-1]], dim=0)
            average_embedding = torch.mean(first_last, dim=0)
        else:
            # Use all embeddings
            average_embedding = torch.mean(torch.stack(embeddings, dim=0), dim=0)

        tokens_embeddings.append(average_embedding)

    # Stack the list of embeddings into a tensor
    tokens_embeddings_tensor = torch.stack(tokens_embeddings)

    return tokens_embeddings_tensor

def get_embedding_tensor_from_tokens_df(tokens_df, tokenizer, model, sliding_window_size='max', mini_batch_size=10,
                                        sliding_window_overlap=0.5, first_last_average=True, device=None):
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model_max_length = tokenizer.model_max_length
    hidden_size = model.config.hidden_size
    if sliding_window_size == "max":
        sliding_window_size = model_max_length
    padding_token_id = int(tokenizer.pad_token_id)
    tokens_dict = fast_tokennize_tokens_df(tokens_df, tokenizer)
    boundaries_list = get_boudaries_list(max_token_id=len(tokens_dict), sliding_window_size=sliding_window_size,
                                         sliding_window_overlap=sliding_window_overlap)
    subword_indices, all_embeddings = compute_sub_word_embeddings(boundaries_list, tokens_dict, model,
                                                                  mini_batch_size=mini_batch_size,
                                                                  padding_token_id=padding_token_id,
                                                                  sliding_window_size=sliding_window_size,
                                                                  device=device)
    tokens_dict = average_embeddings_from_overlapping_sliding_windows(tokens_dict, subword_indices, all_embeddings)
    tokens_embeddings_tensor = get_token_embeddings_tensor_from_subwords(tokens_df, tokens_dict, hidden_size,
                                                                         first_last_average=first_last_average)

    return tokens_embeddings_tensor


## Coreference Resolution
### Initialize mentions pairs
def initialize_mention_pairs_df(entities_df: pd.DataFrame, pronoun_antecedent_max_distance: int = 30, proper_common_nouns_antecedent_max_distance: int = 300, low_information_noun_max_distance: int = 50) -> pd.DataFrame:
    """
    Initialize a DataFrame of mention pairs within a specified maximum distance. The maximum distance depends on the category ('prop') of mentions (PROP, NOM, PRON).

    Parameters:
    ----------
    entities_df : pd.DataFrame
        DataFrame containing entity information. Must include columns 'prop' and 'mention_len'.
    pronoun_antecedent_max_distance : int, optional
        Maximum distance allowed for pronoun antecedents, in mentions (default is 30).
    proper_common_nouns_antecedent_max_distance : int, optional
        Maximum distance allowed for proper/common nouns, in mentions (default is 300).
    low_information_noun_max_distance : int, optional
        Maximum distance allowed for low-information nouns, in mentions (default is 50).

    Returns:
    -------
    pd.DataFrame
        A DataFrame with columns "A" and "B", representing valid mention pairs.

    Example
    -------
    mention_pairs_df = initialize_mention_pairs_df(PER_entities_df, pronoun_antecedent_max_distance=30, proper_common_nouns_antecedent_max_distance=300, low_information_noun_max_distance=50)
    """

    mentions_prop_list = entities_df['prop'].to_numpy()  # Convert to NumPy array for faster access
    mentions_len_list = entities_df['mention_len'].to_numpy()  # Convert to NumPy array for faster access

    # N: Number of mentions
    N = len(mentions_prop_list)

    # Precompute max distances
    max_distances_matrix = np.full((N, N), proper_common_nouns_antecedent_max_distance)  # Default for common nouns
    for A in range(N):
        if ('NOM' in mentions_prop_list[A]) and (mentions_len_list[A] == 1):
            max_distances_matrix[A, :] = low_information_noun_max_distance  # Set row for pronoun
            max_distances_matrix[:, A] = low_information_noun_max_distance  # Set column for pronoun
    for A in range(N):
        if 'PRON' in mentions_prop_list[A]:
            max_distances_matrix[A, :] = pronoun_antecedent_max_distance  # Set row for pronoun
            max_distances_matrix[:, A] = pronoun_antecedent_max_distance  # Set column for pronoun

    # Compute mention distance matrix
    mention_distance_matrix = np.arange(N).reshape(N, 1) - np.arange(N).reshape(1, N)
    mention_distance_matrix = np.where(mention_distance_matrix <= 0, N,
                                       mention_distance_matrix)  # Replace negatives with N

    # Calculate the distance matrix
    matrix = max_distances_matrix - mention_distance_matrix

    # Get indices where distances are non-negative
    indexes = np.where(matrix >= 0)
    cell_indices = list(zip(indexes[1], indexes[0]))  # Combine row and column indices

    mention_pairs_df = pd.DataFrame(cell_indices, columns=["A", "B"]).sort_values(by=["A", "B"]).reset_index(drop=True)
    return mention_pairs_df

### generate mentions pairs tensor
def get_mentions_embeddings(entities_df, tokens_embeddings_tensor):
    mentions_embeddings = []
    for entity_start_token, entity_end_token in entities_df[['start_token', 'end_token']].values:
        # Convert the embeddings to PyTorch tensors
        first_last_embeddings = [tokens_embeddings_tensor[entity_start_token],
                                 tokens_embeddings_tensor[entity_end_token]]

        entity_mean_embedding = torch.mean(torch.stack(first_last_embeddings), dim=0)
        mentions_embeddings.append(entity_mean_embedding)

    # Stack all embeddings into a single tensor
    mentions_embeddings_tensor = torch.stack(mentions_embeddings)

    return mentions_embeddings_tensor
def generate_coreference_resolution_training_dict(files_directory, model_name, features, embedding_batch_size=30):
    tokenizer, model = load_tokenizer_and_embedding_model(model_name)
    extension = ".entities"
    entities_files = sorted([f.replace(extension, "") for f in os.listdir(files_directory) if f.endswith(extension)])

    model_training_dict = {}
    for file_name in tqdm(sorted(entities_files[:], reverse=True)):
        tokens_df = load_tokens_df(file_name, files_directory=files_directory, extension=".tokens")
        entities_df = load_entities_df(file_name, files_directory=files_directory, extension=".entities")
        PER_entities_df = entities_df[entities_df["cat"] == "PER"].copy().reset_index(drop=True)

        tokens_embeddings_tensor = get_embedding_tensor_from_tokens_df(tokens_df, tokenizer, model,
                                                                       sliding_window_size='max', mini_batch_size=embedding_batch_size,
                                                                       sliding_window_overlap=0.5,
                                                                       first_last_average=True)
        PER_mentions_embeddings_tensor = get_mentions_embeddings(PER_entities_df, tokens_embeddings_tensor)
        del tokens_embeddings_tensor

        mention_pairs_df = initialize_mention_pairs_df(PER_entities_df, pronoun_antecedent_max_distance=30,
                                                       proper_common_nouns_antecedent_max_distance=300)
        features_array = generate_mention_pairs_features_array(mention_pairs_df, PER_entities_df, features=features)
        labels_array = get_mention_pairs_gold_labels(mention_pairs_df, PER_entities_df)

        model_training_dict[file_name] = {'PER_entities_df': PER_entities_df,
                                          'mention_pairs_df': mention_pairs_df[["A", "B"]],
                                          'PER_mentions_embeddings_tensor': PER_mentions_embeddings_tensor.numpy(),
                                          'features_tensor': features_array,
                                          'labels_tensor': labels_array}
    del tokenizer, model
    torch.cuda.empty_cache()  # Clear the CUDA cache
    gc.collect()

    # model_training_dict = generate_coreference_resolution_training_dict(files_directory, model_name, features)
    return model_training_dict
def generate_split_data(files_list, model_training_dict):
    overall_mention_pairs_dfs = []
    overall_PER_mentions_embeddings_tensors = []
    overall_features_tensors = []
    overall_labels_tensors = []

    overall_mention_index = 0
    for file_name in files_list:
        PER_entities_df = model_training_dict[file_name]["PER_entities_df"]
        PER_mentions_embeddings_tensor = model_training_dict[file_name]["PER_mentions_embeddings_tensor"]
        features_tensor = model_training_dict[file_name]["features_tensor"]
        labels_tensor = model_training_dict[file_name]["labels_tensor"]

        mention_pairs_df = model_training_dict[file_name]["mention_pairs_df"][["A", "B"]]
        mention_pairs_df = mention_pairs_df + overall_mention_index

        overall_mention_pairs_dfs.append(mention_pairs_df)
        overall_PER_mentions_embeddings_tensors.append(PER_mentions_embeddings_tensor)
        overall_features_tensors.append(features_tensor)
        overall_labels_tensors.append(labels_tensor)

        overall_mention_index += len(PER_entities_df)

        # Clear references to free up memory
        del PER_entities_df, PER_mentions_embeddings_tensor, features_tensor, labels_tensor, mention_pairs_df

    # Concatenate DataFrames and NumPy arrays on CPU
    overall_mention_pairs_df = pd.concat(overall_mention_pairs_dfs).reset_index(drop=True)

    # Keep everything in NumPy arrays to avoid OOM on GPU
    overall_PER_mentions_embeddings_tensor = np.concatenate(overall_PER_mentions_embeddings_tensors, axis=0)  # Use NumPy for now
    overall_features_tensor = np.concatenate(overall_features_tensors, axis=0)  # Use NumPy for now
    overall_labels_tensor = np.concatenate(overall_labels_tensors, axis=0)  # Use NumPy for now

    # Cleanup
    del model_training_dict, overall_mention_pairs_dfs, overall_PER_mentions_embeddings_tensors, overall_features_tensors, overall_labels_tensors
    gc.collect()

    return {
        "overall_mention_pairs_df": overall_mention_pairs_df.to_numpy(),
        "overall_PER_mentions_embeddings_tensor": overall_PER_mentions_embeddings_tensor,  # NumPy array
        "overall_features_tensor": overall_features_tensor,  # NumPy array
        "overall_labels_tensor": overall_labels_tensor  # NumPy array
    }

### Generate mention pairs features array
def add_mentions_infos(mention_pairs_df, entities_df, features=['mention_len', 'start_token_ID_within_sentence']):
    columns=['mention_len', 'start_token_ID_within_sentence']
    columns = [column for column in columns if column in features]
    for mention_polarity in ['A', 'B']:
        mention_pairs_df = pd.merge(mention_pairs_df, entities_df[columns].add_prefix(f"{mention_polarity}_"),
                                    left_on=mention_polarity, right_index=True)
    return mention_pairs_df
def get_mention_pairs_distance_features(mention_pairs_df, entities_df, features=['mention_ID_delta', 'start_token_delta', 'end_token_delta', 'paragraph_ID_delta', 'sentence_ID_delta', 'out_to_in_nested_level_delta']):
    columns = ['start_token', 'end_token', 'paragraph_ID', 'sentence_ID', 'out_to_in_nested_level']
    # Extract infos for each mention in the mention pair
    for mention_polarity in ["A", "B"]:
        mention_pairs_df = mention_pairs_df.merge(
        entities_df[columns].add_prefix(f"{mention_polarity}_"),
        left_on=mention_polarity,
        right_index=True,
        how='left')

    # Generate mention pairs distance features
    if 'mention_ID_delta' in features:
        mention_pairs_df['mention_ID_delta'] = abs(mention_pairs_df['A'] - mention_pairs_df['B'])
    if 'start_token_delta' in features:
        mention_pairs_df['start_token_delta'] = mention_pairs_df['B_start_token'] - mention_pairs_df['A_start_token']
    if 'end_token_delta' in features:
        mention_pairs_df['end_token_delta'] = mention_pairs_df['B_end_token'] - mention_pairs_df['A_end_token']
    if 'paragraph_ID_delta' in features:
        mention_pairs_df['paragraph_ID_delta'] = abs(mention_pairs_df['A_paragraph_ID'] - mention_pairs_df['B_paragraph_ID'])
    if 'sentence_ID_delta' in features:
        mention_pairs_df['sentence_ID_delta'] = abs(mention_pairs_df['A_sentence_ID'] - mention_pairs_df['B_sentence_ID'])
    if 'out_to_in_nested_level_delta' in features:
        mention_pairs_df['out_to_in_nested_level_delta'] = abs((mention_pairs_df['A_out_to_in_nested_level'] - mention_pairs_df['B_out_to_in_nested_level']))

    # Drop previously created columns
    mention_pairs_df.drop([f"{mention_polarity}_{column}" for column in columns for mention_polarity in ["A", "B"]], axis=1, inplace=True)
    return mention_pairs_df
def get_text_and_syntactic_match_features(mention_pairs_df, entities_df, features=['shared_token_ratio', 'text_match', 'head_text_match', 'syntactic_head_match']):
    # Extract infos for each mention in the mention pair
    columns = ['text', 'head_word', 'head_syntactic_head_ID']
    for mention_polarity in ["A", "B"]:
        mention_pairs_df = mention_pairs_df.merge(
        entities_df[columns].add_prefix(f"{mention_polarity}_"),
        left_on=mention_polarity,
        right_index=True,
        how='left')

    def get_shared_token_ratio(mention_pairs_df):
        shared_token_ratio_list = []
        for A_text, B_text in mention_pairs_df[['A_text', 'B_text']].values:
            A_tokens, B_tokens = A_text.lower().split(), B_text.lower().split()

            # Calculate shared tokens
            shared_tokens = set(A_tokens).intersection(set(B_tokens))
            shared_count = len(shared_tokens)

            # Calculate the length of the longer text
            longer_text_tokens_count = max(len(A_tokens), len(B_tokens))

            # Calculate the ratio
            ratio = shared_count / longer_text_tokens_count if longer_text_tokens_count > 0 else 0
            shared_token_ratio_list.append(ratio)
        return shared_token_ratio_list

    if 'shared_token_ratio' in features:
        mention_pairs_df['shared_token_ratio'] = get_shared_token_ratio(mention_pairs_df)
    if 'text_match' in features:
        mention_pairs_df['text_match'] = (mention_pairs_df['A_text'].str.lower() == mention_pairs_df['B_text'].str.lower())*1
    if 'head_text_match' in features:
        mention_pairs_df['head_text_match'] = (mention_pairs_df['A_head_word'].str.lower() == mention_pairs_df['B_head_word'].str.lower())*1
    if 'syntactic_head_match' in features:
        mention_pairs_df['syntactic_head_match'] = (mention_pairs_df['A_head_syntactic_head_ID'] == mention_pairs_df['B_head_syntactic_head_ID'])*1

    mention_pairs_df.drop([f"{mention_polarity}_{column}" for column in columns for mention_polarity in ["A", "B"]], axis=1, inplace=True)

    return mention_pairs_df
def assign_grammatical_person(entities_df):
    grammatical_person_dict = {"1": ['je', 'me', 'moi', "j'", "m'", 'mon', 'ma', 'mes', 'nous', 'notre', 'nos', 'moi - même', 'moi-même', 'mien', 'miens', 'mienne','miennes', 'nôtre', 'nous-mêmes', 'nous - mêmes'],
                               "2": ['tu', 'toi', 'te', "t'", 'ton', 'ta', 'tes', 'vous', 'vôtre', 'vos', 'votre', 'tien', 'tiens', 'tienne', 'tiennes', 'vous - même', 'vous-même', 'toi-même', 'toi - même', 'vous-mêmes', 'vous - mêmes'],
                               "3": ['il', 'elle', 'lui', 'son', 'sa', "l'", 'ses', 'le', 'la', 'se', 'ils', 'elles', 'leur', 'les', 'leurs', 'eux', "s'", 'elle-même', 'lui-même', 'sienne', 'sien', 'sienne', 'siennes','un', 'une', "l' autre", 'tous', 'celui-ci', 'duquel', 'celle', 'celui'],
                               "4": ['qui', 'que', 'dont', "qu'"]}

    # Reverse the dictionary to map each word to its grammatical person
    word_to_person = {word: person for person, words in grammatical_person_dict.items() for word in words}

    # Map entities_df['text'].str.lower() to grammatical persons
    entities_df['grammatical_person'] = entities_df['text'].str.lower().map(word_to_person).fillna("3").astype(int)
    return entities_df
def get_one_hot_encoded_features(mention_pairs_df, entities_df, features=['prop', 'head_dependency_relation', 'gender', 'number', 'grammatical_person']):
    one_hot_encoding_dict = {"prop" : ["NOM", "PROP", "PRON"],
                             "head_dependency_relation": ["ROOT", "acl", "acl:relcl", "advcl", "advmod", "amod", "appos", "aux:pass", "aux:tense", "case", "cc", "ccomp", "conj", "cop", "dep", "det", "expl:comp", "expl:pass", "expl:subj", "fixed", "flat:foreign", "flat:name", "iobj", "mark", "nmod", "nsubj", "nsubj:pass", "nummod", "obj", "obl:agent", "obl:arg", "obl:mod", "parataxis", "punct", "vocative", "xcomp"],
                             "gender": ["Male", "Female", "Ambiguous", 'Not_Assigned'],
                             "number": ["Singular", "Plural", "Ambiguous", 'Not_Assigned'],
                             "grammatical_person" : [1, 2, 3, 4],
                             }
    columns = list(one_hot_encoding_dict.keys())
    features = [column for column in columns if column in features]
    if 'grammatical_person' in features:
        entities_df = assign_grammatical_person(entities_df)

    # Extract infos for each mention in the mention pair
    for mention_polarity in ["A", "B"]:
        mention_pairs_df = mention_pairs_df.merge(
        entities_df[features].add_prefix(f"{mention_polarity}_"),
        left_on=mention_polarity,
        right_index=True,
        how='left')

    for mention_polarity in ["A", "B"]:
        for feature in features:
            possible_values = one_hot_encoding_dict[feature]
            dummy_values = pd.get_dummies(mention_pairs_df[f"{mention_polarity}_{feature}"].tolist() + possible_values)[:len(mention_pairs_df)] * 1
            dummy_values = dummy_values.add_prefix(f"{mention_polarity}_{feature}_")
            mention_pairs_df[dummy_values.columns] = dummy_values

    mention_pairs_df.drop([f"{mention_polarity}_{feature}" for feature in features for mention_polarity in ["A", "B"]], axis=1, inplace=True)

    return mention_pairs_df
def convert_mention_pairs_df_to_features_array(mention_pairs_df):
    features_columns = sorted([column for column in mention_pairs_df.columns if column not in ["A", "B"]])
    mention_pairs_df = mention_pairs_df[features_columns]
    # features_array = mention_pairs_df.values
    features_array = mention_pairs_df.values.astype(np.float32)  # Specify float32 here
    return features_array

def generate_mention_pairs_features_array(mention_pairs_df, PER_entities_df, features=['mention_len', 'start_token_ID_within_sentence', 'mention_ID_delta', 'start_token_delta', 'end_token_delta', 'paragraph_ID_delta', 'sentence_ID_delta', 'out_to_in_nested_level_delta', 'shared_token_ratio', 'text_match', 'head_text_match', 'syntactic_head_match', 'prop', 'head_dependency_relation', 'gender', 'number', 'grammatical_person']):
    mention_pairs_df = add_mentions_infos(mention_pairs_df, PER_entities_df, features=features)
    mention_pairs_df = get_mention_pairs_distance_features(mention_pairs_df, PER_entities_df, features=features)
    mention_pairs_df = get_text_and_syntactic_match_features(mention_pairs_df, PER_entities_df, features=features)
    mention_pairs_df = get_one_hot_encoded_features(mention_pairs_df, PER_entities_df, features=features)
    features_array = convert_mention_pairs_df_to_features_array(mention_pairs_df)
    return features_array



### Train coreference resolution
import tensorflow as tf
from keras.losses import BinaryFocalCrossentropy
import tensorflow.keras.backend as K
from tensorflow import keras
from tensorflow.keras import layers, callbacks
import random
from time import time
from keras.optimizers import Adam
from keras.models import load_model

def get_mention_pairs_gold_labels(mention_pairs_df, entities_df):
    # Create a dictionary mapping each entity index to its COREF value
    coref_dict = entities_df['COREF'].to_dict()

    # Map COREF values directly using the dictionary
    mention_pairs_df['A_COREF'] = mention_pairs_df['A'].map(coref_dict)
    mention_pairs_df['B_COREF'] = mention_pairs_df['B'].map(coref_dict)

    # Calculate gold labels
    labels_array = (mention_pairs_df['A_COREF'] == mention_pairs_df['B_COREF']).astype(int).to_numpy()

    return labels_array
class DataGenerator(Sequence):
    def __init__(self, generator_model_data=None, batch_size=32, shuffle=False, **kwargs):
        super().__init__(**kwargs)

        self.overall_mention_pairs_df = generator_model_data['overall_mention_pairs_df']
        self.overall_PER_mentions_embeddings_tensor = tf.convert_to_tensor(
            generator_model_data['overall_PER_mentions_embeddings_tensor'], dtype=tf.float32)
        # generator_model_data['overall_features_tensor'] = generator_model_data['overall_features_tensor'].astype(np.float32)
        self.overall_features_tensor = tf.convert_to_tensor(generator_model_data['overall_features_tensor'],
                                                            dtype=tf.float32)
        self.overall_labels_tensor = tf.convert_to_tensor(generator_model_data['overall_labels_tensor'],
                                                          dtype=tf.float32)

        self.batch_size = batch_size
        self.shuffle = shuffle

        # Get the mentions pair ids
        self.mention_pair_ids = np.arange(len(self.overall_mention_pairs_df))

        if self.shuffle:
            np.random.shuffle(self.mention_pair_ids)

    def __len__(self):
        return int(np.ceil(len(self.mention_pair_ids) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_indices = self.mention_pair_ids[idx * self.batch_size:(idx + 1) * self.batch_size]

        # Accessing IDs as tensors
        A_ids = self.overall_mention_pairs_df[batch_indices, 0]
        B_ids = self.overall_mention_pairs_df[batch_indices, 1]

        # Get embeddings and features as tensors
        A_embeddings = tf.gather(self.overall_PER_mentions_embeddings_tensor, A_ids)
        B_embeddings = tf.gather(self.overall_PER_mentions_embeddings_tensor, B_ids)
        features = tf.gather(self.overall_features_tensor, batch_indices)

        # Concatenate using TensorFlow
        X_batch = tf.concat([A_embeddings, B_embeddings, features], axis=1)
        y_batch = tf.gather(self.overall_labels_tensor, batch_indices)

        return X_batch, y_batch  # Return as tensors

    def on_epoch_end(self):
        if self.shuffle:
            np.random.shuffle(self.mention_pair_ids)
        gc.collect()
        K.clear_session()
def training_model(train_data,
                   validation_data,
                   batch_size=8000,
                   layers_number=3,
                   layers_units=1900,
                   dropout=0.5,
                   l2_regularization=0,
                   learning_rate=0.0005,
                   patience=10,
                   max_epochs=100,
                   focal_crossentropy_gamma=1.2,
                   run_eagerly=False,
                   verbose=2,
                   mixed_precision_global_policy="mixed_float16",
                   set_memory_growth=False,
                   optimizer_set_jit=True):
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, set_memory_growth)
    tf.keras.mixed_precision.set_global_policy(mixed_precision_global_policy)
    tf.config.optimizer.set_jit(optimizer_set_jit)

    model_training_start_time = time()

    # Create training and validation generators
    train_generator = DataGenerator(generator_model_data=train_data,
                                    batch_size=batch_size,
                                    shuffle=True)
    validation_generator = DataGenerator(generator_model_data=validation_data,
                                         batch_size=batch_size,
                                         shuffle=False)

    local_model = keras.Sequential()
    # Add the Input layer to define the input shape
    local_model.add(keras.Input(shape=[train_generator[0][0].shape[1]]))
    # Add the first dense layer
    local_model.add(
        layers.Dense(units=layers_units, activation="relu", kernel_regularizer=keras.regularizers.l2(l2_regularization),
                     name='dense_1'))
    local_model.add(layers.Dropout(dropout, name='dropout_1'))
    # Add the remaining dense and dropout layers alternately
    for i in range(2, layers_number + 1):  # Start from 2 since dense_1 is already added
        local_model.add(layers.Dense(units=layers_units, activation="relu",
                                     kernel_regularizer=keras.regularizers.l2(l2_regularization),
                                     name=f'dense_{i}'))
        local_model.add(layers.Dropout(dropout, name=f'dropout_{i}'))
    # Add the output layer
    local_model.add(layers.Dense(1, activation='sigmoid', name='output_layer'))

    early_stopping = callbacks.EarlyStopping(
        min_delta=0.0005,  # minimium amount of change to count as an improvement
        patience=patience,  # how many epochs to wait before stopping
        restore_best_weights=True,
    )
    reduce_lr = keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=4, min_lr=1e-6, verbose=1)

    local_model.compile(
        optimizer=Adam(learning_rate=learning_rate, clipnorm=1),
        # optimizer=Adam(learning_rate=learning_rate, clipnorm=5),
        # optimizer=Adam(learning_rate=learning_rate),
        loss=BinaryFocalCrossentropy(gamma=focal_crossentropy_gamma),
        metrics=['binary_accuracy'],
        run_eagerly=run_eagerly,
    )

    # Fit the model
    history = local_model.fit(
        train_generator,
        epochs=max_epochs,
        validation_data=validation_generator,
        callbacks=[early_stopping, reduce_lr],
        verbose=verbose,
    )

    history_df = pd.DataFrame(history.history)

    model_training_time = time() - model_training_start_time

    def clear_generators(generator):
        del generator.overall_mention_pairs_df
        del generator.overall_PER_mentions_embeddings_tensor
        del generator.overall_features_tensor
        del generator.overall_labels_tensor
        gc.collect()
        K.clear_session()

    # Clear generators after each iteration to free memory
    clear_generators(train_generator)
    clear_generators(validation_generator)
    del train_generator, train_data, history, validation_generator, validation_data
    gc.collect()
    K.clear_session()
    gc.collect()

    return local_model, history_df, model_training_time

### Coreference_resolution
def get_mention_pairs_coreference_predictions(coreference_model, model_data_dict, batch_size=10000):
    test_generator = DataGenerator(
            generator_model_data=model_data_dict,
            batch_size=batch_size,
        )

    predictions = []

    # Iterate through the generator to get each batch
    for i in tqdm(range(len(test_generator)), leave=False, desc="Predicting Coreference Pairs"):  # Number of batches in the generator
        X_batch, y_batch = test_generator[i]  # Fetch each batch
        batch_predictions = coreference_model.predict(X_batch, verbose=0)
        predictions.append(batch_predictions)

    predictions = np.concatenate(predictions, axis=0)

    K.clear_session()
    del coreference_model, model_data_dict
    gc.collect()

    return predictions

### Evaluate Coreference Resolution
import json
import subprocess
def initialize_gold_coreference_matrix_from_entities_df(entities_df):
    COREF_array = np.array(entities_df['COREF'])
    # Create an outer comparison of the COREF array with itself
    gold_coreference_matrix = np.equal.outer(COREF_array, COREF_array).astype(int)
    # Convert True/False to 1/-1
    gold_coreference_matrix = np.where(gold_coreference_matrix, 1, -1)
    return gold_coreference_matrix
def extract_mentions_and_links_from_coreference_matrix(matrix):
    matrix_size = matrix.shape[0]
    mentions = list(range(matrix_size))
    minimal_links = []
    treated_mentions = []

    for i in range(matrix_size):
        minimal_links.append([i, i])
        if i not in treated_mentions:
            treated_mentions.append(i)
            for j in range(i + 1, matrix_size):
                if matrix[i, j] == 1:
                    minimal_links.append([i, j])
                    treated_mentions.append(j)

    return mentions, minimal_links
def coreference_resolution_metrics(gold_coreference_matrix, predicted_coreference_matrix):
    # Define your gold and sys dictionaries
    gold = {"type": "graph",
            "mentions": [],
            "links": []
            }

    predicted = {"type": "graph",
                 "mentions": [],
                 "links": []
                 }

    gold['mentions'], gold['links'] = extract_mentions_and_links_from_coreference_matrix(gold_coreference_matrix)
    predicted['mentions'], predicted['links'] = extract_mentions_and_links_from_coreference_matrix(predicted_coreference_matrix)

    # Save the gold dictionary as gold.json
    with open('gold.json', 'w') as gold_file:
        json.dump(gold, gold_file, indent=4)

    # Save the sys dictionary as sys.json
    with open('predicted.json', 'w') as predicted_file:
        json.dump(predicted, predicted_file, indent=4)

    # Define the command to run
    command = ["scorch", "gold.json", "predicted.json"]

    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

    input_string = result.stdout
    # Split the string into lines
    lines = input_string.strip().split('\n')

    # Initialize an empty dictionary
    result_dict = {}

    # Iterate over each line and process it
    for line in lines:
        # Split the line into key and the rest of the metrics
        key, metrics = line.split(':', 1)

        # Further split the metrics part into individual metric components
        metrics_dict = {}
        for metric in metrics.strip().split('\t'):
            metric_key, metric_value = metric.split('=')
            metrics_dict[metric_key] = float(metric_value)

        # Add the metrics dictionary to the result dictionary
        result_dict[key] = metrics_dict

    # Display the resulting dictionary
    coreference_metrics_df = pd.DataFrame(result_dict).T
    coreference_metrics_df.columns = ['Recall', 'Precision', 'F1-Score']
    coreference_metrics_df = coreference_metrics_df[['Precision', 'Recall', 'F1-Score']]
    coreference_metrics_df.loc['CONLL'] = coreference_metrics_df.loc[['MUC', 'B³', 'CEAF_e']].mean()

    return coreference_metrics_df