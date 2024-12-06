#%%
from .BookNLP_fr_load_save_functions import load_sacr_file, clean_text, save_text_file, save_tokens_df, save_entities_df
from .BookNLP_fr_generate_tokens_df import load_spacy_model, generate_tokens_df
from .BookNLP_fr_add_entities_features import add_features_to_entities
#%%
import re
import pandas as pd
from tqdm.auto import tqdm  # notebook compatible
import os
#%%
def remove_sacr_metadata(sacr_content):
    #Remove color and tokenization metadata from the end of SACR files
    sacr_metadata_index = sacr_content.find("#COLOR") if sacr_content.find("#COLOR") != -1 else sacr_content.find("#TOKENIZATION-TYPE")
    if sacr_metadata_index != -1:
        sacr_content = sacr_content[:sacr_metadata_index].rstrip()
    sacr_content = sacr_content.strip()
    return sacr_content
def replace_entities_tags(sacr_content, cat_replace_dict):
    for sacr_label in cat_replace_dict.keys():
        new_label = cat_replace_dict[sacr_label]
        sacr_content = sacr_content.replace(f':EN="{sacr_label}" ', f':EN="{new_label}" ')
    return sacr_content
def remove_sacr_annotations(sacr_content):
    # Remove all substrings matching the mention_oppening_pattern
    mention_oppening_pattern = r'\{[A-Za-z0-9_-]+:EN="([^"]*)"+ '
    raw_text = re.sub(mention_oppening_pattern, "", sacr_content)
    # Remove all '}' mention_closing characters
    raw_text = raw_text.replace('}', '')
    return raw_text
def extract_entities(sacr_content):
    # extracting indices of mentions span boundaries
    opening_indices = [i for i, char in enumerate(sacr_content) if char == '{']
    
    entities_dict = []
    
    for opening_index in opening_indices:
        end_index = opening_index+1
        while len([i for i, char in enumerate(sacr_content[opening_index:end_index]) if char == '{']) != len([i for i, char in enumerate(sacr_content[opening_index:end_index]) if char == '}']):
            end_index += 1
            
        raw_text = sacr_content[opening_index:end_index]
        text = remove_sacr_annotations(raw_text)
        entity_type = re.search(r':EN="([^"]*)"', raw_text).group(1)
        coref_name = re.search(r'{([^:}]*)', raw_text).group(1)
            
        entities_dict.append({'SACR_start_id': opening_index,
                              'SACR_end_id': end_index,
                              'raw_text': raw_text,
                              # 'text': text,
                              'cat': entity_type,
                              'COREF_name': coref_name})
    
    entities_df = pd.DataFrame(entities_dict)
    return entities_df
def convert_annotated_ids_to_raw_ids(opening_indices, closing_indices, sacr_content):
    raw_indices_lists = []
    annotated_to_raw_index_dict = {}
    
    for indices_list in [opening_indices, closing_indices]:
        raw_ids_list = []
        for annotated_index in indices_list:
            max_known_index = max([v for v in annotated_to_raw_index_dict.keys() if v < annotated_index], default=None)
            if max_known_index:
                raw_text_known_index = annotated_to_raw_index_dict[max_known_index]
                delta = len(clean_text(remove_sacr_annotations(sacr_content[max_known_index:annotated_index])))
                raw_index = raw_text_known_index + delta
            else:
                raw_index = len(remove_sacr_annotations(sacr_content[:annotated_index]))
            
            annotated_to_raw_index_dict[annotated_index] = raw_index
            raw_ids_list.append(raw_index)
        
        raw_indices_lists.append(raw_ids_list)
        
    raw_text_opening_indices, raw_text_closing_indices = raw_indices_lists[0], raw_indices_lists[1]
    return raw_text_opening_indices, raw_text_closing_indices
def add_tokens_infos_to_entities(entities_df, tokens_df, sacr_content):
    byte_onset, byte_offset = convert_annotated_ids_to_raw_ids(entities_df['SACR_start_id'], entities_df['SACR_end_id'], sacr_content)
    entities_df['byte_onset'] = byte_onset
    entities_df['byte_offset'] = byte_offset
    
    start_tokens, end_tokens, text_list  = [], [], []
    for byte_onset, byte_offset in entities_df[['byte_onset', 'byte_offset']].values:
        sample_tokens_df = tokens_df[(tokens_df['byte_offset'] > byte_onset) & (tokens_df['byte_onset'] < byte_offset)]
        
        token_ids = sample_tokens_df['token_ID_within_document'].tolist()
        start_token, end_token = token_ids[0], token_ids[-1]
        start_tokens.append(start_token)
        end_tokens.append(end_token)
        text_list.append(' '.join(sample_tokens_df['word'].tolist()))
        
    entities_df['start_token'] = start_tokens
    entities_df['end_token'] = end_tokens
    entities_df['text'] = text_list
    
    return entities_df
