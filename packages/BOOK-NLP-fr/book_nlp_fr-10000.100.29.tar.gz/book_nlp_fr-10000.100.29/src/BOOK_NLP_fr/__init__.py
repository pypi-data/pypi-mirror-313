import pandas as pd

from .BookNLP_fr_load_save_functions import load_sacr_file, load_text_file, save_text_file, load_tokens_df, save_tokens_df, load_entities_df, save_entities_df, clean_text
from .BookNLP_fr_add_entities_features import add_features_to_entities
from .BookNLP_fr_generate_tokens_df import load_spacy_model, generate_tokens_df
from .BookNLP_fr_generate_tokens_and_entities_from_sacr import generate_tokens_and_entities_from_sacr
from .BookNLP_fr_generate_tokens_embeddings_tensor import load_tokenizer_and_embedding_model, get_embedding_tensor_from_tokens_df
from .BookNLP_fr_mentions_detection_module import mentions_detection_LOOCV_full_model_training, generate_model_card_from_LOOCV_directory, load_mentions_detection_model, generate_entities_df
from .BookNLP_fr_mentions_detection_module import LockedDropout, Highway, NERModel


# from .BookNLP_fr import (
#                         load_spacy_model, generate_tokens_df,
#                         load_mentions_detection_models, predict_entities_from_tokens_df,
#                         load_tokenizer_and_embedding_model, get_embedding_tensor_from_tokens_df,
#                         get_mentions_embeddings,
#                         add_infos_to_entities,
#                         initialize_gold_coreference_matrix_from_entities_df,
#                         extract_mentions_and_links_from_coreference_matrix, coreference_resolution_metrics,
#                         initialize_mention_pairs_df, generate_mention_pairs_features_array, get_mention_pairs_gold_labels,
#                         generate_coreference_resolution_training_dict, generate_split_data, get_mention_pairs_coreference_predictions,
#                         DataGenerator, training_model)

# Inside BOOK_NLP_fr/__init__.py
print("BOOK_NLP_fr package loaded successfully.")




