## Mentions Detection - Generate entities_df from tokens_df

import pickle
import requests
import os

def load_mentions_detection_model(model_path="AntoineBourgois/bookNLP-fr_NER"):
    """
    mentions_detection_model = load_mentions_detection_model(model_path="AntoineBourgois/bookNLP-fr_NER")
    """
    try:
        # Check if the model exists locally
        if os.path.exists(model_path):
            print(f"Loading mentions detection model from {os.path.abspath(model_path)}...")
            with open(model_path, "rb") as file:
                mentions_detection_model = pickle.load(file)
        else:
            print(f"Model not found locally. Downloading from HuggingFace: https://huggingface.co/{model_path}")
            url_model_path = f"https://huggingface.co/{model_path}/resolve/main/pytorch_model.bin"

            response = requests.get(url_model_path)
            response.raise_for_status()  # Ensure the request was successful

            # Deserialize the model from the downloaded content
            mentions_detection_model = pickle.loads(response.content)

            # Ensure the directory exists
            directory = os.path.dirname(model_path)
            absolute_directory = os.path.abspath(directory)  # Get the full absolute path
            if not os.path.exists(absolute_directory):
                os.makedirs(absolute_directory)

            print(f"Saving model locally to: {absolute_directory}")

            # Save the model locally for future use
            with open(model_path, "wb") as file:
                pickle.dump(mentions_detection_model, file)

        return mentions_detection_model

    except requests.exceptions.RequestException as req_err:
        print(f"Error downloading model from HuggingFace: {req_err}")
    except pickle.UnpicklingError as pickle_err:
        print(f"Error unpickling the model: {pickle_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

