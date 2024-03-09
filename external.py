from newscatcher import Newscatcher, urls
from datetime import datetime, timezone
import json

# Generate current date in various formats
def format_date(date):
    formats = ["%d %b %Y", "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S GMT", 
                "%Y-%m-%dT%H:%M:%SZ", "%a, %d %b %Y", "%a, %d %b %Y %H:%M:%S %Z", 
                "%Y-%m-%dT%H:%M:%S%z"]
    dates = [date.strftime(fmt) for fmt in formats]
    # Extract just the date parts and convert them to tuples, ensure non-empty tuples
    date_formatted = set(tuple(date.split(' ')[0:3]) for date in dates if len(date.split(' ')) >= 3)
    return date_formatted

def retrieve_external(date_formatted, topic_list, content_len_limit, element_limit):
    articles = []
    element_count = 0

    # topic loop
    for topic in topic_list:
        exit_flag = False
        print("TOPIC: ", topic, "//////////////////////////////////////////////////////////////////")
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
                    if news_date_parts in date_formatted and len(content) > content_len_limit:
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

def external_generation(current_date=None, topic_list=None, element_limit=10, source_limit=None, content_len_limit=500, output_dir=None):
    if current_date is None: current_date = datetime.now()
    date_formatted = format_date(current_date)

    if topic_list is None: topic_list = ['tech', 'news', 'business', 'science', 'finance', 'food', 'politics', 'economics', 'travel', 'entertainment', 'music', 'sport', 'world']

    # Retrieve the articles
    articles = retrieve_external(date_formatted, topic_list, content_len_limit, element_limit)

    # Save the articles to the JSON file
    if output_dir is None: output_dir = f"data/retrieved/{current_date.strftime('%Y-%m-%d')}.json"
    with open(output_dir, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    print(f"Articles saved to {output_dir}")