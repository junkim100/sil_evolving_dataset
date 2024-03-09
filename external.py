from newscatcher import Newscatcher, urls
from datetime import datetime, timezone
import json
from dotenv import load_dotenv
import os
from openai import OpenAI

# get the API key from the environment variable
load_dotenv() 
api_key = os.getenv("OPENAI_API_KEY")

# create the client
client = OpenAI(api_key=api_key)

# Generate current date in various formats
def format_date(date):
    formats = ["%d %b %Y", "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S GMT", 
                "%Y-%m-%dT%H:%M:%SZ", "%a, %d %b %Y", "%a, %d %b %Y %H:%M:%S %Z", 
                "%Y-%m-%dT%H:%M:%S%z"]
    dates = [date.strftime(fmt) for fmt in formats]
    # Extract just the date parts and convert them to tuples, ensure non-empty tuples
    date_formatted = set(tuple(date.split(' ')[0:3]) for date in dates if len(date.split(' ')) >= 3)
    return date_formatted

def retrieve_external(date_formatted, topic_list, source_limit, content_len_limit, element_limit):
    articles = []
    element_count = 0

    # topic loop
    for topic in topic_list:
        exit_flag = False
        if source_limit is None: source_limit = len(urls(topic=topic))
        # source loop
        for source_idx in range(source_limit):
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
                    if news_date_parts in date_formatted and content_len_limit < len(content) < 16000:
                        article_dict = {
                            "topic": topic,
                            "link": news['link'],
                            "content": content
                        }
                        articles.append(article_dict)
                        element_count += 1
                        if element_count >= element_limit:
                            exit_flag = True

    return articles

def external_generation(retrieve=True, generate=True, current_date=None, topic_list=['tech', 'news', 'business', 'science', 'finance', 'food', 'politics', 'economics', 'travel', 'entertainment', 'music', 'sport', 'world'], element_limit=10, source_limit=None, content_len_limit=500, output_dir=None):
    # Get the current date
    if current_date is None: current_date = datetime.now()
    date_formatted = format_date(current_date)

    if retrieve:
        # Retrieve the articles
        articles = retrieve_external(date_formatted, topic_list, source_limit, content_len_limit, element_limit)

        # Save the articles to the JSON file
        if output_dir is None: output_dir = f"data/retrieved/{current_date.strftime('%Y-%m-%d')}.json"
        with open(output_dir, 'w', encoding='utf-8') as f: json.dump(articles, f, ensure_ascii=False, indent=4)
        print(f"Articles saved to {output_dir}")

    if generate:
        with open(f"data/retrieved/{current_date.strftime('%Y-%m-%d')}.json", 'r', encoding='utf-8') as f: articles = json.load(f)

        instruction_type = {
            "ARC": "You are a helpful assistant designed to output JSON. You must read the given article and create a question and 4 multiple choices based on the article and an answer. Make sure you include all required information required to answer in the question, as the solvers do not have access to the article. Make sure the answer is included in the choice options. The question and answers must be in the following format: 'question: What is the structure of the United Nations Security Council? choices: \"5 permanent members with veto power, 10 rotating members with no veto power\", \"5 permanent members and 10 rotating members, all with veto power\", \"10 permanent members with veto power, and 5 rotating members without veto power\", \"15 permanent members with veto power\" answer: A'",
            # "HellaSwag": "",
            # "MMLU": "",
            # "TruthfulQA": "",
            # "Winogrande": "",
            # "GSM8k": ""
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

                response_json = json.loads(response)
                responses.append(response_json)

            with open(f"data/dataset/{instruction}_{current_date.strftime('%Y-%m-%d')}.json", 'w', encoding='utf-8') as f: json.dump(responses, f, ensure_ascii=False, indent=4)

        print(f"Dataset saved to data/dataset/{instruction}_{current_date.strftime('%Y-%m-%d')}.json")
    