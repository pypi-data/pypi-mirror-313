from langchain.schema import SystemMessage, HumanMessage
import pandas as pd
import numpy as np

def data_validation(dataset, llm, max_categories=5):
    """
    Perform data validation using LangChain and GPT-4o-mini model, and return a user-friendly summary.

    Args:
        api_key (str): OpenAI API key for accessing the GPT-4o-mini model.
        dataset (pd.DataFrame): The dataset to validate.
        max_categories (int): Maximum number of top categories to display for categorical trends.

    Returns:
        str: A formatted summary of data validation results.
    """

    # Prepare summary statistics for numeric and categorical columns
    numeric_columns = dataset.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = dataset.select_dtypes(exclude=[np.number]).columns.tolist()
    
    # Initial validation dictionary
    validation_results = {
        "data_types": {},
        "missing_values": {},
        "outliers": {},
        "trends": {},
    }
    
    # Identify data types
    for column in dataset.columns:
        if column in numeric_columns:
            validation_results["data_types"][column] = "Numeric"
        elif column in categorical_columns:
            validation_results["data_types"][column] = "Categorical"
        else:
            validation_results["data_types"][column] = "Other"

    # Check for missing values
    validation_results["missing_values"] = dataset.isnull().mean().to_dict()

    # Detect outliers for numeric columns
    for column in numeric_columns:
        q1 = dataset[column].quantile(0.25)
        q3 = dataset[column].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outliers = dataset[(dataset[column] < lower_bound) | (dataset[column] > upper_bound)]
        validation_results["outliers"][column] = {
            "num_outliers": outliers.shape[0],
            "outlier_percentage": len(outliers) / len(dataset) * 100,
        }

    # Analyze trends in categorical columns
    for column in categorical_columns:
        top_categories = dataset[column].value_counts().head(max_categories).to_dict()
        validation_results["trends"][column] = top_categories

    # Generate a prompt for GPT-4o-mini to validate data
    prompt = (
        "You are a data validator. The following are summaries of a dataset.\n\n"
        "Data Types:\n" + str(validation_results["data_types"]) + "\n\n"
        "Missing Values (as percentages):\n" + str(validation_results["missing_values"]) + "\n\n"
        "Outliers:\n" + str(validation_results["outliers"]) + "\n\n"
        "Trends in Categorical Data:\n" + str(validation_results["trends"]) + "\n\n"
        "Based on this information, validate the dataset and identify potential data quality issues."
    )
    
    # Use LangChain LLM to provide insights with invoke
    try:
        messages = [
            SystemMessage(content="You are a data analysis assistant."),
            HumanMessage(content=prompt)
        ]
        response = llm.invoke(messages)
        validation_results["gpt_response"] = response.content
    except Exception as e:
        validation_results["gpt_response"] = f"Error occurred: {str(e)}"

    # Format the results for better readability
    formatted_results = "DATA VALIDATION SUMMARY\n\n"
    formatted_results += "1. Data Types:\n"
    for col, dtype in validation_results["data_types"].items():
        formatted_results += f"   - {col}: {dtype}\n"

    formatted_results += "\n2. Missing Values:\n"
    for col, missing_pct in validation_results["missing_values"].items():
        formatted_results += f"   - {col}: {missing_pct:.2%} missing\n"

    formatted_results += "\n3. Outliers:\n"
    for col, stats in validation_results["outliers"].items():
        formatted_results += f"   - {col}: {stats['num_outliers']} outliers ({stats['outlier_percentage']:.2f}%)\n"

    formatted_results += "\n4. Trends in Categorical Data:\n"
    for col, trends in validation_results["trends"].items():
        formatted_results += f"   - {col}: {trends}\n"

    formatted_results += "\n5. GPT Model Response:\n"
    formatted_results += validation_results["gpt_response"]

    return formatted_results