import re
import requests
import pickle
import os

def parse(data, tag):
    pattern = "<" + tag + ">([\s\S]*?)<\/" + tag + ">"
    if all:
        obj = re.findall(pattern, data)
    return obj

def search_and_send(query, max_results, ids, api_url):
    while True:
        url = 'http://export.arxiv.org/api/query?search_query=' + query + '&start=0' + '&max_results=' + str(max_results) + '&sortBy=lastUpdatedDate&sortOrder=descending'
        data = requests.get(url).text
        entries = parse(data, "entry")
        counter = 0
        for entry in entries:
            url = parse(entry, "id")[0]
            if not(url in ids):
                title = parse(entry, "title")[0]
                abstract = parse(entry, "summary")[0]
                author = ', '.join(parse(entry,"name"))
                date = parse(entry, "published")[0]
                message = "\n".join(["=" * 20, "Title:  " + title, "Author: " + author, "URL: " + url])
                requests.post(api_url, json={"text": message})
                ids.append(url)
                counter = counter + 1
        if counter == 0 and len(entries) < max_results:
            requests.post(api_url, json={"text": "Currently, there is no available papers"})
            return 0
        elif counter == 0 and len(entries) == max_results:
            requests.post(api_url, json={"text": "Currently, there is no available papers and full query"})
            return 0


if __name__ == "__main__":
    base_path = os.path.dirname(__file__)
    with open(os.path.join(base_path, "api_url.txt")) as f:
        api_url = f.read().split('\n')[0]
    published_filename = os.path.join(base_path, "published.pkl")
    if os.path.exists(published_filename):
        with open(published_filename, "rb") as f:
            ids = pickle.load(f)
    else:
        ids = []
    # Query for arXiv API
    query = "(cat:cs.RO)"
    max_results = 25
    search_and_send(query, max_results, ids, api_url)
    # Update log of published data
    with open(published_filename, "wb") as f:
        pickle.dump(ids, f)
