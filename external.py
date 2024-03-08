from newscatcher import Newscatcher, urls
from datetime import datetime, timezone
import json

# Generate current date in various formats
current_date = datetime.now()
date_formats = ["%d %b %Y", "%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S GMT", 
                "%Y-%m-%dT%H:%M:%SZ", "%a, %d %b %Y", "%a, %d %b %Y %H:%M:%S %Z", 
                "%Y-%m-%dT%H:%M:%S%z"]
current_dates = [current_date.strftime(fmt) for fmt in date_formats]

# Extract just the date parts and convert them to tuples, ensure non-empty tuples
current_date_strs = set(tuple(date.split(' ')[0:3]) for date in current_dates if len(date.split(' ')) >= 3)

# topic_list = ['tech', 'news', 'business', 'science', 'finance', 'food', 'politics', 'economics', 'travel', 'entertainment', 'music', 'sport', 'world']
topic_list = ['tech', 'news', 'business', 'science', 'travel', 'entertainment', 'music', 'sport']
# topic_list = ['business']

articles = []

# topic loop
element_count = 0
element_limit = 10

for topic in topic_list:
    exit_flag = False
    print("TOPIC: ", topic, "//////////////////////////////////////////////////////////////////")
    # source loop
    for source_idx in range(len(urls(topic=topic))):
    # for source_idx in range(10):
        if exit_flag: break
        # news loop
        for news in (Newscatcher(urls(topic=topic)[source_idx], topic=topic).get_news() or {}).get('articles', []):
            if exit_flag: break
            if 'published' not in news: continue
            if 'content' not in news: continue

            # Extract the date part from the published date and convert it to a tuple
            news_date_parts = tuple(news['published'].split(' ')[1:4])

            # print(news['content'])
            # Assuming news['content'] returns a list of dictionaries like you've shown
            content_values = [item['value'] for item in news['content'] if 'value' in item]

            # Now, content_values will contain all the 'value' entries from the dictionaries
            # If you just want to print them, you can do:
            for content in content_values:
                if exit_flag: break
                if content == '': continue

                # Check if the news date is in the current date set
                if news_date_parts in current_date_strs and len(content) > 500:
                    article_dict = {
                        "topic": topic,
                        "link": news['link'],
                        "content": content
                    }
                    articles.append(article_dict)
                    element_count += 1
                    if element_count >= element_limit:
                        exit_flag = True

filename = f"{datetime.now().strftime('%Y-%m-%d')}.json"

# Save the articles to the JSON file
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print(f"Articles saved to {filename}")