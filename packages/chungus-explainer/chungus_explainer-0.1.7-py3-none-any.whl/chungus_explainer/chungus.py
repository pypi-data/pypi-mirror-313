import numpy as np
import pandas as pd
import ipywidgets as widgets
from IPython.display import display, clear_output
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage


def bins(feature_values, num_bins=15):
    """
    Create bins for the given feature values.
    
    Args:
    - feature_values: A pandas Series or numpy array of feature values.
    - num_bins: Number of bins to create (default is 15 for continuous features).
    
    Returns:
    - binned_values: An array of binned values.
    """
    if pd.api.types.is_numeric_dtype(feature_values):
        # Use specified number of bins for continuous values
        binned_values = pd.cut(feature_values, bins=num_bins, labels=False, duplicates="drop")
    else:
        # Use unique categories for discrete values
        binned_values = pd.factorize(feature_values)[0]
    return binned_values



def shap_to_json(feature_names, shap_values, feature_values, num_bins=15):
    """
    Entry point for generating SHAP JSON for both classifiers and regressors.
    """
    try:
        # Extract SHAP values if they are inside an Explanation object
        shap_values_array = shap_values.values if hasattr(shap_values, 'values') else shap_values

        # Check SHAP values shape
        print("SHAP values type:", type(shap_values_array))
        print("SHAP values shape:", shap_values_array.shape)

        shap_data = {}

        # Determine if SHAP values are 3D (multi-class) or 2D (regressor or binary classification)
        is_multi_class = len(shap_values_array.shape) == 3
        num_classes = shap_values_array.shape[2] if is_multi_class else 1

        for idx, feature_name in enumerate(feature_names):
            binned_features = bins(feature_values.iloc[:, idx], num_bins=num_bins)

            # Collect SHAP data for each class or single output
            feature_shap_data = {}
            for class_idx in range(num_classes):
                class_shap_data = {}
                for bin_idx in np.unique(binned_features):
                    bin_mask = binned_features == bin_idx

                    # Validate bin_mask
                    if bin_mask.sum() == 0:
                        continue

                    # Apply mask to SHAP values
                    if is_multi_class:
                        bin_shap_values = shap_values_array[bin_mask, idx, class_idx]
                    else:
                        bin_shap_values = shap_values_array[bin_mask, idx]

                    # Validate SHAP values for the bin
                    if bin_shap_values.size > 0:
                        class_shap_data[f"Bin {bin_idx}"] = {
                            "SHAP Values": bin_shap_values.tolist(),
                            "Mean Feature Value": feature_values.loc[bin_mask, feature_values.columns[idx]].mean(),
                        }
                if is_multi_class:
                    feature_shap_data[f"Class {class_idx}"] = class_shap_data
                else:
                    feature_shap_data = class_shap_data  # Single output

            shap_data[feature_name] = feature_shap_data

        # Convert to JSON
        return json.dumps(shap_data, indent=4)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
    
    
def shap_to_json_classifier(feature_names, shap_values, feature_values, num_bins=15):
    """
    Generate JSON for classifiers using SHAP values and feature statistics, including shap value ranges.

    Args:
    - feature_names: List of feature names.
    - shap_values: SHAP values (3D array for classifiers, with shape [n_samples, n_features, n_classes]).
    - feature_values: DataFrame or array of feature values.
    - num_bins: Number of bins for discretizing feature values.

    Returns:
    - shap_json_output: A JSON object containing binned SHAP statistics and shap value ranges.
    """
    try:
        # Extract SHAP values if they are inside an Explanation object
        shap_values_array = shap_values.values if hasattr(shap_values, 'values') else shap_values

        # Check if SHAP values are for multi-class classification
        num_classes = shap_values_array.shape[2]

        shap_data = {}

        for idx, feature_name in enumerate(feature_names):
            # Create bins for the feature
            binned_features = bins(feature_values.iloc[:, idx], num_bins=num_bins)

            # Collect SHAP data for each class and bin
            feature_shap_data = {}
            for class_idx in range(num_classes):  # Iterate through each class
                class_shap_data = {}
                for bin_idx in np.unique(binned_features):
                    bin_mask = binned_features == bin_idx

                    # Extract SHAP values for the current feature and class
                    bin_shap_values = shap_values_array[bin_mask, idx, class_idx]

                    # Add SHAP statistics to JSON if there are values in the bin
                    if bin_shap_values.size > 0:
                        class_shap_data[f"Bin {bin_idx}"] = {
                            "SHAP Values High": np.percentile(bin_shap_values, 75),  # Highest SHAP value
                            "SHAP Values Low": np.percentile(bin_shap_values, 25),   # Lowest SHAP value
                            "Mean Feature Value": feature_values.loc[bin_mask, feature_values.columns[idx]].mean(),
                            "Mean Shap Value": bin_shap_values.mean()   # Mean SHAP value
                        }

                # Add data for the class to the feature data
                feature_shap_data[f"Class {class_idx}"] = class_shap_data

            # Add feature data to the JSON
            shap_data[feature_name] = feature_shap_data

        # Convert to JSON
        return json.dumps(shap_data, indent=4)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
    
    
