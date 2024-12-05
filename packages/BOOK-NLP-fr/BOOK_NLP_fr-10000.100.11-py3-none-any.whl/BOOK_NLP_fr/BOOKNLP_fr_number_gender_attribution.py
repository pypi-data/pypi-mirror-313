from .BOOKNLP_fr_number import assign_number_to_PER_entities
from .BOOKNLP_fr_gender import assign_gender_to_PER_entities

import pkg_resources

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
