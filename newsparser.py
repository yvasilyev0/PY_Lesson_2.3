import json
import re
import string


def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr, '', raw_html)
    return clean_text


def get_rss_feed_from_file(file_name, encoding):
    with open(file_name, encoding=encoding) as news:
        file_content = json.load(news)
        return file_content['rss']


def get_channel_data(feed):
    channel_details = feed['channel']
    channel_items = channel_details['item']
    return channel_items


def get_item_content(channel_data):
    return channel_data['__cdata']


def get_text_from_json(file_name, encoding):
    news_list = []
    feed = get_rss_feed_from_file(file_name, encoding)
    content = get_channel_data(feed)
    for item in content:
        for value in item.values():
            if type(value) is dict:
                data = get_item_content(value)
                clean_data = clean_html(data.strip())
                news_list.append(clean_data)
            else:
                news_list.append(value)
    plain_text = ' '.join(news_list)
    text = "\n".join([s for s in plain_text.split("\n") if s]).lower()
    return text


def calculate_words_frequency(text):
    hist = dict()
    for word in text.split():
        word = word.strip(string.punctuation + string.whitespace)
        word = word.lower()
        hist[word] = hist.get(word, 0) + 1
    return hist


def print_summary(hist, word_len, words_count):
    filtered = {key: value for key, value in hist.items() if len(key) >= word_len}
    ordered = sorted(filtered.items(), key=lambda t: t[1], reverse=True)[:words_count]
    for num, item in enumerate(ordered):
        print('{}: {}'.format(num + 1, item))
    print('\n')


def get_words_frequency_in_file(file, encoding):
    print("Results for '{}' with encoding '{}'".format(file, encoding))
    text = get_text_from_json(file, encoding)
    hist = calculate_words_frequency(text)
    print_summary(hist, 6, 10)


files = {'newsfr.json': 'iso8859_5',
         'newsafr.json': 'utf-8',
         'newscy.json': 'koi8_r',
         'newsit.json': 'cp1251'
         }

for file_name, encoding in files.items():
    get_words_frequency_in_file(file_name, encoding)