def shap_to_json_regressor(feature_names, shap_values, feature_values, num_bins=15):
    """
    Generate JSON for regressors using SHAP values and feature statistics, including shap value ranges.

    Args:
    - feature_names: List of feature names.
    - shap_values: SHAP values (2D array for regressors).
    - feature_values: DataFrame or array of feature values.
    - num_bins: Number of bins for discretizing feature values.

    Returns:
    - shap_json_output: A JSON object containing binned SHAP statistics and shap value ranges.
    """
    try:
        # Extract SHAP values if they are inside an Explanation object
        shap_values_array = shap_values.values if hasattr(shap_values, 'values') else shap_values

        shap_data = {}

        for idx, feature_name in enumerate(feature_names):
            # Create bins for the feature
            binned_features = bins(feature_values.iloc[:, idx], num_bins=num_bins)

            # Collect SHAP data for each bin
            feature_shap_data = {}
            for bin_idx in np.unique(binned_features):
                bin_mask = binned_features == bin_idx

                # Extract SHAP values for the current bin
                bin_shap_values = shap_values_array[bin_mask, idx]

                # Add SHAP statistics to JSON if there are values in the bin
                if bin_shap_values.size > 0:
                    feature_shap_data[f"Bin {bin_idx}"] = {
                        "SHAP Values High": np.percentile(bin_shap_values, 75),  # Highest SHAP value
                        "SHAP Values Low": np.percentile(bin_shap_values, 25),   # Lowest SHAP value
                        "Mean Feature Value": feature_values.loc[bin_mask, feature_values.columns[idx]].mean(),
                        "Mean Shap Value": bin_shap_values.mean()   # Mean SHAP value
                    }

            # Add feature data to the JSON
            shap_data[feature_name] = feature_shap_data

        # Convert to JSON
        return json.dumps(shap_data, indent=4)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
    
    
def chatgpt(shap_json_context, llm):
    """
    Create an interactive chatbox to analyze SHAP values using ChatGPT.
    
    Args:
    - shap_json_context: JSON string containing SHAP values and feature statistics.
    - llm: An instance of ChatOpenAI initialized with the desired model and API key.
    
    Returns:
    - None. Displays an interactive chatbox in the notebook.
    """
    # Initialize output box for chat responses
    output_box = widgets.Output(layout={"border": "1px solid black", "width": "100%"})
    
    # Input box for user questions
    user_input = widgets.Textarea(
        value="",
        placeholder="Type your question about the SHAP values here...",
        description="You:",
        layout=widgets.Layout(width="100%", height="100px"),
    )
    
    # Display user input and output box
    display(user_input, output_box)
    
    # Function to handle user input and send to ChatGPT
    def send_message_to_chatgpt(user_message):
        # Define the conversation context
        conversation_context = [
            SystemMessage(
                content=(
                    "You are a Data Scientist proficient in analyzing Shapley values. "
                    "The dataset is about features that influence model predictions. "
                    "Positive SHAP values indicate an increased likelihood of an outcome, "
                    "while negative SHAP values indicate a decreased likelihood. "
                    "Interpret the SHAP values clearly for unfamiliar users."
                )
            ),
            SystemMessage(content=f"Here are the SHAP values and statistics: {shap_json_context}"),
            HumanMessage(content=user_message),
        ]
        
        # Get response from ChatGPT using `invoke`
        ai_response = llm.invoke(conversation_context)
        
        # Display the conversation
        with output_box:
            clear_output(wait=True)
            print(f"Human: {user_message}")
            print(f"AI: {ai_response.content}\n")
    
    # Handle input submission
    def send_message(event):
        if event["new"].endswith("\n"):
            user_message = user_input.value.strip()
            if user_message:
                send_message_to_chatgpt(user_message)
                user_input.value = ""  # Clear input box
    
    # Bind function to user input
    user_input.observe(send_message, names="value")