def reorder_coref_ids(entities_df):
    COREF_column = 'COREF_name'
    # Group by 'COREF' column and aggregate
    grouped_entities_df = entities_df.groupby(COREF_column).agg(
        Count=(COREF_column, 'size'),
        coref_cat=('cat', lambda x: x.value_counts().idxmax())  # Inline lambda function for most frequent value
    ).reset_index()
    # Sorting by mention count
    grouped_entities_df = grouped_entities_df.sort_values(by=['Count'], ascending=[False])#.drop(columns=['cat_priority'])

    grouped_entities_df = grouped_entities_df.reset_index(drop=True)
    grouped_entities_df['new_COREF'] = grouped_entities_df.index
    COREF_converter = dict(zip(grouped_entities_df[COREF_column], grouped_entities_df['new_COREF']))
    
    entities_df['COREF'] = entities_df[COREF_column].map(COREF_converter)
    
    return entities_df
#%%
def generate_tokens_and_entities_from_sacr(file_name, files_directory,
                                                 end_directory=None,
                                                 spacy_model=None,
                                                 max_char_sentence_length=75000,
                                                 cat_replace_dict=None):
    # print(SACR_file_name)
    if cat_replace_dict is None:
        cat_replace_dict = {"f FAC": "FAC",
                            "g GPE": "GPE",
                            "h HIST": "TIME",
                            "l LOC": "LOC",
                            "m METALEPSE": "PER",
                            "n NO_PER": "PER",
                            "o ORG": "ORG",
                            "p PER": "PER",
                            "t TIME": "TIME",
                            "v VEH": "VEH",
                            "": "PER",
                            }
    if spacy_model == None:
        spacy_model = load_spacy_model(model_name='fr_dep_news_trf', model_max_length=500000)

    if end_directory==None:
        end_directory = files_directory
        
    sacr_content = load_sacr_file(file_name, files_directory=files_directory, extension=".sacr")
    sacr_content = remove_sacr_metadata(sacr_content)
    sacr_content = clean_text(sacr_content)
    sacr_content = replace_entities_tags(sacr_content, cat_replace_dict)
    
    recovered_txt_file_content = remove_sacr_annotations(sacr_content)
    recovered_txt_file_content = clean_text(recovered_txt_file_content)
    
    save_text_file(recovered_txt_file_content, file_name, files_directory=end_directory, extension=".txt")
    
    tokens_df = generate_tokens_df(recovered_txt_file_content, spacy_model, max_char_sentence_length=max_char_sentence_length)
    entities_df = extract_entities(sacr_content)
    entities_df = add_tokens_infos_to_entities(entities_df, tokens_df, sacr_content)
        
    entities_df = reorder_coref_ids(entities_df)
    # # print(entities_df['cat'].unique())
    entities_df = entities_df[['COREF_name', 'COREF', 'start_token', 'end_token', 'cat', 'text']]
    
    entities_df = add_features_to_entities(entities_df, tokens_df)

    entities_df = entities_df[['COREF_name', 'COREF', 'start_token', 'end_token', 'cat', 'text', 'prop', 'number', 'gender', 'head_word', 'mention_len', 'head_dependency_relation', 'in_to_out_nested_level', 'out_to_in_nested_level','nested_entities_count', 'paragraph_ID', 'sentence_ID', 'start_token_ID_within_sentence', 'POS_tag', 'head_id', 'head_syntactic_head_ID']]
    # print(Counter(entities_df['cat']))


    # remove tokens after the last sentence with annotated entity // allow to filter partially anotated SACR files, can continue annotations at anny given time
    last_annotated_sentence = tokens_df.loc[entities_df['end_token'].max(), 'sentence_ID']
    tokens_df = tokens_df[tokens_df['sentence_ID'] <= last_annotated_sentence]
    
    
    
    save_tokens_df(tokens_df, end_directory, file_name, extension=".tokens")
    save_entities_df(entities_df, end_directory, file_name, extension=".entities")


# #%%
# spacy_model = load_spacy_model(model_name='fr_dep_news_trf', model_max_length=500000)
# #%%
# files_directory = '/home/antoine/Documents/bookBLP_modular_development/chapitre_francesca_2024_11'
#
# extension = ".sacr"
# SACR_files = sorted([f.replace(extension, "") for f in os.listdir(files_directory) if f.endswith(extension)])
#
# cat_replace_dict = {"f FAC": "FAC",
#                     "g GPE": "GPE",
#                     "h HIST": "TIME",
#                     "l LOC": "LOC",
#                     "m METALEPSE": "PER",
#                     "n NO_PER": "PER",
#                     "o ORG": "ORG",
#                     "p PER": "PER",
#                     "t TIME": "TIME",
#                     "v VEH": "VEH",
#                     "": "PER",
#                     }
#
# for file_name in tqdm(SACR_files, desc='Generating .tokens and .entities files from .sacr files'):
#     generate_tokens_df_and_entities_df_from_sacr(file_name, files_directory, spacy_model=spacy_model, max_char_sentence_length=50000, cat_replace_dict=cat_replace_dict)
# #%%
