from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from tqdm.auto import tqdm
import pandas as pd

## Get BERT embeddings from tokens_df
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

def load_tokenizer_and_embedding_model(model_name="almanach/camembert-base"):

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name, output_hidden_states=True)
    print(f"Tokenizer and Embedding Model Initialized: {model_name}")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    return tokenizer, model
def get_embedding_tensor_from_tokens_df(tokens_df, tokenizer, model, sliding_window_size='max', mini_batch_size=10,
                                        sliding_window_overlap=0.5, first_last_average=True, device=None):
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # model_max_length = model.config.max_position_embeddings
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