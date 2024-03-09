from datetime import datetime, timezone
import json
import random

def noise_injection(injection_ratio = 0.5, noise_level=0.15):

    instruction_type = {
        "ARC": "You are a helpful assistant designed to output JSON. You must read the given article and create a question and 4 multiple choices based on the article and an answer. Make sure you include all required information required to answer in the question, as the solvers do not have access to the article. Make sure the answer is included in the choice options. The question and answers must be in the following format: 'question: What is the structure of the United Nations Security Council? choices: \"5 permanent members with veto power, 10 rotating members with no veto power\", \"5 permanent members and 10 rotating members, all with veto power\", \"10 permanent members with veto power, and 5 rotating members without veto power\", \"15 permanent members with veto power\" answer: A'",
        # "HellaSwag": "",
        # "MMLU": "",
        # "TruthfulQA": "",
        # "Winogrande": "",
        # "GSM8k": ""
    }

    for instruction in instruction_type:
        dataset_dir = f"data/dataset/{instruction}_2024-03-09.json"
        with open(dataset_dir, 'r', encoding='utf-8') as f: articles = json.load(f)

    # Choose injection ratio of articles to inject noise into
    num_articles = len(articles)
    injection_count = int(num_articles * injection_ratio)
    injection_indices = random.sample(range(num_articles), injection_count)

    # Inject noise into the articles
    for idx in injection_indices:
        article = articles[idx]
        # article['content'] = article['content'] + ' [NOISE]'

    # Save the articles to the JSON file
    save_dir = f"data/dataset/noisy_{instruction}_2024-03-09.json"
    with open(save_dir, 'w', encoding='utf-8') as f: json.dump(articles, f, ensure_ascii=False, indent=4)