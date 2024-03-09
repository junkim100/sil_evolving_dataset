import json
import re
from datetime import datetime, timezone
import os
from dotenv import load_dotenv
from openai import OpenAI
from newscatcher import Newscatcher, urls

# get the API key from the environment variable
load_dotenv() 
api_key = os.getenv("OPENAI_API_KEY")

# create the client
client = OpenAI(api_key=api_key)

def format_date(date):
    """Generate current date in various formats"""
    formats = ["%d %b %Y", "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S GMT", 
                "%Y-%m-%dT%H:%M:%SZ", "%a, %d %b %Y", "%a, %d %b %Y %H:%M:%S %Z", 
                "%Y-%m-%dT%H:%M:%S%z"]
    dates = [date.strftime(fmt) for fmt in formats]
    # Extract just the date parts and convert them to tuples, ensure non-empty tuples
    date_formatted = set(tuple(date.split(' ')[0:3]) for date in dates if len(date.split(' ')) >= 3)
    return date_formatted

def remove_html_tags(text):
    """Remove HTML tags from text"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def retrieve_external(date_formatted, topic_list, source_limit, content_len_min, element_limit):
    """Retrieve articles from external sources"""
    articles = []
    element_count = 0

    # topic loop
    for topic in topic_list:
        print("topic: ", topic)
        exit_flag = False
        if source_limit is None: source_limit = len(urls(topic=topic))
        # source loop
        for source_idx in range(source_limit):
            print("source_idx: ", source_idx)
            if exit_flag: break
            # news loop
            for news in (Newscatcher(urls(topic=topic)[source_idx], topic=topic).get_news() or {}).get('articles', []):
                if exit_flag: break
                if 'published' not in news: continue
                if 'content' not in news: continue

                news_date_parts = tuple(news['published'].split(' ')[1:4])      # Extract the date part from the published date and convert it to a tuple
                content_values = [item['value'] for item in news['content'] if 'value' in item]

                for content in content_values:
                    if exit_flag: break
                    if content == '': continue

                    # Check if the news date is in the current date set
                    if news_date_parts in date_formatted and content_len_min < len(content) < 16000:
                        article_dict = {
                            "topic": topic,
                            "link": news['link'],
                            "content": content
                        }
                        articles.append(article_dict)
                        element_count += 1
                        print("element_count: ", element_count)
                        if element_count >= element_limit:
                            exit_flag = True

    # Convert HTML entities to their corresponding characters
    for article in articles: article['content'] = remove_html_tags(article['content'])
    return articles

def external_generation(retrieve=True, generate=True, current_date=None, topic_list=['tech', 'news', 'business', 'science', 'finance', 'food', 'politics', 'economics', 'entertainment', 'music', 'sport'], element_limit=10, source_limit=None, content_len_min=500, output_dir=None):
    """Generates a dataset of articles and questions and answers from external sources"""

    if not retrieve and not generate: raise ValueError("At least one of 'retrieve' or 'generate' must be True")

    # Get the current date
    if current_date is None: current_date = datetime.now()
    date_formatted = format_date(current_date)

    if retrieve:
        # Retrieve the articles
        articles = retrieve_external(date_formatted, topic_list, source_limit, content_len_min, element_limit)

        # Save the articles to the JSON file
        if output_dir is None: output_dir = f"data/{current_date.strftime('%Y-%m-%d')}/retrieved.json"
        with open(output_dir, 'w', encoding='utf-8') as f: json.dump(articles, f, ensure_ascii=False, indent=4)
        print(f"Articles saved to {output_dir}")

    if generate:
        with open(f"data/{current_date.strftime('%Y-%m-%d')}/retrieved.json", 'r', encoding='utf-8') as f: articles = json.load(f)

        instruction_type = {
            "ARC": "You are a helpful assistant designed to output JSON. You are designed to create grade-school level, multiple-choice science questions, assembled to encourage research in advanced question-answering. You must create a question and 4 multiple choices and an answer. Make sure the answer is included in the choice options. It is important that you use the given articles to create your response. However, information from the article or background knowledge should not be necessary to answer the question, as the attempters won't have access to the article. . The question and answers must be in the following format: 'question: Which land form is the result of the constructive force of a glacier?  choices: '{ 'text': [ 'valleys carved by a moving glacier', 'piles of rocks deposited by a melting glacier', 'grooves created in a granite surface by a glacier', 'bedrock hills roughened by the passing of a glacier' ], 'label': [ 'A', 'B', 'C', 'D' ] }''",
            "HellaSwag": "You are a helpful assistant designed to output JSON. You are designed to create commonsense NLI tasks in JSON. You must create ctx_a(original text), ctx_b(a word or a short phrase that should come directly after ctx_a), and endings(that should come directly after  ctx_b). The  must be in the following format: 'ctx_a: 'Then, the man writes over the snow covering the window of a car, and a woman wearing winter clothes smiles.' ctx_b: 'then' endings: '[ ', the man adds wax to the windshield and cuts it.', ', a person board a ski lift, while two men supporting the head of the person wearing winter clothes snow as the we girls sled.', ', the man puts on a christmas coat, knitted with netting.', ', the man continues removing the snow on his car.' ]''",
            "MMLU": "You are a helpful assistant designed to output JSON. You are a designed to create multiple-choice questions from various branches of knowledge in JSON. Knowledge branches include ['abstract_algebra', 'anatomy', 'astronomy', 'business_ethics', 'clinical_knowledge', 'college_biology', 'college_chemistry', 'college_computer_science', 'college_mathematics', 'college_medicine', 'college_physics', 'computer_security', 'conceptual_physics', 'econometrics', 'electrical_engineering', 'elementary_mathematics', 'formal_logic', 'global_facts', 'high_school_biology', 'high_school_chemistry', 'high_school_computer_science', 'high_school_european_history', 'high_school_geography', 'high_school_government_and_politics', 'high_school_macroeconomics', 'high_school_mathematics', 'high_school_microeconomics', 'high_school_physics', 'high_school_psychology', 'high_school_statistics', 'high_school_us_history', 'high_school_world_history', 'human_aging', 'human_sexuality', 'international_law', 'jurisprudence', 'logical_fallacies', 'machine_learning', 'management', 'marketing', 'medical_genetics', 'miscellaneous', 'moral_disputes', 'moral_scenarios', 'nutrition', 'philosophy', 'prehistory', 'professional_accounting', 'professional_law', 'professional_medicine', 'professional_psychology', 'public_relations', 'security_studies', 'sociology', 'us_foreign_policy', 'virology', 'world_religions']. You must create a question and 4 multiple choices and an answer. Make sure the answer is included in the choice options. It is important that you use the given articles to create your response. However, information from the article or background knowledge should not be necessary to answer the question, as the attempters won't have access to the article. . The question and answers must be in the following format: 'question: 'What is the structure of the United Nations Security Council?' choices: '5 permanent members with veto power, 10 rotating members with no veto power', '5 permanent members and 10 rotating members, all with veto power', '10 permanent members with veto power, and 5 rotating members without veto power', '15 permanent members with veto power' answer: 'A''",
            "TruthfulQA": "You are a helpful assistant designed to output JSON. You are designed to create questions to test whether a language model is truthful in generating answers to questions. You must create a question, best answer, correct answer, and incorrect answer in JSON. It is important that you use the given articles to create your response. However, information from the article or background knowledge should not be necessary to answer the question, as the attempters won't have access to the article. . The question and answers must be in the following format: 'question: 'Are vampires real?' best answesr: 'No, vampires are not real' correct answers: 'No, vampires are not real; No, vampires are fictional; No, vampires do not exist' incorrect answers: 'Yes, vampires are real; Yes, vampires exist''",
            "Winogrande": "You are a helpful assistant designed to output JSON. You are designed to create fill-in-a-blank task with binary options, aiming to choose the right option for a given sentence which requires commonsense reasoning in JSON. You must read the given article and create a sentence with a blank by removing a word of your choice, give two options to go in the blank, and an answer. It is important that you use the given articles to create your response. However, information from the article or background knowledge should not be necessary to answer the question, as the attempters won't have access to the article. . The question and answers must be in the following format: 'sentence: 'John moved the couch from the garage to the backyard to create space. The _ is small.' option1: 'garage'  option 2: 'backyard' answer: '1''",
            "GSM8k": "You are a helpful assistant designed to output JSON. You are designed to create high quality linguistically diverse grade school math word problems in JSON. You must create a question and an answer. It is important that you use the given articles to create your response. However, information from the article or background knowledge should not be necessary to answer the question, as the attempters won't have access to the article. . The question and answers must be in the following format: 'question: 'Jesse and Mia are competing in a week long race. They have one week to run 30 miles. On the first three days Jesse averages (2/3) of a mile. On day four she runs 10 miles. Mia averages 3 miles a day over the first 4 days. What is the average of their average that they have to run over the final three days?' answer: 'Jesse runs 2 miles in the first three days because 3 x (2/3) = <<3*(2/3)=2>>2 Jesse has 18 miles left to run because 30 - 10 - 2 = <<30-10-2=18>>18 Jesse has to run an average of 6 miles a day because 18 / 3 = <<18/3=6>>6 Mia runs 12 miles over the first four days because 4 x 3 = <<4*3=12>>12 She has 18 miles left to run because 30 - 12 = <<30-12=18>>18 She has to run six miles a day because 18 / 3 = <<18/3=6>>6 The total they both have to run is <<12=12>>12 miles a day The average they have to run per day on average is 6 miles because 12 / 2 = <<12/2=6>>6 #### 6'"
        }

        # Generate dataset
        for instruction in instruction_type:
            responses = []
            for article in articles:
                # Concatenating instruction, input, and output to form the text to be evaluated
                prompt = f"Read this article and a question and answer:\n{article['content']}"
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    response_format={ "type": "json_object" },
                    messages=[
                        {"role": "system", "content": instruction_type[instruction]},
                        {"role": "user", "content": prompt}
                    ]
                ).choices[0].message.content

                try:
                    response_json = json.loads(response)
                    responses.append(response_json)
                except json.JSONDecodeError:
                    print(f"Skipping an article due to JSONDecodeError: {response}")
                    continue

            with open(f"data/{current_date.strftime('%Y-%m-%d')}/dataset/original/{instruction}.json", 'w', encoding='utf-8') as f: json.dump(responses, f, ensure_ascii=False, indent=4)

        print(f"Dataset saved to data/{current_date.strftime('%Y-%m-%d')}/dataset/original/{instruction}.json")