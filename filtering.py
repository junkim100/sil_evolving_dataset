import json
import os

def filter_arc(data, filtered_path):
    required_keys = ["question", "choices", "answerKey"]
    final_keys = ["id", "question", "choices", "answerKey"]
    filtered_data = []

    def normalize_key(key):
        key = key.replace('_', ' ')
        if key.endswith('answers') or key.endswith('questions'):
            key = key[:-1]
        return key

    for item in data:
        # Normalize and map the keys
        normalized_item = {normalize_key(key): value for key, value in item.items()}

        # Check if all required keys are present
        if all(key in normalized_item for key in required_keys):
            # Construct the new item with required final keys
            new_item = {final_key: normalized_item.get(final_key, "") for final_key in final_keys}
            filtered_data.append(new_item)

    with open(filtered_path+'filtered_ARC.jsonl', 'w') as f:
        for item in filtered_data:
            f.write(json.dumps(item) + '\n')

    return filtered_data

def filter_truthfulqa(data, filtered_path):
    required_keys = ["Question", "Best Answer", "Correct Answers", "Incorrect Answers"]
    final_keys = ["Type", "Category", "Question", "Best Answer", "Correct Answers", "Incorrect Answers", "Source"]
    filtered_data = []

    def normalize_key(key):
        key = key.replace('_', ' ')
        return key

    for item in data:
        # Normalize and map the keys
        normalized_item = {normalize_key(key): value for key, value in item.items()}

        # Check if all required keys are present
        if all(key in normalized_item for key in required_keys):
            # Construct the new item with required final keys
            new_item = {final_key: normalized_item.get(final_key, "") for final_key in final_keys}
            filtered_data.append(new_item)

    with open(filtered_path+'filtered_TruthfulQA.jsonl', 'w') as f:
        for item in filtered_data:
            f.write(json.dumps(item) + '\n')

    return filtered_data

def filter_gsm8k(data, filtered_path):
    required_keys = ["question", "answer"]
    final_keys = ["question", "answer"]
    filtered_data = []

    def normalize_key(key):
        key = key.replace('_', ' ')
        if key.endswith('answers') or key.endswith('questions'):
            key = key[:-1]
        return key

    for item in data:
        # Normalize and map the keys
        normalized_item = {normalize_key(key): value for key, value in item.items()}

        # Check if all required keys are present
        if all(key in normalized_item for key in required_keys):
            # Construct the new item with required final keys
            new_item = {final_key: normalized_item.get(final_key, "") for final_key in final_keys}
            filtered_data.append(new_item)

    with open(filtered_path+'filtered_GSM8k.jsonl', 'w') as f:
        for item in filtered_data:
            f.write(json.dumps(item) + '\n')

    return filtered_data

def filter_hellaswag(data, filtered_path):
    required_keys = ["ctx_a", "ctx_b", "endings"]
    final_keys = ["ind", "activity_label", "ctx_a", "ctx_b", "ctx", "endings", "source_id", "split", "split_type", "label"]
    filtered_data = []

    # Create new column called ctx that combines ctx_a and ctx_b
    for item in data:
        item["ctx"] = item["ctx_a"] + " " + item["ctx_b"]

    def normalize_key(key):
        return key

    for item in data:
        # Normalize and map the keys
        normalized_item = {normalize_key(key): value for key, value in item.items()}

        # Check if all required keys are present
        if all(key in normalized_item for key in required_keys):
            # Construct the new item with required final keys
            new_item = {final_key: normalized_item.get(final_key, "") for final_key in final_keys}
            filtered_data.append(new_item)

    with open(filtered_path+'filtered_HellaSwag.jsonl', 'w') as f:
        for item in filtered_data:
            f.write(json.dumps(item) + '\n')

    return filtered_data

def filter_mmlu(data, filtered_path):
    required_keys = ["question", "choices", "answer"]
    final_keys = ["question", "subject", "choices", "answer"]
    filtered_data = []

    def normalize_key(key):
        key = key.replace('_', ' ')
        if key.endswith('answers') or key.endswith('questions'):
            key = key[:-1]
        return key

    for item in data:
        # Normalize and map the keys
        normalized_item = {normalize_key(key): value for key, value in item.items()}

        # Check if all required keys are present
        if all(key in normalized_item for key in required_keys):
            # Construct the new item with required final keys
            new_item = {final_key: normalized_item.get(final_key, "") for final_key in final_keys}
            filtered_data.append(new_item)

    with open(filtered_path+'filtered_ARC.jsonl', 'w') as f:
        for item in filtered_data:
            f.write(json.dumps(item) + '\n')

    return filtered_data

def filter_winogrande(data, filtered_path):
    required_keys = ["sentence", "option1", "option2", "answer"]
    final_keys = ["sentence", "option1", "option2", "answer"]
    filtered_data = []

    def normalize_key(key):
        # Remove underscores and convert plurals to singular
        key = key.replace('_', ' ')
        if key.endswith('answers') or key.endswith('sentences'):
            key = key[:-1]
        return key

    for item in data:
        # Normalize and map the keys
        normalized_item = {normalize_key(key): value for key, value in item.items()}

        # Check if all required keys are present
        if all(key in normalized_item for key in required_keys):
            # Construct the new item with required final keys
            new_item = {final_key: normalized_item.get(final_key, "") for final_key in final_keys}
            filtered_data.append(new_item)

    with open(filtered_path+'filtered_GSM8k.jsonl', 'w') as f:
        for item in filtered_data:
            f.write(json.dumps(item) + '\n')

    return filtered_data

def filter_data(path):
    noised_path = path + "noised/"
    filtered_path = path + "filtered/"
    # read all json files in the specified folder
    for root, dirs, files in os.walk(noised_path):
        for file in files:
            if file.endswith(".json"):
                with open(os.path.join(root, file), "r") as f:
                    data = json.load(f)
                    dataset = os.path.splitext(os.path.basename(f.name))[0][7:]
                    if dataset == "ARC":
                        filter_arc(data, filtered_path)
                    elif dataset == "TruthfulQA":
                        filter_truthfulqa(data, filtered_path)
                    elif dataset == "GSM8k":
                        filter_gsm8k(data, filtered_path)
                    elif dataset == "HellaSwag":
                        filter_hellaswag(data, filtered_path)
                    elif dataset == "MMLU":
                        filter_mmlu(data, filtered_path)
                    elif dataset == "WinoGrande":
                        filter_winogrande(data, filtered_path)