from datetime import datetime, timezone, timedelta
import json
import random

import nltk
from nltk.corpus import wordnet

nltk.download('punkt')
nltk.download('wordnet')

current_date = datetime.now(timezone(timedelta(hours=-7)))

def inject_syntactical_noise(text, noise_level=0.15):
    """Introduce syntactical noise by randomly shuffling sentence structures"""
    sentences = nltk.sent_tokenize(text)
    num_sentences_to_change = int(len(sentences) * noise_level)
    changed_indices = random.sample(range(len(sentences)), num_sentences_to_change)

    for i in changed_indices:
        words = nltk.word_tokenize(sentences[i])
        random.shuffle(words)
        sentences[i] = ' '.join(words)

    return ' '.join(sentences)

def inject_semantic_noise(text, noise_level=0.15):
    """Introduce semantic noise by replacing words with their synonyms"""
    words = text.split()
    num_words_to_change = int(len(words) * noise_level)
    changed_indices = random.sample(range(len(words)), num_words_to_change)

    for i in changed_indices:
        synonyms = set()
        for syn in wordnet.synsets(words[i]):
            for lemma in syn.lemmas():
                synonyms.add(lemma.name())
        if synonyms:
            synonyms.discard(words[i])
            if synonyms:  # Ensure there is at least one different synonym
                words[i] = random.choice(list(synonyms))

    return ' '.join(words)

def inject_typographical_noise(text, noise_level=0.15):
    """Introduce typographical errors into the text"""
    characters = list(text)
    num_chars_to_change = int(len(characters) * noise_level)

    for _ in range(num_chars_to_change):
        char_index = random.randint(0, len(characters) - 1)
        characters[char_index] = random.choice('abcdefghijklmnopqrstuvwxyz')

    return ''.join(characters)

def noise_injection(injection_ratio=0.5, noise_level=0.15):
    """Inject noise into the original datasets"""
    instruction_type = ["ARC", "HellaSwag", "MMLU", "TruthfulQA", "WinoGrande", "GSM8k"]

    for instruction in instruction_type:
        dataset_dir = f"data/{current_date.strftime('%Y-%m-%d')}/dataset/original/{instruction}.json"
        with open(dataset_dir, 'r', encoding='utf-8') as f: articles = json.load(f)

        # Choose injection ratio of articles to inject noise into
        num_articles = len(articles)
        injection_count = int(num_articles * injection_ratio)
        injection_indices = random.sample(range(num_articles), injection_count)

        # Inject noise into the articles
        for idx in injection_indices:
            article = articles[idx]

            keywords = ["question", "ctx_a", "endings", "sentence"]
            keyword = [keyword for keyword in keywords if keyword in article][0]

            if keyword != []:
                # Randomly choose which type of noise to inject
                noise_type = random.choice(['semantic', 'syntactical', 'typographical'])
                if noise_type == 'syntactical':
                    article[keyword] = inject_syntactical_noise(article[keyword], noise_level)
                elif noise_type == 'semantic':
                    article[keyword] = inject_semantic_noise(article[keyword], noise_level)
                else:
                    article[keyword] = inject_typographical_noise(article[keyword], noise_level)

                print(noise_type)
                print(article[keyword])
                print("\n\n")

        # Save the articles with injected noise
        save_dir = f"data/{current_date.strftime('%Y-%m-%d')}/dataset/noised/noised_{instruction}.json"
        with open(save_dir, 'w', encoding='utf-8') as f: json.dump(articles, f, ensure_ascii=False, indent=4)
        print(f"Noised {instruction} dataset saved at {save_dir}")
