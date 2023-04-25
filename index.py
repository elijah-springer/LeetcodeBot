import re


class Question:
    def __init__(self, number, name, url, category):
        self.number = number
        self.name = name
        self.url = url
        self.category = category


index = []
category = None

with open('leetcodequestions.md', 'r', encoding="utf-8") as f:
    for line in f:
        if '###' in line:
            category = line[4:-1]
        if category and (data := re.search("\[(\d{4}) - ([a-zA-Z0-9\s]+)]\(([/A-Z\.a-z:-]+)\)", line)):
            index.append(Question(*data.groups(), category))


def filter_by_category(index, *categories):
    return [q for q in index if q.category in categories]


print([q.name for q in filter_by_category(index, 'Stack', 'Binary Search')])

